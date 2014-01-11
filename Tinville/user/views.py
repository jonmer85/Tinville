import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from django.contrib.auth.views import login as auth_view_login
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.shortcuts import render


from Tinville.user.forms import TinvilleShopperCreationForm, TinvilleDesignerCreationForm
from Tinville.user.models import TinvilleUser

def register(request):
    if request.method == 'POST':
      if 'shopperForm' in request.POST:
        form = TinvilleShopperCreationForm(request.POST)
      else:
        form = TinvilleDesignerCreationForm(request.POST)

      if form.is_valid():
        #create initial entry for User object
        user = form.save()
        user.generate_activation_information()
        user.send_confirmation_email(request.get_host())  # Kind of a hack to get the base URL. Jon M TODO
        # Can't do super() here because it would save the instance again
        msg = """An e-mail has been sent to %s. Please check your mail and click on the confirmation link in the
            message to complete your registration. If the e-mail address provided is incorrect, contact Tinville
            customer support to correct the address.""" % user.email
        messages.success(request, msg)
        success_url = reverse('notifications')
        return HttpResponseRedirect(success_url)

    else:
      shopperForm = TinvilleShopperCreationForm()
      designerForm = TinvilleDesignerCreationForm()
    c = {
      'shopperForm':shopperForm,
      'designerForm':designerForm,
    }
    return render(request, 'register.html', c)


class CreateUserView(CreateView):
    model = TinvilleUser
    template_name = 'register.html'
    form_class = TinvilleShopperCreationForm
    second_form_class = TinvilleDesignerCreationForm

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


    def get_context_data(self, **kwargs):
        context = super(CreateUserView, self).get_context_data(**kwargs)
        if 'shopperForm' not in context:
            context['shopperForm'] = self.form_class(request=self.request, prefix="shopperForm")
        if 'designerForm' not in context:
            context['designerForm'] = self.second_form_class(request=self.request, prefix="designerForm")
        return context

    # def get_object(self):
    #     return get_object_or_404(TinvilleUser, pk=self.request.session['value_here'])

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):

        if 'shopperForm' in request.POST:
            form_class = self.get_form_class()
            form_name = 'shopperForm'
            form = self.form_class(request.POST)
        else:
            form_class = self.second_form_class
            form_name = 'designerForm'
            form = self.form_class(request.POST)


        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})






class ActivationView(TemplateView):
    template_name = "notification.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user = get_object_or_404(TinvilleUser, activation_key=kwargs['activation_key'])
        if user.is_active or (self.request.user.is_authenticated() and self.request.user.email == user.email):
            messages.warning(self.request,
                             "Your account already exists and is activated. There is no need to activate again.")
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

