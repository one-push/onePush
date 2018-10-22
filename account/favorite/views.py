#!/usr/bin/env python
# encoding: utf-8

"""
  用户之间关注和收藏
  > FileName: views.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 15/08/2018 11:11
"""

from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from account.models import UserFavorites
from account.models import UserBlogFavorites
from blog.models import Blog


@api_view(['POST'])
@login_required()
def create_favorite(request):
    """

    :param request:
    :return:
    """
    params = request.POST.dict()
    action = params.get('action')
    user_id = params.get('user_id')

    if not user_id and not action:
        return Response()

    data = dict(user=request.user)
    if action == 'attention':
        data['attention_id'] = user_id
    elif action == 'favorite':
        data['favorite_id'] = user_id

    # 防止重复点击
    ins = UserFavorites.objects.filter(**data).first()
    if not ins:
        ins = UserFavorites.objects.create(**data)
    return Response(data=dict(id=ins.id))


@api_view(['PUT'])
@login_required()
def dis_favorite(request):
    params = request.POST.dict()
    action = params.get('action')
    user_id = params.get('user_id')

    if not user_id and not action:
        return Response()

    data = dict(user=request.user)
    if action == 'attention':
        data['attention_id'] = user_id
    elif action == 'favorite':
        data['favorite_id'] = user_id

    ins = UserFavorites.objects.filter(**data).first()
    if ins:
        ins.delete()
    return Response(data=dict(status=True))


@api_view(['POST'])
@login_required()
def blog_relation(request):
    """
    收藏/转发博客
    :param request:
    :return:
    """
    params = request.POST.dict()
    blog = Blog.objects.filter(id=params.get('blog_id')).first()
    if not blog or not params.get('type'):
        return Response()

    data = dict(
        user=request.user,
        block='man',
        type=params.get('type'),
        blog=blog,
    )

    ins, is_create = UserBlogFavorites.objects.update_or_create(**data)
    return Response(data=dict(id=ins.id))

