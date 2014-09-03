import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.views import login as auth_view_login
from user.forms import LoginForm
from django.core.urlresolvers import reverse
from django.shortcuts import render

from user.forms import TinvilleUserCreationForm
from user.models import TinvilleUser
from basket.views import load_cart

def register(request):
    if request.method == 'POST':
        form = TinvilleUserCreationForm(request.POST)

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
            success_url = reverse('home')
            return HttpResponseRedirect(success_url)
    else:
        form = TinvilleUserCreationForm()
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
        load_cart(request)
        logged_in = True
        return HttpResponse(json.dumps({'logged_in': logged_in}, {'errors': form.errors}), mimetype='application/json')

    return HttpResponseBadRequest(json.dumps(form.errors), mimetype="application/json")


