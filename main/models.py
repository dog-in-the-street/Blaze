from enum import unique
from typing import Text
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from django.template.defaultfilters import slugify
from accounts.models import BlazeUser
from datetime import datetime, timedelta
from django.utils import timezone


class Category(models.Model):
    category_name = models.CharField(max_length=30)
    
    def __str__(self) :
        return self.category_name    


class Post(models.Model):
    author = models.ForeignKey(BlazeUser, on_delete=models.CASCADE, related_name='user')
    # category = models.CharField(max_length=30, null=True )
    title = models.CharField(max_length=30, null=True)
    text = models.TextField(blank=True)
    # image = models.ImageField(null = True, blank = True )
    # updated = models.DateTimeField(auto_now=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    registered_date = models.DateTimeField( auto_now_add=True , verbose_name='registration time')

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.registered_date

        if time < timedelta(minutes=1):
            return 'just now'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + 'minutes ago'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + 'hours ago'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.registered_date.date()
            return str(time.days) + 'days ago'
        else:
            return False






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


