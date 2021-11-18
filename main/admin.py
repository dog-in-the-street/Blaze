from django.contrib import admin
from .models import Category, Post, Message
#from .models import Category

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Message)


#admin.site.register(Category)