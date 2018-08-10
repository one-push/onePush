#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: views.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 2018/8/1 20:13
"""


from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from blog.serializer import TheoryListSerializer
from blog.serializer import TheoryCreateSerializer
from blog.serializer import TheoryDetailSerializer
from blog.models import Theory, Trade
from blog.service import created_code


class TheoryViews(ModelViewSet):

    def get_serializer_class(self):
        return TheoryListSerializer

    def list(self, request, *args, **kwargs):

        params = request.GET.dict()
        # params['user_id'] = request.user.id
        params['is_delete'] = False

        self.serializer_class = TheoryListSerializer
        self.queryset = Theory.objects.filter(**params)
        ret = super(TheoryViews, self).list(request)

        context = dict(data=ret.data.get('results', []))
        return render(request, 'comment.html', context)

    def create(self, request, *args, **kwargs):
        data = request.POST.dict()
        trade_id = data.pop('trade_id')
        data['user_id'] = request.user.id
        data['code'] = created_code()
        self.serializer_class = TheoryCreateSerializer
        serial = self.serializer_class(data=data)
        if not serial.is_valid():
            return Response(error=serial.errors)

        ins = serial.save()
        if not ins:
            return HttpResponseRedirect('theory')
        else:
            return HttpResponseRedirect('trade/{}'.format(trade_id))

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        blog = Theory.objects.filter(id=pk).first()
        serial = TheoryDetailSerializer(blog)
        data = serial.data
        context = dict(data=data)
        return render(request, 'theory-info.html', context)
