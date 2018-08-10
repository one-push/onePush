#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: serializer.py.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 05/08/2018 14:26
"""

from models import Blog, Trade, Theory, BlogReply
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
                  'see_count', 'forward_count', 'reply_count', 'user_id',
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
                  'see_count', 'forward_count', 'reply_count', 'user_id',
                  'created_at')


class BlogDetailSerializer(BlogListSerializer):
    pass


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
    buyer = serializers.SerializerMethodField()
    seller = serializers.SerializerMethodField()

    @staticmethod
    def get_date_text(obj):
        return obj.date.strftime('%Y年%m月%d日')

    @staticmethod
    def get_status(obj):
        return dict(TRADE_STATE).get(obj.status)

    @staticmethod
    def get_buyer(obj):
        return obj.buyer.username

    @staticmethod
    def get_seller(obj):
        return obj.seller.username

    class Meta:
        model = Trade
        fields = ('id', 'date', 'date_text', 'buyer', 'seller', 'amount', 'img',
                  'user_id', 'content', 'status')


class TradeDetailSerializer(TradeListSerializer):
    pass


class TheoryCreateSerializer(ModelSerializer):

    code = serializers.CharField(required=True, max_length=50)
    prosecute_id = serializers.IntegerField(required=True)
    respondent_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False, max_length=200)
    content = serializers.CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)
    picture = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Theory
        fields = ('code', 'prosecute_id', 'respondent_id', 'title', 'content',
                  'picture', 'user_id')


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
        fields = ('id', 'code', 'prosecute', 'respondent', 'title', 'content', 'status', 'created_at',
                  'picture', 'pro_support_count', 'res_support_count', 'user_id')


class TheoryDetailSerializer(TheoryListSerializer):
    pass


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