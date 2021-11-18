from django import forms
from django.contrib import auth
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import BlazeUser, UserManager
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    class Meta:
        model = BlazeUser 
        fields = ['email', 'nickname', 'password1', 'password2', 'country']

    def clean(self):
        nickname = self.cleaned_data.get('nickname')
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        country = self.cleaned_data.get('country')

        try:
            BlazeUser.objects.get(email=email)
            raise forms.ValidationError('BLAZE : "This email already exists. Please try other emails"')
        except BlazeUser.DoesNotExist:
            pass

        if email is None:
            raise forms.ValidationError('BLAZE : "Please enter the correct email"')

        if len(nickname)==1 or len(nickname)>=8:
            raise forms.ValidationError('BLAZE : "Nicknames are 2 or more letters and 10 or less letters"')

        try:
            BlazeUser.objects.get(nickname=nickname)
            raise forms.ValidationError('BLAZE : "This nickname already exists. Please try other nicknames"')
        except BlazeUser.DoesNotExist:
            pass
        return self.cleaned_data