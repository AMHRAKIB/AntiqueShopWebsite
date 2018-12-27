import re

from django.http import Http404
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
# Create your views here.
from django.contrib.auth import login, logout, authenticate
from .form import LoginForm, RegistrationForm
from .models import EmailConfirmed


def logout_view(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return HttpResponseRedirect('%s' % (reverse("auth_login")))


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, "Successfully Logged in. Welcome Back")
        return HttpResponseRedirect("/")
        # user.emailconfirmed.activate_user_email()
    context = {
        "form": form
    }
    return render(request, "form.html", context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        print("is valid")
        new_user = form.save(commit=False)
        # new_user.first_name = "Justin"
        new_user.save()
        messages.success(request, "Successfully Registered. Please Cunfirm your Email now")
        return HttpResponseRedirect("/")
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']
        # user = authenticate(username=username, password=password)
        # login(request,user)
    context = {
        "form": form
    }
    return render(request, "form.html", context)


SHA1_RE = re.compile('^[a-f0-9]{40}$')


def activation_view(request, activation_key):
    if SHA1_RE.search(activation_key):
        print("Activation Real")
        try:
            instance = EmailConfirmed.objects.get(activation_key=activation_key)
        except EmailConfirmed.DoesNotExist:
            instance = None
            raise Http404
        if instance is not None and not instance.confirmed:
            page_message = "User has been confirmed"
            instance.confirmed = True
            instance.activation_key = "Confirmed"
            instance.save()
            messages.success(request, "Successfully Confirmed")
        elif instance is not None and instance.confirmed:
            page_message = "Already Confirmed "
            messages.success(request, "Already Confirmed")
        else:
            page_message = ""
        context = {
            "page_message": page_message
        }
        return render(request, "accounts/activation_complete.html", context)
    else:
        return HttpResponseRedirect("/")
