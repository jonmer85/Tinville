import json
from django.contrib.sites.shortcuts import get_current_site

from django.shortcuts import get_object_or_404, resolve_url
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import login as auth_view_login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect
from designer_shop.models import Shop
from oscar.core.loading import get_model
import stripe

from custom_oscar.apps.dashboard.orders.views import queryset_orders_for_user
from user.forms import TinvilleUserCreationForm, LoginForm, PaymentInfoFormWithFullName, BetaAccessForm
from user.models import TinvilleUser
from custom_oscar.apps.dashboard.views import get_dashboard_notifications


Partner = get_model('partner', 'Partner')

class DesignerPaymentInfoView(FormView):
    template_name = 'payment_info.html'
    form_class = PaymentInfoFormWithFullName
    success_url = reverse_lazy('designer-payment-info')

    def get_context_data(self, **kwargs):
        context = super(DesignerPaymentInfoView, self).get_context_data(**kwargs)
        context['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        user = self.request.user
        if user.account_token:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            token = stripe.Token.retrieve(user.account_token)
            context['last4'] = token.card.last4

        return context

    def form_valid(self, form):
        # Add the payment info to the user
        token = form.cleaned_data['stripe_token']
        full_legal_name = form.cleaned_data['full_legal_name']
        type = form.cleaned_data['recipient_type']
        tax_id = form.cleaned_data['tax_id']

        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            type_string = "individual" if type == "1" else "corporation"
            if not self.request.user.recipient_id:
                # No recipient, create one
                recipient = stripe.Recipient.create(
                  name=full_legal_name,
                  type=type_string,
                  tax_id=tax_id,
                  email=self.request.user.email,
                  card=token)
            else:
                # Update existing recipient
                recipient = stripe.Recipient.retrieve(self.request.user.recipient_id)
                recipient.name = full_legal_name
                recipient.type = type_string
                recipient.tax_id = tax_id
                recipient.card = token
                recipient.save()


            self.request.user.recipient_id = recipient.id
            self.request.user.account_token = token
            self.request.user.save()

            messages.success(self.request, "You have successfully added your payment info")

        except (stripe.error.CardError, stripe.error.InvalidRequestError) as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err  = body['error']

            print "Status is: %s" % e.http_status
            print "Type is: %s" % err['type']
            print "Message is: %s" % err['message']

            messages.error(self.request, err['message'])
            return super(DesignerPaymentInfoView, self).form_invalid(form)


        return super(DesignerPaymentInfoView, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Error occurred while processing card information.")
        return super(DesignerPaymentInfoView, self).form_invalid(form)


def register(request,type=None):
    if request.method == 'POST':
        form = TinvilleUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = False  # Need this since oscar defaults it to True
            user.save()
            user.generate_activation_information()
            user.send_confirmation_email(request.get_host(), request.scheme)  # Kind of a hack to get the base URL. Jon M TODO

            # Create a Partner model if this is a designer
            if user.is_seller:
                user.generate_access_code()
                partner = Partner(name=user.email, code=user.slug)
                partner.save()
                partner.users.add(user)

            # Can't do super() here because it would save the instance again
            msg = """An e-mail has been sent to %s. Please check your mail and click on the confirmation link in the
                message to complete your registration. If the e-mail address provided is incorrect, contact Tinville
                customer support to correct the address.""" % user.email
            messages.success(request, msg)
            return HttpResponseRedirect(form.cleaned_data['redirect_url'])
    else:

        form = TinvilleUserCreationForm(initial=
                                        {
                                            'email': request.GET.get('email', ''),
                                            'redirect_url': request.GET.get('next', reverse('home'))
                                        },
                                        host=request.get_host())


    if type is None or type == "customer":
        customer = True
    else:
        customer = False

    c = {
        'form': form,
        'customer': customer,
    }
    return render(request, 'register.html', c)


def activation(request, **kwargs):
    if request.method == 'GET':

        user = get_object_or_404(TinvilleUser, activation_key=kwargs['activation_key'])
        if user.is_active or (request.user.is_authenticated() and request.user.email == user.email):
            messages.warning(request,
                             "Your account already exists and is activated. There is no need to activate again.")
        else:
          #  return super(ActivationView, self).get_redirect_url(*args, **kwargs)
        # introduce again to enforce expiring activation Jon M TODO
        # if user.key_expires < datetime.datetime.utcnow().replace(tzinfo=utc):
        #     messages.error(self.request,
        #                      """Your have exceeded the time period for activation.
        #                      Please contact Tinville customer support so that your account may be activated.""")
        #     return context
            user.is_active = True
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            data = auth_login(request, user)

            if(user.is_seller):
                return redirect('dashboard:index')
            else:
                return activation_redirectUrl(reverse('home'))

    homeUrl = reverse('home')
    return HttpResponseRedirect(homeUrl)

def activation_redirectUrl(url):
    loginResponse = HttpResponseRedirect(url)
    logged_in = True
    loginResponseBody = JsonResponse({'logged_in': logged_in})
    loginResponse.content = loginResponseBody.content
    return loginResponse

@csrf_exempt
def ajax_login(request, *args, **kwargs):
    ud_dict = {'username':str(request.POST['username']).lower()}
    ud_dict['username'] = ud_dict['username'].strip()

    request.POST = request.POST.copy()
    request.POST.update(ud_dict)

    form = LoginForm(request=request, data=request.POST)
    logged_in = False
    data = {}

    if request.is_ajax() and form.is_valid():

        data = login(request, form)
        logged_in = True
        return HttpResponse(json.dumps({'logged_in': logged_in}, {'errors': form.errors}), content_type='application/json')

    return HttpResponseBadRequest(json.dumps(form.errors), content_type="application/json")

def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

def load_user_notifications_count(request):
    if(not request.user.is_anonymous() and request.user.is_seller):
        dashboard_notifications = get_dashboard_notifications(request, queryset_orders_for_user(request.user))
        return HttpResponse(json.dumps({'dashboard_notifications_count': dashboard_notifications["count"]}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'dashboard_notifications_count': 0}), content_type='application/json')


def load_user_info(request):
    user_info = {}
    if not request.user.is_anonymous():
        user_info['username'] = request.user.email
        user_info['is_seller'] = False
        user_info['is_staff'] = request.user.is_staff
        if request.user.is_seller:
            user_info['is_seller'] = True
            user_info['shop_slug'] = Shop.objects.get(user=request.user).slug
    return HttpResponse(json.dumps(user_info), content_type='application/json')


class BetaAccessView(FormView):
    template_name = 'beta_access.html'
    form_class = BetaAccessForm
    access_code = None

    def get_context_data(self, **kwargs):
        context = super(BetaAccessView, self).get_context_data(**kwargs)
        context['shop'] = self.request.GET.get('shop', reverse('home'))
        return context

    def get_success_url(self):
        shop = self.request.POST.get('shop',None)
        if shop:
            return reverse('designer_shop.views.shopper', kwargs = {'slug': shop})
        else :
            return reverse(reverse(''))

    def form_valid(self, form):
        form.cleaned_data['access_code']
        self.access_code = form.cleaned_data['access_code']
        return super(BetaAccessView,self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        response = super(BetaAccessView, self).dispatch(request, *args, **kwargs)
        if self.access_code is not None:
            response.set_cookie(key='beta_access',value = self.access_code, max_age = 365 * 24 * 60 * 60)#set cookie here
        return response
