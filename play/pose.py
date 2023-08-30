# 处理视频获取关键帧骨骼信息

import cv2
import mediapipe as mp
import numpy as np
import json
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def get_pose(video_path):
    time_gap = 3 #每隔几秒取一次
    cap = cv2.VideoCapture(video_path)
    cut_fps = int(cap.get(cv2.CAP_PROP_FPS) * time_gap)   # 帧速率
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 视频文件的总帧数
    duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
        marks = {}
        for f in range(cut_fps, frames, cut_fps):
            cap.set(cv2.CAP_PROP_POS_FRAMES,f) #直接取帧，不用所有帧都过一遍
            time_key = int(f/cut_fps*time_gap)
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            if results.pose_world_landmarks:
                joints = []
                for index, landmark in enumerate(results.pose_world_landmarks.landmark):
                    if index in [0, 11,12,13,14,15,16, 23,24,25,26,27,28]:
                        joint = [round(landmark.x, 4),round(landmark.y, 4), round(landmark.visibility, 4)]
                        joints.append(joint)
                marks[time_key] = joints
        # with open('public/video/video1.json','w') as file:
        #     json.dump(marks, file, separators=(',',':'))

    cap.release()
    return marks, duration