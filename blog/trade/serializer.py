#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: serializer.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 10/08/2018 17:29
"""

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from blog.models import Trade
from account.models import TRADE_STATE


class TradeCreateSerializer(ModelSerializer):
    date = serializers.DateField(required=True)
    buyer = serializers.CharField(required=True)
    amount = serializers.FloatField(required=True)
    content = serializers.CharField(max_length=100)
    seller = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    img = serializers.CharField(required=False, max_length=100, allow_null=True, allow_blank=True)

    class Meta:
        model = Trade
        fields = ('date', 'buyer', 'seller', 'amount', 'img',
                  'user_id', 'content')


class TradeListSerializer(ModelSerializer):
    date_text = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()

    @staticmethod
    def get_date_text(obj):
        return obj.date.strftime('%Y年%m月%d日')

    @staticmethod
    def get_status(obj):
        return dict(TRADE_STATE).get(obj.status)

    @staticmethod
    def get_buyer_name(obj):
        return obj.buyer.username

    @staticmethod
    def get_seller_name(obj):
        return obj.seller.username

    class Meta:
        model = Trade
        fields = ('id', 'date', 'date_text', 'buyer', 'seller', 'amount', 'img',
                  'user_id', 'content', 'status', 'buyer_name', 'seller_name')


class TradeDetailSerializer(TradeListSerializer):
    pass

