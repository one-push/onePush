#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: serializer.py.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 15/08/2018 13:41
"""

from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from models import UserInfo
from models import UserFavorites
from models import VIP_LEVEL, SOURCE_AREA, SERVICE, DELIVERY, GOODS


class UserInfoListSerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super(UserInfoListSerializer, self).__init__(*args, **kwargs)

    source_text = SerializerMethodField()
    service_text = SerializerMethodField()
    delivery_text = SerializerMethodField()
    goods_text = SerializerMethodField()
    level_text = SerializerMethodField()
    favorite_ids = SerializerMethodField()
    attention_ids = SerializerMethodField()
    is_favorite = SerializerMethodField()
    is_attention = SerializerMethodField()

    @staticmethod
    def get_enum(macro, item):
        return dict(macro).get(item, '')

    @staticmethod
    def get_goods_text(obj):
        gos = obj.goods.split(',')
        gost = [UserInfoListSerializer.get_enum(GOODS, item) for item in gos
                if item and UserInfoListSerializer.get_enum(GOODS, item)]
        return ','.join(gost)

    @staticmethod
    def get_delivery_text(obj):
        dels = obj.delivery.split(',')
        dt = [UserInfoListSerializer.get_enum(DELIVERY, item) for item in dels
              if item and UserInfoListSerializer.get_enum(DELIVERY, item)]
        return ','.join(dt)

    @staticmethod
    def get_service_text(obj):
        sers = obj.service.split(',')
        st = [UserInfoListSerializer.get_enum(SERVICE, item) for item in sers
              if item and UserInfoListSerializer.get_enum(SERVICE, item)]
        return ','.join(st)

    @staticmethod
    def get_source_text(obj):
        return dict(SOURCE_AREA).get(obj.source, u'')

    @staticmethod
    def get_level_text(obj):
        return dict(VIP_LEVEL).get(obj.level, u'菜鸟')

    @staticmethod
    def get_favorite_ids(obj):
        # 收藏的用户列表
        favorites = UserFavorites.objects.filter(favorite=obj.user).all()
        if favorites:
            serial = UserFavoriteListSerializer(favorites, many=True)
            return serial.data
        else:
            return list()

    @staticmethod
    def get_attention_ids(obj):
        # 关注的用户列表
        favorites = UserFavorites.objects.filter(attention=obj.user).all()
        if favorites:
            serial = UserFavoriteListSerializer(favorites, many=True)
            return serial.data
        else:
            return list()

    def get_is_favorite(self, obj):
        if self.current_user:
            # 当前达人是否有人关注
            return UserFavorites.objects.filter(
               favorite=obj.user,
               user=self.current_user).exists()
        else:
            return False

    def get_is_attention(self, obj):
        if self.current_user:
            return UserFavorites.objects.filter(
                attention=obj.user,
                user=self.current_user).exists()
        else:
            return False

    class Meta:
        model = UserInfo
        fields = ('id', 'user', 'is_vip', 'level', 'score', 'nickname',
                  'level_text', 'goods_text', 'delivery_text', 'service_text',
                  'source_text', 'address',
                  'open_id', 'is_buyer', 'head_img', 'desc',  'goods', 'source',
                  'delivery', 'service', 'wx', 'qq', 'phone', 'email', 'www',
                  'created_at', 'last_login_at', 'is_favorite', 'is_attention',
                  'favorite_ids', 'attention_ids')


class UserFavoriteListSerializer(ModelSerializer):

    class Meta:
        model = UserFavorites
        fields = ('user',)
        # fields = ('id', 'user', 'favorite', 'attention')
