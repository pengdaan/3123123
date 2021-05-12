#!/bin/sh
# start nginx
nginx -c /etc/nginx/nginx.conf
# start Luna
# gunicorn --workers=4 --bind=0.0.0.0:5000 wsgi:app
# 50s 超时时常 协程启动
# gunicorn --worker-class=gevent --workers=1 -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -b 0.0.0.0:5000 wsgi:app –preload -t 50 &
# 多线程启动
gunicorn --workers=1 --threads=17 -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -b 0.0.0.0:5000 wsgi:app –preload -t 50 &
# 开启ssh
/usr/sbin/sshd -D
