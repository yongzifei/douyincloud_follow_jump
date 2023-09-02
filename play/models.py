from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import numpy as np


class User(AbstractUser):
    class Meta:
        ordering = ['-date_joined']

    class Gender(models.IntegerChoices):
        Created = 0, _('未知')
        Checked = 1, _('男')
        Used = 2, _('女')

    avatar_url = models.CharField(max_length=200)
    gender = models.IntegerField(choices=Gender.choices, default=0)
    country = models.CharField(max_length=20, blank=True, null=True)
    province = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)

class Video(models.Model):
    douyin_video_id = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=50, blank=True)
    desc = models.CharField(max_length=400, blank=True)
    tags = models.CharField(max_length=100, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(editable=False, default=0)
    poster = models.ImageField(upload_to='videos/%Y/%m/', blank=True)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    poses = models.JSONField(editable=False, help_text='''JSON Format. like {3:[0.3234,-0.1654,0.9987]}''',
                             default=dict)
    play_times = models.IntegerField(default=0)


class Play(models.Model):
    class State(models.IntegerChoices):
        '''
        Created - User buy ticket.
        Checked - When go to dance sence, if ticket in this state, it can be used next time.
        Used - When backend receive first dance motion. If in Used state, the ticket can't use again.
        Ended - When receive last dance motion or Used State Time is expired 300s. this is final state.
        '''
        Created = 0, _('Created')
        Checked = 1, _('Checked')
        Used = 2, _('Used')
        Ended = 3, _('Ended')
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(choices=State.choices)
    state_time = models.DateTimeField(auto_now=True)
    user_frame = models.IntegerField(default=0, help_text='if dancing break, can continue from this frame.')
    points = models.IntegerField(default=0, db_index=True)
    perfect_qty = models.IntegerField(default=0, db_index=True)
    good_qty = models.IntegerField(default=0, db_index=True)
    ok_qty = models.IntegerField(default=0, db_index=True)
    miss_qty = models.IntegerField(default=0, db_index=True)

    def match(self, frame_no, user_poses):
        video_poses = self.video.poses
        frame_no = str(frame_no)
        video_pose_frame = video_poses[frame_no]
        video_pose = []
        for p in video_pose_frame:
            video_pose.append([p[0], p[1]])
        most_similarity = 2.0
        for user_pose in user_poses:
            cosine_similarity = 0
            for position_index in range(13):
                cosine_similarity += 1 - np.dot(user_pose[position_index], video_pose[position_index]) / (
                            np.linalg.norm(user_pose[position_index]) * np.linalg.norm(video_pose[position_index]))
            cosine_similarity /= 13
            # pose_similarity = round(np.std(cosine_similarity),6)
            pose_similarity = cosine_similarity
            most_similarity = pose_similarity if pose_similarity < most_similarity else most_similarity
        # 算分
        GRADE_POINT = dict(perfect=4, good=2, ok=1, miss=0)
        pose_point = 0
        pose_grade = 'miss'
        if most_similarity < 0.001:
            pose_point = GRADE_POINT['perfect']
            pose_grade = 'perfect'
            self.perfect_qty += 1
        elif most_similarity < 0.01:
            pose_point = GRADE_POINT['good']
            pose_grade = 'good'
            self.good_qty += 1
        elif most_similarity < 0.05:
            pose_point = GRADE_POINT['ok']
            pose_grade = 'ok'
            self.ok_qty += 1
        else:
            self.miss_qty += 1

        self.points += pose_point
        self.user_frame = frame_no
        # dance_frames = sorted(dance_poses.keys)
        last_frame_keys = list(video_pose.keys())
        last_frame_key = last_frame_keys[len(last_frame_keys) - 1]
        if frame_no == last_frame_key:
            self.state = Play.State.Ended
        self.save()
        return pose_grade, pose_point, pose_similarity
