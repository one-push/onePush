#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: views.py.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 07/08/2018 20:37
"""
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from serializer import TradeReplyListSerializer
from serializer import TradeReplyCreateSerializer
from blog.models import TheoryReply
from blog.service import update_score


class TheoryReplyViews(ModelViewSet):

    def get_serializer_class(self):
        return TradeReplyListSerializer

    def list(self, request, *args, **kwargs):

        theory_id = request.GET.get('theory_id')
        if not theory_id:
            return Response(status=400, error=u'说说谁有理不存在')

        self.serializer_class = TradeReplyListSerializer
        self.queryset = TheoryReply.objects.filter(theory_id=theory_id)
        ret = super(TheoryReplyViews, self).list(request)

        context = dict(data=ret.data)
        return HttpResponseRedirect('block/{}'.format(theory_id), context)

    def create(self, request, *args, **kwargs):
        data = request.POST.dict()
        data['user_id'] = request.user.id
        serial = TradeReplyCreateSerializer(data=data)
        if not serial.is_valid():
            return Response(status=400, error=serial.errors)

        ins = serial.save()
        if ins:
            update_score(request.user, 'comments', ins.id)
        return HttpResponseRedirect('/blogs/theory/{}'.format(data.get('theory_id')))


# 点赞
from serializer import TradeLikeCreateSerializer
from serializer import TradeLikeListSerializer
from blog.models import TheoryLike


class TheoryLikeViews(ModelViewSet):

    def get_serializer_class(self):
        return TradeLikeListSerializer

    def list(self, request, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        data = request.POST.dict()
        serial = TradeLikeCreateSerializer(data=data)

        if TheoryLike.objects.filter(theory_id=data.get('theory_id'),
                                     user_id=data.get('user_id')).exists()\
                or not serial.is_valid():
            return HttpResponseRedirect('/blogs/theory/{}'
                                        .format(data.get('theory_id')))

        ins = serial.save()
        if ins:
            update_score(request.user, 'theory_like', ins.id)
        return HttpResponseRedirect('/blogs/theory/{}'
                                    .format(data.get('theory_id')))
