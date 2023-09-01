FROM public-cn-beijing.cr.volces.com/public/base:python-3.10.6

MAINTAINER douyincloud

COPY ./ /opt/application

WORKDIR /opt/application

RUN pip3 install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn/simple
# 使用了mediapipe，默认带的opencv不能在docker里使用，需要替换下
RUN pip3 uninstall -y opencv-contrib-python && pip3 install opencv-contrib-python-headless -i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn/simple
RUN chmod 777 run.sh

ENTRYPOINT ["/bin/sh", "/opt/application/run.sh"]
EXPOSE 8000
