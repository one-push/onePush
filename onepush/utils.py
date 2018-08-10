#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: utils.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 06/08/2018 16:50
"""
import json
from hashlib import md5
from blog.models import Picture
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from rest_framework.response import Response
from datetime import datetime
DAY_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
INPUT_IMG_SINGLE = 'Filedata'
USE_ALIYUN_OSS = True


def format_datetime(dt):
    """
    Args:
        dt:
    Returns:
    """
    return dt.strftime(DATETIME_FORMAT)


def upload_file(in_file, upload_dir, is_bin=False, name=None):
    if is_bin:
        filename = '{}/{}.jpg'.format(upload_dir, name)
    else:
        filename = '{}/{}.jpg'.format(upload_dir, md5(in_file.read()).hexdigest())

    avatar_path = default_storage.save(filename, in_file)
    return avatar_path


# @login_required()
def image_upload(request):
    in_file = request.FILES.get('file').file
    upload_dir = request.GET.get('dir', 'upload')
    url = upload_file(in_file, upload_dir)

    pic = Picture(url=url)
    pic.save()
    resp = {'status': 'success', 'id': pic.id, 'url': url}
    response = HttpResponse(json.dumps(resp), content_type='application/json; charset=utf-8', status=200)
    return response


class DisableCSRF(object):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
