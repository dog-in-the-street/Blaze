from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .models import *
# from django.contrib.auth import get_user_model
# User = get_user_model()

def signup(request):
    regi_form = SignUpForm()
    if request.method == "POST":
        regi_form = SignUpForm(request.POST)
        if regi_form.is_valid():
            regi_form.save()
            return redirect('index')
    else :
        form = SignUpForm()
        print("error")
    return render(request,'signup.html',{'regi_form':regi_form})

