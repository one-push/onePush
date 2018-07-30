# -*- coding: utf-8 -*-

"""
Create at 2018/7/2
"""

__author__ = 'TT'

from django.db import models
from django.contrib.auth.models import User


delivery = {
    1: u'海外直邮', 2: u'国内现货', 3: u'人肉带回', 4: u'物流转运'
}

service = {
    1: u'代购', 2: u'拼单', 3: u'代收转发', 4: u'物流货代'
}

source_area = dict(
    Europe=u'欧洲', America=u'美洲', Oceania=u'大洋洲',
    Asia=u'亚洲', Africa=u'非洲',
    USA=u'美国', Canada=u'加拿大', UK=u'英国', France=u'法国',
    Italy=u'意大利', Germany=u'德国', Australia=u'澳大利亚',
    Nz=u'新西兰', Japan=u'日本', Korea=u'韩国', HKM=u'港澳',
    China=u'中国'
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


TODOS = [
    '评价', '点赞', '拉黑', '关注', '收藏'
]



