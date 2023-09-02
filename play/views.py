from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .decorators import require_login
from .models import User, Video, Play
from django.core.cache import cache
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import logging
from .pose import get_pose

logger = logging.getLogger('play')

@require_login
@csrf_exempt
def check_profile(req):
    if req.user.first_name and req.user.avatar_url:
        user_profile = dict(nick_name=req.user.first_name, avatar_url=req.user.avatar_url)
        return JsonResponse(dict(code=0, profile=user_profile))
    else:
        return JsonResponse(dict(code=1, msg='用户昵称和头像信息不完整'))

# dycloud debug
@csrf_exempt
@require_login
def update_profile(req):
    req.user.first_name = req.POST.get('nickName')
    req.user.avatar_url = req.POST.get('avatarUrl')
    req.user.gender = int(req.POST.get('gender', 0))
    req.user.country = req.POST.get('country')
    req.user.province = req.POST.get('province')
    req.user.city = req.POST.get('city')
    req.user.save()
    user_profile = dict(nick_name=req.user.first_name, avatar_url=req.user.avatar_url)
    return JsonResponse(dict(code=0, profile=user_profile))

# dycloud debug
@csrf_exempt
@require_login
def detect_poses(req):
    # 暂存视频并提取骨骼
    upload_video = req.FILES.get('video')
    poses, duration = get_pose(upload_video.file.name)
    video = Video(user=req.user, poses=poses, duration=duration)
    video.save()
    # 保存文件并返回成功
    return JsonResponse(dict(code=0, video_id=video.id))
    # if int(duration/3) == len(poses):
    #     video = Video(user=req.user, poses=poses, duration=duration)
    #     video.save()
    #     # 保存文件并返回成功
    #     return JsonResponse(dict(code=0, video_id=video.id))
    # else:
    #     return JsonResponse(dict(code=1, msg='视频中存在无法检测动作的画面'));

@csrf_exempt
@require_login
def update_douyin_video_id(req):
    video_id = req.POST.get('jumpVideoId')
    douyin_video_id = req.POST.get('douyinVideoId')


def get_my_videos(req):
    page = req.GET.get('page', 0),
