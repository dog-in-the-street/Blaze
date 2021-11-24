from django import forms
from django.db import models
from .models import *

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


class CommentForm(forms.ModelForm):
  
    class Meta:
        model = Comment
        
        fields = ('content',)
        labels = {
            'content': (''),
        }
        widgets = {
                
                'content': forms.Textarea(
                attrs={'placeholder':'Comment Here'}),
             }




class RecommentForm(forms.ModelForm):

   class Meta:
        model = Recomment
        fields = ('content',)
        labels = {
            'content': (''),
        }
        widgets = {
                
                'content': forms.Textarea(
                attrs={'placeholder':'ReComment Here'}),
             }


     

# Message updated 날짜 형식
