import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import login as auth_view_login
from django.views.generic import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render
from oscar.core.loading import get_model
import stripe

from user.forms import TinvilleUserCreationForm, LoginForm, PaymentInfoFormWithFullName
from user.models import TinvilleUser

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

        try:
            # Create a Recipient
            stripe.api_key = settings.STRIPE_SECRET_KEY
            recipient = stripe.Recipient.create(
              name=full_legal_name,
              type="individual",
              email=self.request.user.email,
              card=token)

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


        return super(DesignerPaymentInfoView, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Error occurred while processing card information.")
        return super(DesignerPaymentInfoView, self).form_invalid(form)


def register(request):
    f = 1/0
    if request.method == 'POST':
        form = TinvilleUserCreationForm(request.POST)

        if form.is_valid():
            #create initial entry for User object
            user = form.save()
            user.generate_activation_information()
            user.send_confirmation_email(request.get_host())  # Kind of a hack to get the base URL. Jon M TODO

            # Create a Partner model if this is a designer
            if user.is_seller:
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
    c = {
        'form': form,
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
            messages.success(request,
                             """Thank you for completing the registration process! You may now sign in to Tinville
                             with your new user account using the link at the upper right hand corner.""")
    success_url = reverse('home')
    return HttpResponseRedirect(success_url)


def ajax_login(request, *args, **kwargs):
    ud_dict = {'username':str(request.POST['username']).lower()}

    request.POST = request.POST.copy()
    request.POST.update(ud_dict)

    form = LoginForm(data=request.POST)
    logged_in = False
    data = {}

    if request.is_ajax() and form.is_valid():

        data = auth_view_login(request, form)
        logged_in = True
        return HttpResponse(json.dumps({'logged_in': logged_in}, {'errors': form.errors}), content_type='application/json')

    return HttpResponseBadRequest(json.dumps(form.errors), content_type="application/json")


