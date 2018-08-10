#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: serializer.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 10/08/2018 17:10
"""

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from blog.models import BlogReply
from onepush.utils import format_datetime


class ReplyBlogListSerializer(ModelSerializer):
    """
    博客回复--列表
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
        model = BlogReply
        fields = ('id', 'blog_id', 'content', 'ref_reply_id', 'user_id',
                  'username', 'created_at')


class ReplyBlogCreateSerializer(ModelSerializer):
    """
    博客回复--创建
    """

    blog_id = serializers.IntegerField(required=True)
    content = serializers.CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)
    ref_reply_id = serializers.IntegerField(required=False, allow_null=True)
    user_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = BlogReply
        fields = ('blog_id', 'content', 'ref_reply_id', 'user_id')
