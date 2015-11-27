"""
 Developer views
 (c) 2015 - Mark Scrimshire - @ekivemark
"""
__author__ = 'Mark Scrimshire:@ekivemark'

# DONE Activate Account
# DONE: accounts/profile Landing Page.
import ast
import json

from collections import OrderedDict
from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth import (login as django_login,
                                 authenticate,
                                 logout as django_logout)
from django.views.generic.detail import DetailView

from accounts.admin import UserCreationForm
from accounts.decorators import (session_master,
                                 session_master_required)
from accounts.forms.authenticate import AuthenticationForm
from accounts.forms.register import RegistrationForm
from accounts.models import (Crosswalk)
from accounts.utils import (cell_email,
                            send_activity_message)

from apps.bluebutton.cms_parser_utilities import string_to_ordereddict

from appmgmt.models import Organization


def login(request):
    """
    Login view

    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['email'],
                                password=request.POST['password'])
            if user is not None:
                if settings.DEBUG:
                    print("User is not Empty!")
                if user.is_active:
                    django_login(request, user)
                    return redirect('/')
    else:
        form = AuthenticationForm()
    return render_to_response('registration/login.html', {
        'form': form,
    }, context_instance=RequestContext(request))


def register(request):
    """
    User registration view.
    """

    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse_lazy('home'))
    else:
        form = RegistrationForm()
    context = {'form': form}

    return render_to_response('register.html',
                              context_instance=RequestContext(request,
                                                              context,))


def logout(request):
    """
    Log out view
    """
    # DONE: Change redirection based on whether subacc or user
    if 'auth_device' in request.session:
        mode = "subacc"
    else:
        mode = "user"

    django_logout(request)
    if mode == "subacc":
        return redirect(reverse_lazy('api:home'))
    return redirect(reverse_lazy('home'))


def home_index(request):
    # Show Home Page

    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print(settings.APPLICATION_TITLE, "in accounts.views.other.home_index")

    context = {}
    return render_to_response('index.html',
                              RequestContext(request, context, ))


def about(request):
    # Show About Page

    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print(settings.APPLICATION_TITLE, "in accounts.views.other.about")

    context = {}
    return render_to_response('about.html',
                              RequestContext(request, context, ))


def agree_to_terms(request):
    # Agree to Terms
    # Register for account

    if settings.DEBUG:
        print(settings.APPLICATION_TITLE,
              "in accounts.views.agree_to_terms")

    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse_lazy('home'))
    else:
        form = UserCreationForm()

    context = {'form': form, }
    #   return render_to_response('developer/agree_to_terms.html', RequestContext(request, context,))
    return render_to_response(reverse_lazy('accounts:register'),
                              RequestContext(request, context, ))

@session_master
@login_required
def manage_account(request):
    # Manage Accounts entry page

    # DONE: Remove api.data.gov signup widget in manage_account.html

    if settings.DEBUG:
        print(settings.APPLICATION_TITLE,
              "in accounts.views.manage_account")
    user = request.user
    mfa_address = cell_email(user.mobile, user.carrier)
    try:
        org = Organization.objects.filter(owner=user)
    except Organization.DoesNotExist:
        org = {}

    if settings.DEBUG:
        print("Organization", org)

    context = {"user": user,
               "org": org,
               "mfa_address": mfa_address,
               }

    return render_to_response('accounts/manage_account.html',
                              RequestContext(request, context, ))


# DONE: Convert url to lowercase
# DONE: Add view to accounts/urls.py.py
