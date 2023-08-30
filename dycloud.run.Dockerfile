# python构建的基础镜像
FROM public-cn-beijing.cr.volces.com/public/python:3.9.15
WORKDIR /opt/application
# 拷贝requirements.txt至当前目录下
COPY requirements.txt /opt/application
# 安装依赖
RUN pip install --upgrade pip && pip3 install -r requirements.txt #-i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn/simple
# 使用了mediapipe，默认带的opencv不能在docker里使用，需要替换下
RUN pip3 uninstall -y opencv-contrib-python && pip3 install opencv-contrib-python-headless
# 拷贝项目所有文件至/opt/application
COPY ./ /opt/application
CMD ["python", "manage.py", "runserver", "--noreload", "0.0.0.0:8000"]
