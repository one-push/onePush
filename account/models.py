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

LEVEL_SCORE = {
    1: (0, 100),
    2: (101, 200),
    3: (201, 400),
    4: (401, 800),
    5: (801, 1500),
    6: (1501, 2500),
    7: (2501, 4000),
    8: (4001, 6000),
    9: (6001, 9000),
    10: (9001, 15000),
    11: (15001, -1),
}

ACTION_SCORE = {
    u'news': 25,    # 海淘那些事
    u'trade': 15,   # 交易记录
    u'man': 5,      # 达人工作台     仅VIP
    u'want': 5,     # 我要我要
    u'theory_like': 3,  # 说说谁有理点击支持
    u'comments': 3,      # 发表评论
    u'like': 3,          # 赞/倒
}

VIP_LEVEL = (
    (1, u'菜鸟'),
    (2, u'新手'),
    (3, u'见习生'),
    (4, u'小生'),
    (5, u'熟手'),
    (6, u'高手'),
    (7, u'小虾'),
    (8, u'大虾'),
    (9, u'老手'),
    (10, u'达人'),
    (11, u'超级达人'),
)


TRADE_STATE = (
    (u'confirm', u'已确认'),
    (u'waiting', u'待确认'),
)

THEORY_STATE = (
    (u'trial', u'审判中'),
    (u'win', u'胜'),
    (u'lose', u'输'),
)

BLOCKS =(
    (u'news', u'海淘那些事'),
    (u'man', u'达人发布'),
    (u'want', u'我要我要的'),
)

ABOUT = (
    (u'product', u'产品'),
    (u'logistics', u'物流'),
)


class UserInfo(models.Model):
    """用户信息，跟用户表一对一
    来区分达人买手和普通用户"""
    user = models.OneToOneField(User, related_name='info')
    is_vip = models.BooleanField(default=False)
    level = models.IntegerField(default=1, choices=VIP_LEVEL)
    score = models.IntegerField(default=0)
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


class UserScore(models.Model):
    """积分表"""
    user = models.ForeignKey(User, related_name='score', verbose_name=u'关联用户')
    total = models.IntegerField(default=0, verbose_name=u'总积分')

    block = models.CharField(default=0, max_length=20, verbose_name=u'加分的行为')
    score = models.IntegerField(default=0, verbose_name=u'增加的积分')

    # 通过action和ref_id可以追溯到原始记录
    ref_id = models.IntegerField(blank=True, null=True, verbose_name=u'关联ID')


class UserFavorites(models.Model):
    """收藏表"""
    from blog.models import Blog
    block = models.CharField(default=0, max_length=20, verbose_name=u'博客板块')
    blog = models.ForeignKey(Blog, blank=True, null=True, verbose_name=u'关联博客')

    # unlike = models.IntegerField(default=0, verbose_name=u'不喜欢/拉黑')
    # comment = models.IntegerField(default=0, verbose_name=u'评论')
    # favorites = models.ForeignKey(User, related_name=u'exp_user_fav', verbose_name=u'收藏')
    # attention = models.ForeignKey(User, related_name=u'exp_user_att', verbose_name=u'关注')


# 用户文章
# 用户用户





