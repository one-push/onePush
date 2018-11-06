# -*- coding: utf-8 -*-

"""
Create at 2018/7/2
"""

__author__ = 'TT'

from django.db import models
from django.contrib.auth.models import User


GOODS = (
    (u'luxury', u'奢侈品'),
    (u'clothes', u'服装 鞋帽 箱包'),
    (u'health', u'美妆 个人健康'),
    (u'toy', u'玩具 母婴 儿童用品'),
    (u'food', u'食物 保健品 酒水'),
    (u'watch', u'钟表 首饰'),
    (u'phone', u'手机 摄影 数码'),
    (u'electronic', u'电器 电子配件 智能生活'),
    (u'furniture', u'家具 厨具 家装'),
    (u'computer', u'电脑办公'),
    (u'sport', u'运动 户外'),
    (u'car', u'汽车用品'),
)

DELIVERY = (
    (u'oversea', u'海外直邮'),
    (u'domestic', u'国内现货'),
    (u'human', u'人肉带回'),
    (u'logistics', u'物流转运')
)

SERVICE = (
    (u'buyer', u'代购'),
    (u'bill', u'拼单'),
    (u'collection', u'代收转发'),
    (u'logistics', u'物流货代')
)

SOURCE_AREA = (
    (u'USA', u'美国'),
    (u'Canada', u'加拿大'),
    (u'UK', u'英国'),
    (u'France', u'法国'),
    (u'Italy', u'意大利'),
    (u'Germany', u'德国'),
    (u'Australia', u'澳大利亚'),
    (u'Nz', u'新西兰'),
    (u'Japan', u'日本'),
    (u'Korea', u'韩国'),
    (u'HKM', u'港澳'),
    (u'China', u'中国')
)

OTHER_AREA = [
    (u'Europe', u'欧洲'),
    (u'America', u'美洲'),
    (u'Oceania', u'大洋洲'),
    (u'Asia', u'亚洲'),
    (u'Africa', u'非洲'),
]

LEVEL_SCORE = {
    1: (0, 50),
    2: (51, 100),
    3: (101, 200),
    4: (201, 400),
    5: (401, 800),
    6: (801, 1500),
    7: (1501, 4000),
    8: (4001, 6000),
    9: (6001, 9000),
    10: (9001, 15000),
    11: (15001, -1),
}

