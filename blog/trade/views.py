#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: views.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 06/08/2018 19:22
"""

from __future__ import unicode_literals
import json
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from blog.trade.serializer import TradeListSerializer
from blog.trade.serializer import TradeCreateSerializer
from blog.trade.serializer import TradeDetailSerializer
from blog.models import Trade
from blog.service import update_score


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
        'file' in data and data.pop('file')
        if data.get('method') == 'put':
            'method' in data and data.pop('method')
            return self.update(request, data)

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
        if trade:
            update_score(request.user, 'trade')
        return HttpResponseRedirect('/accounts/center')

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        trade = Trade.objects.filter(id=pk).first()
        # serial = TradeDetailSerializer(trade)
        # data = serial.data

        # 当前起诉用户是买方  initiator = True
        # 当前起诉用户是卖方  initiator = False
        initiator = True if request.user.username == trade.buyer.username else False
        data = dict(trade_id=pk, initiator=initiator)
        data['prosecute_user'] = trade.buyer.username if initiator else trade.seller.username
        data['prosecute_id'] = trade.buyer.id if initiator else trade.seller.id
        data['prosecute'] = u'买方' if initiator else u'卖方'
        data['respondent_user'] = trade.seller.username if initiator else trade.buyer.username
        data['respondent_id'] = trade.seller.id if initiator else trade.buyer.id
        data['respondent'] = u'卖方' if initiator else u'买方'

        context = dict(data=data, content=json.dumps(data))
        return render(request, 'theory.html', context)

    def update(self, request, params):
        id = params.get('id')
        if 'buyer' in params:
            buyer = params.pop('buyer')
            user = User.objects.filter(username=buyer).first()
            if user:
                params['buyer_id'] = user.id

        trade = Trade.objects.filter(pk=id).update(**params)
        if trade:
            update_score(request.user, 'trade')

        return HttpResponseRedirect('/accounts/center')
