#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: serializer.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 10/08/2018 17:27
"""

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from blog.models import Theory, TheoryLike, TheoryReply
from account.models import THEORY_STATE
from onepush.utils import format_datetime
from blog.trade.serializer import TradeDetailSerializer


class TheoryCreateSerializer(ModelSerializer):

    code = serializers.CharField(required=True, max_length=50)
    user_id = serializers.IntegerField(required=True)
    trade_id = serializers.IntegerField(required=True)
    initiator = serializers.BooleanField(required=False)
    title = serializers.CharField(required=False, max_length=200)
    content = serializers.CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)

    class Meta:
        model = Theory
        fields = ('code', 'user_id', 'trade_id', 'initiator', 'title',
                  'content')


class TheoryListSerializer(ModelSerializer):
    created_at = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    @staticmethod
    def get_created_at(obj):
        return format_datetime(obj.created_at)

    @staticmethod
    def get_status(obj):
        return dict(THEORY_STATE).get(obj.status)

    class Meta:
        model = Theory
        fields = ('id', 'trade_id', 'code', 'title', 'content', 'status',
                  'created_at', 'user_id', 'initiator')


class TheoryDetailSerializer(ModelSerializer):

    reply = serializers.SerializerMethodField()
    like_respondent = serializers.SerializerMethodField()
    like_prosecute = serializers.SerializerMethodField()
    trade = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()
    # initiator_user = serializers.SerializerMethodField()

    @staticmethod
    def get_reply(obj):
        reply = TheoryReply.objects.filter(theory=obj).all()
        return reply

    @staticmethod
    def get_like_prosecute(obj):
        return TheoryLike.objects.filter(theory=obj, like_prosecute=True).count()

    @staticmethod
    def get_like_respondent(obj):
        return TheoryLike.objects.filter(theory=obj, like_respondent=True).count()

    # @staticmethod
    # def get_initiator_user(obj):
    #     if obj.initiator:
    #         return obj.trade.buyer
    #     else:
    #         return obj.trade.seller

    @staticmethod
    def get_trade(obj):
        if not obj.trade:
            return dict()
        serial = TradeDetailSerializer(obj.trade)
        return serial.data

    @staticmethod
    def get_picture(obj):
        pics = obj.picture.all()
        pics = ['/media/' + item.url for item in pics]
        return pics

    class Meta:
        model = Theory
        fields = ('id', 'code', 'trade', 'initiator', 'title', 'reply',
                  'content', 'picture', 'like_prosecute', 'like_respondent')