# favorite  forward
ACTION_SCORE = {
    # u'news': 25,    # 海淘那些事
    # u'trade': 15,   # 交易记录
    # u'want': 5,     # 我要我要
    # u'theory_like': 3,  # 说说谁有理点击支持
    # u'comments': 3,      # 发表评论
    # u'like': 3,          # 赞/倒

    u'man': 25,         # 达人工作台     仅VIP
    u'msg': 20,         # 私信
    u'forward': 20,     # 转发
    u'favorite': 10,    # 收藏
    u'attention': 10,   # 关注
    u'login': 10,       # 登陆
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
    level = models.IntegerField(default=1, choices=VIP_LEVEL, verbose_name=u'等级')
    score = models.IntegerField(default=0, verbose_name=u'积分')
    nickname = models.CharField(max_length=200, default=u'')
    open_id = models.CharField(max_length=200, default=u'', verbose_name=u'微信ID')
    is_buyer = models.BooleanField(default=False)
    head_img = models.CharField(max_length=200, default=u'', verbose_name=u'头像')
    desc = models.TextField(default=u'描述')
    address = models.TextField(max_length=300, default=u'', verbose_name=u'地址')
    source = models.CharField(max_length=200, default=u'', verbose_name=u'来源')
    goods = models.CharField(max_length=200, default=u'', verbose_name=u'擅长品类, 多个用逗号隔开')
    delivery = models.CharField(max_length=200, default=u'', verbose_name=u'供货方式, 多个用逗号隔开')
    service = models.CharField(max_length=200, default=u'', verbose_name=u'服务内容，多个用逗号隔开')
    wx = models.CharField(max_length=50, default=u'', verbose_name=u'微信号')
    qq = models.CharField(max_length=20, default=u'', verbose_name=u'QQ')
    phone = models.CharField(max_length=20, default=u'', verbose_name=u'电话')
    email = models.CharField(max_length=50, default=u'', verbose_name=u'邮箱')
    www = models.CharField(max_length=50, default=u'', verbose_name=u'网址')
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_at = models.DateTimeField(auto_now_add=True)

    # company

    # 关注该用户的用户
    # attention = models.ManyToManyField(User, related_name=u'user_att', verbose_name=u'关注的用户', blank=True)
    # 收藏该用户的用户
    # favorite = models.ManyToManyField(User, related_name=u'user_fav', verbose_name=u'收藏的用户', blank=True)


class UserScore(models.Model):
    """积分表"""
    user = models.ForeignKey(User, related_name=u'score', verbose_name=u'关联用户')
    total = models.IntegerField(default=0, verbose_name=u'总积分')

    block = models.CharField(default=0, max_length=20, verbose_name=u'加分的行为')
    score = models.IntegerField(default=0, verbose_name=u'增加的积分')

    # 通过action和ref_id可以追溯到原始记录
    ref_id = models.IntegerField(blank=True, null=True, verbose_name=u'关联ID')


class UserBlogFavorites(models.Model):
    """博客收藏&转发表"""
    from blog.models import Blog
    user = models.ForeignKey(User, related_name=u'blog_favorite', verbose_name=u'关联用户')
    block = models.CharField(default='man', max_length=20, verbose_name=u'博客板块')
    type = models.CharField(default='', max_length=20, verbose_name=u'类型')   # favorite forward
    blog = models.ForeignKey(Blog, blank=True, null=True, verbose_name=u'关联博客')


class UserFavorites(models.Model):
    """
    一对多关系
    用户之间的关注和收藏

    """
    user = models.ForeignKey(User, related_name=u'favorite', verbose_name=u'关联用户')
    favorite = models.ForeignKey(User, related_name=u'user_fav', verbose_name=u'收藏的用户', blank=True, null=True)
    attention = models.ForeignKey(User, related_name=u'user_att', verbose_name=u'关注的用户', blank=True, null=True)
#     # unlike = models.IntegerField(default=0, verbose_name=u'不喜欢/拉黑')
#     # comment = models.IntegerField(default=0, verbose_name=u'评论')


class UserInfoShow(models.Model):
    """
    个人信息是否对外展示
    """
    user = models.ForeignKey(User, related_name=u'info_show', verbose_name=u'关联用户')
    user_name = models.BooleanField(default=False, verbose_name=u'用户名')
    nickname = models.BooleanField(default=False)
    open_id = models.BooleanField(default=False, verbose_name=u'微信ID')
    is_buyer = models.BooleanField(default=False)
    head_img = models.BooleanField(default=False, verbose_name=u'头像')
    desc = models.BooleanField(default=False)
    address = models.BooleanField(default=False, verbose_name=u'地址')
    source = models.BooleanField(default=False, verbose_name=u'来源')
    goods = models.BooleanField(default=False, verbose_name=u'擅长品类, 多个用逗号隔开')
    delivery = models.BooleanField(default=False, verbose_name=u'供货方式, 多个用逗号隔开')
    service = models.BooleanField(default=False, verbose_name=u'服务内容，多个用逗号隔开')
    wx = models.BooleanField(default=False, verbose_name=u'微信号')
    qq = models.BooleanField(default=False, verbose_name=u'QQ')
    phone = models.BooleanField(default=False, verbose_name=u'电话')
    email = models.BooleanField(default=False, verbose_name=u'邮箱')
    www = models.BooleanField(default=False, verbose_name=u'网址')


class UserAttributes(models.Model):
    """
    会员属性
    """
    user = models.ForeignKey(User, related_name=u'info_attr', verbose_name=u'关联用户')
    type = models.CharField(max_length=20, default='person',  verbose_name=u'会员性质')  # person || company
    user_name = models.CharField(max_length=200, default=u'')
    user_address = models.TextField(max_length=300, default=u'', verbose_name=u'地址')
    outside_company = models.CharField(max_length=200, default=u'', verbose_name=u'境外公司名称')
    outside_address = models.CharField(max_length=200, default=u'', verbose_name=u'境外公司地址')
    inside_company = models.CharField(max_length=200, default=u'', verbose_name=u'境内公司名称')
    inside_address = models.CharField(max_length=200, default=u'', verbose_name=u'境内公司地址')


class Question(models.Model):
    """询问"""
    from blog.models import Picture
    q_user = models.ForeignKey(User, related_name=u'q_user', verbose_name=u'提问用户')
    a_user = models.ForeignKey(User, related_name=u'a_user', verbose_name=u'回答用户')

    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    content = models.CharField(max_length=200, default='', verbose_name=u'内容')
    picture = models.ManyToManyField(Picture, related_name='q_pics', verbose_name=u'图片', blank=True)


class Answer(models.Model):
    """ 回答 """
    from blog.models import Picture
    question = models.ForeignKey(Question, related_name='question', verbose_name=u'回答的问题')
    user = models.ForeignKey(User, verbose_name=u'回复的用户', blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    content = models.TextField(default='', verbose_name=u'评论的内容')
    picture = models.ManyToManyField(Picture, related_name='a_pics', verbose_name=u'图片', blank=True)
    parent = models.ForeignKey('self', verbose_name=u'回答哪条内容', blank=True, null=True)