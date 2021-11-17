from enum import unique
from typing import Text
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from django.template.defaultfilters import slugify

class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self) :
        return self.category_name    


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    # category = models.CharField(max_length=30, null=True )
    title = models.CharField(max_length=30, null=True)
    text = models.TextField(blank=True)
    # image = models.ImageField(null = True, blank = True )
    updated = models.DateTimeField(auto_now=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)


    def __str__(self) :
        return "text : "+self.text

    # class Meta:
    #     ordering = ['-created']


def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)  


class Images(models.Model):
    
    post = models.ForeignKey(Post, default=None,on_delete=models.CASCADE, related_name="image")
    image = models.ImageField(upload_to=get_image_filename)

    class Meta:
        # 단수
        verbose_name = 'Image'
        # 복수
        verbose_name_plural = 'Images'

    # 이것도 역시 post title로 반환
    def __str__(self):
       return str(self.post)


