from django.urls import path

from . import views

app_name = 'play'
urlpatterns = [
    path('check_profile', views.check_profile, name='check_profile'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('detect_poses', views.detect_poses, name='detect_poses'),
    path('update_douyin_video_id', views.update_douyin_video_id, name="update_douyin_video_id")
]
