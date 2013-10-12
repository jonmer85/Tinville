import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from django.contrib.auth.views import login as auth_view_login
from django.contrib.auth.forms import AuthenticationForm
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
        self.success_url = reverse('notifications')
        return HttpResponseRedirect(self.success_url)



class CreateDesignerView(CreateUserView):
    template_name = 'register_designer.html'

    def get_form_kwargs(self):
        kwargs = super(CreateDesignerView, self).get_form_kwargs()
        kwargs['designer'] = True
        return kwargs



class CreateShopperView(CreateUserView):
    template_name = 'register_shopper.html'

    def get_form_kwargs(self):
        # pass "user" keyword argument with the current user to your form
        kwargs = super(CreateShopperView, self).get_form_kwargs()
        kwargs['designer'] = False
        return kwargs


class ActivationView(TemplateView):
    template_name = "notification.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user = get_object_or_404(TinvilleUser, activation_key=kwargs['activation_key'])
        if self.request.user.is_authenticated() and self.request.user.email == user.email:
            messages.warning(self.request,
                             "Your account already exists and activated. There is no need to activate again.")
            return self.render_to_response(context)
        # introduce again to enforce expiring activation Jon M TODO
        # if user.key_expires < datetime.datetime.utcnow().replace(tzinfo=utc):
        #     messages.error(self.request,
        #                      """Your have exceeded the time period for activation.
        #                      Please contact Tinville customer support so that your account may be activated.""")
        #     return context
        user.is_active = True
        user.save()
        messages.success(self.request,
                             """Thank you for completing the registration process! You may now sign in to Tinville
                             with your new user account using the link at the upper right hand corner.""")
        return self.render_to_response(context)


def login(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
    return auth_view_login(request, *args, **kwargs)


def ajax_login(request, *args, **kwargs):
    form = AuthenticationForm(data=request.POST)
    logged_in = False
    data = {}

    if request.is_ajax() and form.is_valid():
        data = auth_view_login(request, form)
        logged_in = True
        return HttpResponse(json.dumps({'logged_in': logged_in}, {'errors': form.errors}), mimetype='application/json')

    return HttpResponseBadRequest(json.dumps(form.errors), mimetype="application/json")

