#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: views.py.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 16/08/2018 16:42
"""


from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from blog.models import BlogRelationUser


@api_view(['POST'])
def create_favorite(request):
    """

    :param request:
    :return:
    """
    params = request.POST.dict()
    blog_id = params.get('blog_id')

    if not blog_id:
        return Response()

    data = dict(user=request.user)
    data['blog_id'] = blog_id

    # 防止重复点击
    ins = BlogRelationUser.objects.filter(**data).first()
    if not ins:
        ins = BlogRelationUser.objects.create(**data)
    return Response(data=dict(id=ins.id))


@api_view(['PUT'])
def dis_favorite(request):
    params = request.POST.dict()
    blog_id = params.get('blog_id')

    if not blog_id:
        return Response()

    data = dict(user=request.user)
    data['blog_id'] = blog_id

    ins = BlogRelationUser.objects.filter(**data).first()
    if ins:
        ins.delete()
    return Response(data=dict(status=True))
