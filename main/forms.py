from django import forms
from django.db import models
from .models import Images, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','text','category',)

        widgets = {
                'title': forms.TextInput(attrs={'placeholder': 'Title'}),
                'text': forms.Textarea(
                attrs={'placeholder':'Write something!'}),
}

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('image',)
        labels = {
            'image': ('Image'),
        }