from django.contrib import admin
from django.urls import path, include
from .views import signup
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('signup/',signup, name='signup'),
    path('signin/',LoginView.as_view(), name='signin'),
    path('signout/',LogoutView.as_view(),name='signout'),
    path('', include('social_django.urls', namespace='social')),
    # path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
]