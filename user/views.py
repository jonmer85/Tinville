import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from django.contrib.auth.views import login as auth_view_login
from django.contrib.auth.forms import AuthenticationForm
from user.forms import LoginForm
from django.core.urlresolvers import reverse
from django.shortcuts import render


from user.forms import TinvilleShopperCreationForm, TinvilleDesignerCreationForm
from user.models import TinvilleUser


def register(request):

    if request.method == 'POST':
      if 'shopperForm' in request.POST:
        shopperForm = TinvilleShopperCreationForm(request.POST)
        designerForm = TinvilleDesignerCreationForm()
        form = shopperForm
      else:
        designerForm = TinvilleDesignerCreationForm(request.POST)
        shopperForm = TinvilleShopperCreationForm()
        form = designerForm

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
        return HttpResponse(json.dumps({'logged_in': logged_in}, {'errors': form.errors}), mimetype='application/json')

    return HttpResponseBadRequest(json.dumps(form.errors), mimetype="application/json")


