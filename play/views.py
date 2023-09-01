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

@csrf_exempt
@require_login
def check_user(req):
    return JsonResponse(dict(errno=0, data=req.user))

@csrf_exempt
def register(req):
    openid = req.POST.get('openid')
    nick_name = req.POST.get('nick_name')
    avatar_url = req.POST.get('avatar_url')
    user = User(
        username=openid,
        first_name=nick_name,
        avatar_url=avatar_url
    )
    user.save()

# dycloud debug
@csrf_exempt
@require_login
def detect_poses(req):
    # 暂存视频并提取骨骼
    upload_video = req.FILES.get('video')
    poses, duration = get_pose(upload_video.file.name)
    if int(duration/3) == len(poses):
        # 保存文件并返回成功
        return JsonResponse({
            'err_no': 0,
            'data': poses
        })
    else:
        return JsonResponse({
        'err_no': 1,
        'err_msg': '视频中存在无法检测动作的画面',
    })

def upload_video_info(req):
    video_id = req.POST.get('video_id')
    douyin_video_id = req.POST.get('douyin_video_id')
