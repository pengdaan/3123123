#!/bin/sh
# start nginx
nginx -c /etc/nginx/nginx.conf
# start Luna
# gunicorn --workers=4 --bind=0.0.0.0:5000 wsgi:app
# 新增ws后启动方式[workers 只能设置1个，不然ws会报错。]
gunicorn --worker-class=gevent --threads=10 -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -b 0.0.0.0:5000 wsgi:app –preload &
# 开启ssh
/usr/sbin/sshd -D
