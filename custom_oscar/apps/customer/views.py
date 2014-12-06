import logging
import six

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.db.models import get_model
from django.utils.translation import ugettext as _

from oscar.core.loading import get_class, get_classes
from oscar.core import prices

from oscar.apps.customer.views import AddressUpdateView as CoreAddressUpdateView, UserAddressForm

# Create your views here.
from oscar_stripe.facade import Facade

class AddressUpdateView(CoreAddressUpdateView):
    template_name = 'edit_address.html'
    form_class = UserAddressForm