from Tinville.Site.forms import TinvilleDesignerCreationForm
from Tinville.Site.models import FashionStyles
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

def home(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))

def register(request):
    return render_to_response("register.html", {}, context_instance=RequestContext(request))

def register_designer(request):
    if request.method == 'POST':
        form = TinvilleDesignerCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = TinvilleDesignerCreationForm()
        styles = FashionStyles.objects.all()

    return render_to_response("register_designer.html", {
        'form': form, 'styles': styles}, context_instance=RequestContext(request))
