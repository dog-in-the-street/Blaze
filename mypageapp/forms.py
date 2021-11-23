from django import forms
from django.db import models
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

class CheckPasswordForm(forms.Form):
    password = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={'class': 'form-control',}), 
    )
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password
        
        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', "The password doesn't match.")
