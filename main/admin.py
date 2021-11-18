from django.contrib import admin
from .models import Category, Images, Post
#from .models import Category

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Images)


#admin.site.register(Category)