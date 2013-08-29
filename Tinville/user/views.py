import datetime

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from django.core.urlresolvers import reverse

from Tinville.user.forms import TinvilleUserCreationForm
from Tinville.user.models import TinvilleUser


class CreateUserView(CreateView):
    model = TinvilleUser
    form_class = TinvilleUserCreationForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = form.save()
        form.save_m2m()
        user.generate_activation_information()
        user.send_confirmation_email(self.request.get_host())  # Kind of a hack to get the base URL. Jon M TODO
        # Can't do super() here because it would save the instance again
        msg = """An e-mail has been sent to %s. Please check your mail and click on the confirmation link in the
            message to complete your registration. If the e-mail address provided is incorrect, contact Tinville
            customer support to correct the address.""" % user.email
        messages.success(self.request, msg)

        return HttpResponseRedirect(self.success_url)


class CreateDesignerView(CreateUserView):
    template_name = 'register_designer.html'

    def get_form_kwargs(self):
        kwargs = super(CreateDesignerView, self).get_form_kwargs()
        kwargs['designer'] = True
        self.success_url = reverse('create-designer')
        return kwargs



class CreateShopperView(CreateUserView):
    template_name = 'register_shopper.html'

def get_form_kwargs(self):
        # pass "user" keyword argument with the current user to your form
        kwargs = super(CreateDesignerView, self).get_form_kwargs()
        kwargs['designer'] = False
        self.success_url = reverse('create-shopper')
        return kwargs


class ActivationView(TemplateView):
    template_name = "notification.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            messages.warning(self.request,
                             "Your account already exists and activated. There is no need to activate again.")
            return context
        user = get_object_or_404(TinvilleUser, activation_key=kwargs['activation_key'])
        # introduce again to enforce expiring activation Jon M TODO
        # if user.key_expires < datetime.datetime.utcnow().replace(tzinfo=utc):
        #     messages.error(self.request,
        #                      """Your have exceeded the time period for activation.
        #                      Please contact Tinville customer support so that your account may be activated.""")
        #     return context
        user.is_active = True
        user.save()
        messages.success(self.request,
                             """Thank you for completing the registration process. You are now successfully logged into Tinville!""")
        return context

