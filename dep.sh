#!/usr/bin/env bash
find . -name \*.pyc -delete
#ps -ef|grep uwsgi|grep -v grep|awk '{print $2}'|xargs kill -9;
ps -ef|grep panoapi|grep -v grep|awk '{print $2}'|xargs kill -9;
#nginx -s reload;
#uwsgi --ini uwsgi.ini &
#redis-server &
#celery -A mysite worker -l info &
uwsgi --ini /panoapi/uwsgi.ini &
