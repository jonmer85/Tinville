from Tinville.Site.forms import TinvilleUserCreationForm
from Tinville.Site.models import TinvilleUser
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect

def home(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))

def register(request):
    return render_to_response("register.html", {}, context_instance=RequestContext(request))
def faq(request):
    return render_to_response("faq.html", {}, context_instance=RequestContext(request))

def register_designer(request):
    if request.method == 'POST':
        form = TinvilleUserCreationForm(request.POST, designer=True)
        if form.is_valid():
            user = form.save()
            form.save_m2m()
            return HttpResponseRedirect("/register_success/%d" % user.pk)
    else:
        form = TinvilleUserCreationForm(designer=True)

    return render_to_response("register_designer.html", {
        'form': form}, context_instance=RequestContext(request))

def register_shopper(request):
    if request.method == 'POST':
        form = TinvilleUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            form.save_m2m()
            return HttpResponseRedirect("/register_success/%d" % user.pk)
    else:
        form = TinvilleUserCreationForm()

    return render_to_response("register_shopper.html", {
        'form': form}, context_instance=RequestContext(request))

def register_success(request, user_id):
    user = get_object_or_404(TinvilleUser, pk=user_id)
    return render_to_response("register_success.html", {"email": user.email}, context_instance=RequestContext(request))

