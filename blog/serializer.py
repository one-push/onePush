#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: serializer.py.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 05/08/2018 14:26
"""

from models import Blog, Trade, Theory
from account.models import BLOCKS, TRADE_STATE, THEORY_STATE
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from onepush.utils import format_datetime


class BlogCreateSerializer(ModelSerializer):

    title = serializers.CharField(required=True, max_length=200)
    block = serializers.CharField(required=False, max_length=50, allow_blank=True)
    source_area = serializers.CharField(required=False, max_length=50, allow_blank=True)
    article = serializers.CharField(max_length=None, min_length=None, allow_blank=False,trim_whitespace=True)
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
        return BLOCKS.get(obj.block)

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
    screen_shot = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Trade
        fields = ('date', 'buyer', 'seller', 'amount', 'screen_shot',
                  'user_id', 'content')


class TradeListSerializer(ModelSerializer):
    status = serializers.SerializerMethodField()


    @staticmethod
    def get_status(obj):
        return dict(TRADE_STATE).get(obj.status)

    class Meta:
        model = Trade
        fields = ('id', 'date', 'buyer', 'seller', 'amount', 'screen_shot',
                  'user_id', 'content', 'status')


class TradeDetailSerializer(TradeListSerializer):
    pass


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
        fields = ('id', 'code', 'prosecute', 'respondent', 'title', 'content',
                  'picture', 'pro_support_count', 'res_support_count', 'user_id')
