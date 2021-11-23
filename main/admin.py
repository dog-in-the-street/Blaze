from django.contrib import admin
from .models import *
#from .models import Category

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Recomment)
admin.site.register(Category)
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(Images)
admin.site.register(ChatRoomUser)


#admin.site.register(Category)