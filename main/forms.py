from django import forms
from django.db import models
from .models import Images, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','text','category',)

        # error_messages = {
        #     'Title' : {
        #         'max_length': _("wpahrdms")
        #     }
        # }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('image',)
        labels = {
            'image': ('Image'),
        }