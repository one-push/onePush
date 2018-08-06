#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: views.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 06/08/2018 19:22
"""

from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from blog.serializer import TradeListSerializer
from blog.serializer import TradeCreateSerializer
from blog.serializer import TradeDetailSerializer
from blog.models import Trade


class TradeViews(ModelViewSet):

    def get_serializer_class(self):
        return TradeListSerializer

    def list(self, request, *args, **kwargs):

        params = request.GET.dict()
        params['user_id'] = request.user.id

        args = dict(
            user_id=params.get('user_id'),
            is_delete=False,
        )

        self.serializer_class = TradeListSerializer
        self.queryset = Trade.objects.filter(**args)
        ret = super(TradeViews, self).list(request)

        context = dict(data=ret.data)
        return render(request, 'theory.html', context)

    def create(self, request, *args, **kwargs):
        data = request.POST.dict()
        if data.get('method') == 'put':
            return self.update(request, *args, **kwargs)

        buyer = User.objects.filter(username=data.get('buyer')).first()
        if not buyer:
            return Response(status=400, error='买家不存在')

        self.serializer_class = TradeCreateSerializer
        serial = self.serializer_class(data=data)
        if not serial.is_valid():
            return Response(status=400, error=serial.errors)

        data['buyer'] = buyer
        data['seller'] = request.user
        data['user'] = request.user
        trade = Trade.objects.create(**data)
        return HttpResponseRedirect('/accounts/center')

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        trade = Trade.objects.filter(id=pk).first()
        serial = TradeDetailSerializer(trade)
        data = serial.data
        context = dict(data=data)
        return render(request, 'blog-detail.html', context)

    def update(self, request, *args, **kwargs):
        params = request.POST.dict()
        id = params.get('id')
        trade = Trade.objects.filter(pk=id).first()
        if trade:
            trade.status = u'confirm'
            trade.save()

        return HttpResponseRedirect('/accounts/center')
