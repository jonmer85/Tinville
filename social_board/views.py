import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import login as auth_view_login
from django.contrib.auth import login as auth_login
from django.views.generic import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect
from oscar.core.loading import get_model
import stripe

from custom_oscar.apps.dashboard.orders.views import queryset_orders_for_user
from user.forms import TinvilleUserCreationForm, LoginForm, PaymentInfoFormWithFullName, BetaAccessForm
from user.models import TinvilleUser
from custom_oscar.apps.dashboard.views import get_dashboard_notifications


