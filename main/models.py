from enum import unique
from typing import Text
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from django.template.defaultfilters import slugify
from accounts.models import BlazeUser


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
    updated = models.DateTimeField(auto_now=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)


    def __str__(self) :
        return self.text

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


class Comment(models.Model):
  user = models.ForeignKey(BlazeUser,on_delete=models.CASCADE, related_name='comment_user')
  post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="comment")
  content = models.TextField()
  # 최초 생성 날짜만 보여줌
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return str(self.user)



    
class Recomment(models.Model):
    user = models.ForeignKey(BlazeUser,on_delete=models.CASCADE,related_name="recom_user")
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="recom_post")
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="recomment")
    content = models.TextField('recomment')