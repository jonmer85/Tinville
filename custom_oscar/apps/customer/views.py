from custom_oscar.apps.customer.forms import UserAddressForm
from django.shortcuts import get_list_or_404, get_object_or_404
from oscar.apps.customer.views import AddressUpdateView as CoreAddressUpdateView
from oscar.apps.customer.views import AddressCreateView as CoreAddressCreateView
from oscar.apps.customer.views import AddressListView as CoreAddressListView
from oscar.apps.customer.views import AddressChangeStatusView as CoreAddressChangeStatusView
from oscar.core.loading import get_model

Partner = get_model('partner', 'Partner')
UserAddress = get_model('address', 'UserAddress')


class AddressUpdateView(CoreAddressUpdateView):
    template_name = 'edit_address.html'
    form_class = UserAddressForm


class AddressCreateView(CoreAddressCreateView):
    template_name = 'edit_address.html'
    form_class = UserAddressForm


class AddressListView(CoreAddressListView):
    template_name = 'address_list.html'

    def get_context_data(self, **kwargs):
        ctx = super(AddressListView, self).get_context_data(**kwargs)
        ctx['shop_shipping_address_pk'] = self._get_shipping_address_pk_that_is_shop_shipping_address()
        return ctx

    def _get_shipping_address_pk_that_is_shop_shipping_address(self):
        addresses = UserAddress._default_manager.filter(user=self.request.user)
        partners = get_list_or_404(Partner, users__pk=self.request.user.pk)

        if partners is not None:
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


class AddressChangeStatusView(CoreAddressChangeStatusView):
    def get(self, request, pk=None, action=None, *args, **kwargs):
        if action == 'default_for_shop':
            # Find all partners associated with this user and set the new address
            address = get_object_or_404(UserAddress, user=self.request.user,
                                        pk=pk)

            partners = get_list_or_404(Partner, users__pk=self.request.user.pk)

            for partner in partners:
                partner_address = partner.primary_address
                if partner_address is not None:
                    partner_address.delete()
                partner_address = partner.addresses.model(partner=partner)
                address.populate_alternative_model(partner_address)
                partner_address.save()
                partner.save()

        return super(AddressChangeStatusView, self).get(
            request, pk, action, *args, **kwargs)

