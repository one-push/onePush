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
from account.models import UserFavorites


@api_view(['POST'])
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

