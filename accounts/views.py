from django.shortcuts import render, HttpResponseRedirect

# Create your views here.
from django.contrib.auth import login, logout, authenticate
from .form import LoginForm, RegistrationForm


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request,user)
    context={
        "form":form
    }
    return render(request, "form.html",context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        print("is valid")
        new_user = form.save(commit=False)
        # new_user.first_name = "Justin"
        new_user.save()
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']
        # user = authenticate(username=username, password=password)
        # login(request,user)
    context={
        "form":form
    }
    return render(request, "form.html",context)