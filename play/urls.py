from django.urls import path

from . import views

app_name = 'play'
urlpatterns = [
    path('check_user', views.check_user, name='check_user'),
    path('register', views.register, name='register'),
    path('detect_poses', views.detect_poses, name='detect_poses'),
]
