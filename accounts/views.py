from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .forms import SignUpForm
from .models import *
# from django.contrib.auth import get_user_model
# User = get_user_model()

def signup(request):
    regi_form = SignUpForm()
    if request.method == "POST":
        regi_form = SignUpForm(request.POST)
        if regi_form.is_valid():
            user = regi_form.save()
            auth_login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('main')
        else :
            form = SignUpForm()
            print("error")
    return render(request,'signup.html',{'regi_form':regi_form})

