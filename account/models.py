# -*- coding: utf-8 -*-

"""
Create at 2018/7/2
"""

__author__ = 'TT'

from django.db import models
from django.contrib.auth.models import User


DELIVERY = {
    1: u'海外直邮', 2: u'国内现货', 3: u'人肉带回', 4: u'物流转运'
}

SERVICE = {
    1: u'代购', 2: u'拼单', 3: u'代收转发', 4: u'物流货代'
}

SOURCE_AREA = dict(
    Europe=u'欧洲', America=u'美洲', Oceania=u'大洋洲',
    Asia=u'亚洲', Africa=u'非洲',
    USA=u'美国', Canada=u'加拿大', UK=u'英国', France=u'法国',
    Italy=u'意大利', Germany=u'德国', Australia=u'澳大利亚',
    Nz=u'新西兰', Japan=u'日本', Korea=u'韩国', HKM=u'港澳',
    China=u'中国'
)

BLOCKS = dict(
    news=u'海淘那些事',
    man=u'达人发布',
    want=u'我要我要的',
)

ABOUT = dict(
    product=u'产品',
    logistics=u'物流',
)


class UserInfo(models.Model):
    """用户信息，跟用户表一对一
    来区分达人买手和普通用户"""
    user = models.OneToOneField(User, related_name='info')
    nickname = models.CharField(max_length=200, default='')
    open_id = models.CharField(max_length=200, default='')
    is_buyer = models.BooleanField(default=False)
    head_img = models.CharField(max_length=200, default='')
    desc = models.TextField(default='')
    goods = models.CharField(max_length=200, default='')
    source = models.CharField(max_length=200, default='')
    delivery = models.CharField(max_length=20, default='')
    service = models.CharField(max_length=20, default='')
    wx = models.CharField(max_length=50, default='')
    qq = models.CharField(max_length=20, default='')
    phone = models.CharField(max_length=20, default='')
    email = models.CharField(max_length=50, default='')
    www = models.CharField(max_length=50, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_at = models.DateTimeField(auto_now_add=True)


# 积分记录表
# 用户文章
# 用户用户

# class UserExperience(models.Model):
#     user = models.ForeignKey(UserInfo, related_name=u'exp_user_info', verbose_name=u'关联用户')
#     integral = models.IntegerField(default=0, verbose_name=u'积分')

    # like = models.IntegerField(default=0, verbose_name=u'点赞')
    # unlike = models.IntegerField(default=0, verbose_name=u'不喜欢/拉黑')
    # comment = models.IntegerField(default=0, verbose_name=u'评论')
    # favorites = models.ForeignKey(User, related_name=u'exp_user_fav', verbose_name=u'收藏')
    # attention = models.ForeignKey(User, related_name=u'exp_user_att', verbose_name=u'关注')
    #




