# 基础镜像
# FROM pengdaan/luna-web-admin-base:v1.0
FROM python:3.9
ENV LANG C.UTF-8
ENV TZ=Asia/Shanghai


# 默认使用上海时区 + 阿里源
RUN echo "deb https://mirrors.aliyun.com/debian/ buster main non-free contrib" > /etc/apt/sources.list && \
    apt-get clean && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    sudo \
    nginx \
    dos2unix \
    tzdata && \
    dpkg-reconfigure --frontend noninteractive tzdata \
    && apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 3B4FE6ACC0B21F32 \
    && apt-get --purge remove openssh-client -y \
    && apt-get install openssh-server -y \
    && mkdir -p /var/run/sshd \
    && apt-get install net-tools -y \
    && echo "PermitRootLogin yes" >> /etc/ssh/sshd_config \
    && echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config \
    && echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config \
    && echo "root:root" | chpasswd \
    && ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
WORKDIR /opt/workspace/Luna/

COPY . .
COPY ./nginx.conf /etc/nginx/nginx.conf
RUN pip3 install --upgrade pip
RUN pip install -r ./requirements.txt -i \
    https://pypi.tuna.tsinghua.edu.cn/simple/ \
    --default-timeout=100
# RUN pip install -r ./requirements.txt 
RUN dos2unix ./start.sh
RUN chmod +x ./start.sh

EXPOSE 5000 5001 22
CMD  ["/bin/bash", "-c", "/opt/workspace/Luna/start.sh"]






