import json
from django.template.context import RequestContext
from custom_oscar.apps.customer.forms import UserAddressForm
from django.shortcuts import get_list_or_404, get_object_or_404, redirect
from oscar.apps.customer.views import AddressUpdateView as CoreAddressUpdateView, OrderHistoryView as CoreOrderHistoryView
from oscar.apps.customer.views import AddressCreateView as CoreAddressCreateView
from oscar.apps.customer.views import AddressListView as CoreAddressListView
from oscar.apps.customer.views import AddressChangeStatusView as CoreAddressChangeStatusView
from oscar.apps.customer.views import AddressDeleteView as CoreAddressDeleteView
from oscar.apps.customer.views import AccountAuthView as CoreAccountAuthView
from user.forms import LoginForm
from oscar.core.loading import get_model
from django.contrib.auth.views import login as auth_view_login
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from common.utils import get_list_or_empty


Partner = get_model('partner', 'Partner')
UserAddress = get_model('address', 'UserAddress')


class AccountAuthView(CoreAccountAuthView):
    template_name = 'login_registration.html'
    login_form_class = LoginForm
    login_prefix = 'login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        template = self.template_name
        context = self.get_context_data(**kwargs)
        return render_to_response(template, context, context_instance=RequestContext(request))

    def get_context_data(self, *args, **kwargs):
        ctx = {}
        if 'login_form' not in kwargs:
             ctx['login_form'] = self.get_login_form()
        return ctx

    def post(self, request, *args, **kwargs):
        ud_dict = {'username': str(request.POST['username']).lower()}
        ud_dict['username'] = ud_dict['username'].strip()

        request.POST = request.POST.copy()
        request.POST.update(ud_dict)

        form = LoginForm(request=request, data=request.POST)
        logged_in = False
        data = {}

        if form.is_valid():
            data = auth_view_login(request, form)
            logged_in = True

            return redirect(self.get_login_success_url(form))

        return HttpResponseBadRequest(json.dumps(form.errors), content_type="application/json")

    def get_login_form(self, bind_data=False):
        return self.login_form_class(
            **self.get_login_form_kwargs(bind_data))

    def get_login_form_kwargs(self, bind_data=False):
        kwargs = { 'redirect_url' : self.request.GET.get(self.redirect_field_name, '') }
        return kwargs

    def get_login_success_url(self, form):
        redirect_url = form.data['next']
        if redirect_url:
            return redirect_url

    def validate_login_form(self, request):
        form = self.get_login_form(bind_data=True)
        if form.is_valid():
            data = auth_view_login(request, form)
            logged_in = True

            return redirect(self.get_login_success_url(form))

        ctx = self.get_context_data(login_form=form)
        return self.render_to_response(ctx)


class AddressUpdateView(CoreAddressUpdateView):
    template_name = 'edit_address.html'
    form_class = UserAddressForm


class AddressCreateView(CoreAddressCreateView):
    template_name = 'edit_address.html'
    form_class = UserAddressForm

    def get_success_url(self):
        # Assign shop shipping address if none assigned
        if self.request.user.is_seller:
            if _get_shipping_address_pk_that_is_shop_shipping_address(self.request) is None:
                _assign_shop_shipping_address(self.request.user, self.object.id)
        return super(AddressCreateView, self).get_success_url()


class AddressListView(CoreAddressListView):
    template_name = 'address_list.html'

    def get_context_data(self, **kwargs):
        ctx = super(AddressListView, self).get_context_data(**kwargs)
        if self.request.user.is_seller:
            ctx['shop_shipping_address_pk'] = _get_shipping_address_pk_that_is_shop_shipping_address(self.request)
        return ctx


class AddressChangeStatusView(CoreAddressChangeStatusView):
    def get(self, request, pk=None, action=None, *args, **kwargs):
        if action == 'default_for_shop':
            _assign_shop_shipping_address(self.request.user, pk)

        return super(AddressChangeStatusView, self).get(
            request, pk, action, *args, **kwargs)


class AddressDeleteView(CoreAddressDeleteView):
    def delete(self, request, *args, **kwargs):
        # Delete any partner address (shop shipping address) associated with this address
        address_pk = kwargs['pk']

        shop_address_pk = _get_shipping_address_pk_that_is_shop_shipping_address(self.request)

        if shop_address_pk is not None and shop_address_pk == int(address_pk):
            partners = get_list_or_404(Partner, users__pk=self.request.user.pk)

            for partner in partners:
                partner_address = partner.primary_address
                if partner_address is not None:
                    partner_address.delete()
        return super(AddressDeleteView, self).delete(request, *args, **kwargs)


def _get_shipping_address_pk_that_is_shop_shipping_address(request):
    addresses = UserAddress._default_manager.filter(user=request.user)
    if request.user.is_staff:
        partners = get_list_or_empty(Partner, users__pk=request.user.pk)
    else:
        partners = get_list_or_404(Partner, users__pk=request.user.pk)

    if partners and partners is not None:
        partner_address = partners[0].primary_address
        if partner_address is not None:
            for address in addresses:
                if partner_address.title == address.title \
                        and partner_address.first_name == address.first_name \
                        and partner_address.last_name == address.last_name \
                        and partner_address.line1 == address.line1 \
                        and partner_address.line2 == address.line2 \
                        and partner_address.line3 == address.line3 \
                        and partner_address.line4 == address.line4 \
                        and partner_address.state == address.state \
                        and partner_address.postcode == address.postcode \
                        and partner_address.country == address.country \
                        and partner_address.search_text == address.search_text:
                    return address.pk
    return None


def _assign_shop_shipping_address(user, address_pk):
    # Find all partners associated with this user and set the new address
    address = get_object_or_404(UserAddress, user=user,
                                pk=address_pk)
    partners = get_list_or_404(Partner, users__pk=user.pk)
    for partner in partners:
        partner_address = partner.primary_address
        if partner_address is not None:
            partner_address.delete()
        partner_address = partner.addresses.model(partner=partner)
        address.populate_alternative_model(partner_address)
        partner_address.save()
        partner.save()


class OrderHistoryView(CoreOrderHistoryView):
    def get_queryset(self):
        qs = self.model._default_manager.filter(user=self.request.user).exclude(number__contains="-")
        if self.form.is_bound and self.form.is_valid():
            qs = qs.filter(**self.form.get_filters())
        return qs



