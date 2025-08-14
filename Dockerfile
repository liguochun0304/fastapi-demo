FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/pytorch/pytorch:2.4.1-cuda11.8-cudnn9-devel


LABEL author="liguochun"
# 使用上海时区
ENV TZ=Asia/Shanghai

# 拷贝依赖包文件
COPY requirements.txt /tmp/requirements.txt


# 基础环境安装
# 基础环境安装
RUN \
    set -ex && \
    chmod 777 /tmp && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse" > /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse">> /etc/apt/sources.list  && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse">> /etc/apt/sources.list  && \
    echo "deb http://security.ubuntu.com/ubuntu/ jammy-security main restricted universe multiverse">> /etc/apt/sources.list  && \
    \
    apt-get update && \
    apt-get install -y vim wget gcc python3-dev python3-pip libgl1-mesa-glx libglib2.0-0 libgomp1 --no-install-recommends && \
    \
    pip install uv -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    uv pip install --system -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    uv pip install --system supervisor uwsgi -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    \
    echo_supervisord_conf > /etc/supervisord.conf && \
    echo "[include]" >> /etc/supervisord.conf && \
    echo "files = /etc/supervisord.d/*.ini" >> /etc/supervisord.conf && \
    \
    apt-get purge -y gcc  python3-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf ~/.cache/pip/*

RUN apt-get update && \
apt-get install -y language-pack-zh-hans  && \
locale-gen zh_CN.UTF-8 && update-locale LANG=zh_CN.UTF-8 LC_ALL=zh_CN.UTF-8

# 工作空间
WORKDIR /work/src

# 添加pythonpath
ENV PYTHONPATH=/work/src

# 程序部署
COPY conf/uwsgi.ini /work/conf/uwsgi.ini
COPY conf/supervisor.ini /etc/supervisord.d/supervisor.ini



# 程序部署
COPY conf/uwsgi.ini /work/conf/uwsgi.ini
COPY conf/supervisor.ini /etc/supervisord.d/supervisor.ini
COPY src /work/src
