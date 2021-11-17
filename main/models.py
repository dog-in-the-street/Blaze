from enum import unique
from typing import Text
from django.contrib.auth.models import User
from django.db import models

from accounts.models import BlazeUser

# Create your models here.

# class Category(models.Model):
#     category_name = models.CharField(max_length=30)
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True )

#     class Meta:
#         unique_together = ["category_name"]

#     def __str__(self) :
#         return self.category_name    


class Post(models.Model):
    author = models.ForeignKey(BlazeUser, on_delete=models.CASCADE, related_name='user')
    # category = models.CharField(max_length=30, null=True )
    title = models.CharField(max_length=30, null=True)
    text = models.TextField(blank=True)
    image = models.ImageField(null = True, blank = True )
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self) :
        return "text : "+self.text

    # class Meta:
    #     ordering = ['-created']
