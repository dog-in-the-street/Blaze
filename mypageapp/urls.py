from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings



app_name='mypage'
urlpatterns = [
    path('mypage',mypage,name="mypage"),
    path('mypageBlaze',mypageBlaze,name='mypageBlaze'),
    path('mypagePosts',mypagePosts,name='mypagePosts'),
    path('mypageComments',mypageComments,name='mypageComments'),
    path('go_editNickname',go_editNickname,name='go_editNickname'),
    path('editNickname', editNickname, name='editNickname'),
    path('signout',LogoutView.as_view(),name='signout'),

] +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)