#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: serializer.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 10/08/2018 17:31
"""


from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from blog.models import TheoryReply
from onepush.utils import format_datetime
from blog.models import TheoryLike


class TradeReplyListSerializer(ModelSerializer):
    """
    回复
    """

    username = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    @staticmethod
    def get_username(obj):
        return obj.user.username

    @staticmethod
    def get_created_at(obj):
        return format_datetime(obj.created_at)

    class Meta:
        model = TheoryReply
        fields = ('id', 'theory_id', 'content', 'ref_reply_id', 'user_id',
                  'username', 'created_at')


class TradeReplyCreateSerializer(ModelSerializer):
    """
    博客回复--创建
    """

    theory_id = serializers.IntegerField(required=True)
    content = serializers.CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)
    ref_reply_id = serializers.IntegerField(required=False, allow_null=True)
    user_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = TheoryReply
        fields = ('theory_id', 'content', 'ref_reply_id', 'user_id')


# 点赞
class TradeLikeListSerializer(ModelSerializer):
    class Meta:
        model = TheoryLike
        fields = '__all__'


class TradeLikeCreateSerializer(ModelSerializer):
    """
    """

    theory_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=False, allow_null=True)
    like_prosecute = serializers.BooleanField(default=False, required=False)
    like_respondent = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = TheoryLike
        fields = ('theory_id', 'user_id', 'like_prosecute', 'like_respondent')
