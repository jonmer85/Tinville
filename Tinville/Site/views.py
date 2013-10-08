from django.shortcuts import render_to_response
from django.template import RequestContext

def faq(request):
    return render_to_response("infopages/faq.html", {}, context_instance=RequestContext(request))
def about(request):
    return render_to_response("infopages/about.html", {}, context_instance=RequestContext(request))
def policies(request):
    return render_to_response("infopages/policies.html", {}, context_instance=RequestContext(request))
def terms(request):
    return render_to_response("infopages/terms.html", {}, context_instance=RequestContext(request))
