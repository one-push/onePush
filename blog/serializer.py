#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: serializer.py.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 05/08/2018 14:26
"""

from models import Blog, BlogRelationUser, Trade, Theory, BlogReply, TheoryLike
from account.models import BLOCKS, TRADE_STATE, THEORY_STATE
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from onepush.utils import format_datetime


class BlogCreateSerializer(ModelSerializer):

    title = serializers.CharField(required=True, max_length=200)
    block = serializers.CharField(required=False, max_length=50, allow_blank=True)
    source_area = serializers.CharField(required=False, max_length=50, allow_blank=True)
    article = serializers.CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)
    user_id = serializers.IntegerField(required=True)

    class Meta:
        model = Blog
        fields = ('title', 'block', 'intro', 'source_area', 'article',
                  'see_count', 'forward_count', 'user_id',
                  'created_at')


class BlogListSerializer(ModelSerializer):

    created_at = serializers.SerializerMethodField()
    block = serializers.SerializerMethodField()

    @staticmethod
    def get_created_at(obj):
        return format_datetime(obj.created_at)

    @staticmethod
    def get_block(obj):
        return dict(BLOCKS).get(obj.block)

    class Meta:
        model = Blog
        fields = ('id', 'title', 'block', 'intro', 'source_area', 'article',
                  'see_count', 'forward_count', 'user_id',
                  'created_at')


class BlogDetailSerializer(BlogListSerializer):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super(BlogDetailSerializer, self).__init__(*args, **kwargs)

    is_favorite = serializers.SerializerMethodField()

    def get_is_favorite(self, obj):
        if self.current_user:
            return BlogRelationUser.objects.filter(
                user=self.current_user, blog=obj).exists()
        else:
            return False

    class Meta:
        model = Blog
        fields = ('id', 'is_favorite', 'title', 'block', 'intro', 'source_area', 'article',
                  'see_count', 'forward_count', 'user_id',
                  'created_at')



