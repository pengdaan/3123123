# 基础镜像
FROM pengdaan/luna-admin:v1
WORKDIR /opt/workspace/Luna/
COPY . .
RUN pip3 install --upgrade pip
RUN dos2unix ./start.sh
RUN chmod +x ./start.sh

EXPOSE 5000 22
CMD  ["/bin/bash", "-c", "/opt/workspace/Luna/start.sh"]






