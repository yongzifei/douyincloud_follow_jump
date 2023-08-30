# python构建的基础镜像
FROM public-cn-beijing.cr.volces.com/public/python:3.9.15
# 设置工作目录
WORKDIR /opt/application
# 拷贝requirements.txt至当前目录下
COPY requirements.txt /opt/application
# 安装相关依赖
RUN pip install --upgrade pip && pip install pydevd-pycharm~=232.9559.58 #-i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn/simple
RUN pip3 install -r requirements.txt #-i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn/simple
# 使用了mediapipe，默认带的opencv不能在docker里使用，需要替换下
RUN pip3 uninstall -y opencv-contrib-python && pip3 install opencv-contrib-python-headless
# 拷贝项目所有文件至/opt/application
COPY ./ /opt/application
# 使用sed替换占位符
RUN sed -i "s/# dycloud debug/import pydevd_pycharm;pydevd_pycharm.settrace('192.168.1.18', port=5005, stdoutToServer=True, stderrToServer=True)/g" `grep "# dycloud debug" -rl /opt/application`
CMD ["python", "manage.py", "runserver", "--noreload", "0.0.0.0:8000"]
