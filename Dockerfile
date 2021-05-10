# 基础镜像
FROM pengdaan/luna-admin:v1
WORKDIR /opt/workspace/Luna/
COPY . .
COPY ./nginx.conf /etc/nginx/nginx.conf
RUN pip3 install --upgrade pip
RUN dos2unix ./start.sh
RUN chmod +x ./start.sh

EXPOSE 8080 8081 22
CMD  ["/bin/bash", "-c", "/opt/workspace/Luna/start.sh"]






