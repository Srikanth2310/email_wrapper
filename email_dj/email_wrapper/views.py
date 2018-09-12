from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm #use the native Django form
from django.contrib.auth import login, logout

# Create your views here.

def login_view(request):
    return render(request,"login.html",{})

def after_login_view(request):
    return render(request,"after_login.html",{})
