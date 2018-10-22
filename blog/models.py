# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.db import models
from mptt.models import MPTTModel
from account.models import UserInfo
from account.models import BLOCKS, ABOUT, TRADE_STATE, THEORY_STATE
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(User, related_name='%(class)s_created_by_user', null=True, blank=True, db_index=True)
    updated_by = models.ForeignKey(User, related_name='%(class)s_updated_by_user', null=True, blank=True)
    is_delete = models.BooleanField(default=False, db_index=True)

    class Meta:
        abstract = True

    def delete(self):
        self.is_delete = True
        self.deleted_at = datetime.now()
        self.updated_at = datetime.now()
        self.save()

    def remove(self):
        self.deleted()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        super(BaseModel, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.updated_at = datetime.now()
        super(BaseModel, self).update(*args, **kwargs)


class Picture(models.Model):
    """图片存储"""
    url = models.CharField(max_length=200, null=True, verbose_name=u'链接地址')
    describe = models.CharField(max_length=100, null=True, verbose_name=u'图片描述')


class Blog(BaseModel):
    """文章发布"""
    user = models.ForeignKey(User, related_name='blo_user', blank=True)

    title = models.CharField(max_length=200, default='', verbose_name=u'主题')
    about = models.CharField(max_length=50, default='', choices=ABOUT, verbose_name=u'关于')
    block = models.CharField(max_length=20, default='', choices=BLOCKS, verbose_name=u'发布板块')
    intro = models.CharField(max_length=250, default='', verbose_name=u'文章简介')
    source_area = models.CharField(max_length=50, verbose_name=u'来源地', blank=True, null=True)
    article = models.TextField(default='', verbose_name=u'文章正文')
    picture = models.ManyToManyField(Picture, related_name='bpics', verbose_name=u'图片', blank=True)

    see_count = models.IntegerField(default=0, verbose_name=u'浏览数')
    forward_count = models.IntegerField(default=0, verbose_name=u'转发数')
    favorite_count = models.IntegerField(default=0, verbose_name=u'收藏数')


#  文章用户关系
class BlogRelationUser(models.Model):
    """
    一对多
    博客和用户的关系
    """
    blog = models.ForeignKey(Blog, related_name='blog_relation', verbose_name='关联博客' )
    user = models.ForeignKey(User, related_name='relation', verbose_name=u'收藏用户', blank=True, null=True)


class BlogReply(BaseModel):
    """博客回复内容 属性"""
    blog = models.ForeignKey(Blog, related_name='reply_blog', verbose_name=u'文章')
    user = models.ForeignKey(User, related_name='reply_user', verbose_name=u'评论的用户', blank=True)
    content = models.TextField(default='', verbose_name=u'评论的内容')
    ref_reply = models.ForeignKey('self', verbose_name=u'回答哪条内容', blank=True, null=True)


class Trade(BaseModel):
    """
    交易记录

    达人创建，非达人只能查看相关
    """
    user = models.ForeignKey(User, verbose_name=u'用户', blank=True)
    date = models.DateField(verbose_name=u'交易日期')
    buyer = models.ForeignKey(User, related_name='tra_buy', verbose_name=u'买方')
    seller = models.ForeignKey(User, related_name='tra_sel', verbose_name=u'卖方')
    amount = models.FloatField(default=0, verbose_name=u'交易金额')
    content = models.CharField(default='', max_length=100, verbose_name=u'交易内容')
    status = models.CharField(choices=TRADE_STATE, default='waiting', max_length=30, verbose_name=u'交易状态')
    img = models.CharField(default='', max_length=100, verbose_name=u'首付款截图', blank=True, null=True)


class Theory(BaseModel):
    """发起说理"""
    user = models.ForeignKey(User, verbose_name=u'用户')
    trade = models.ForeignKey(Trade, related_name='trade', verbose_name=u'交易')
    code = models.CharField(max_length=50, default='', verbose_name=u'序号')

    initiator = models.BooleanField(verbose_name=u'发起诉讼方 True(买方) False(卖方)')

    status = models.CharField(choices=THEORY_STATE, default='trial', max_length=30, verbose_name=u'状态')
    title = models.CharField(max_length=200, default='', verbose_name=u'主题')
    content = models.CharField(max_length=200, default='', verbose_name=u'内容')
    picture = models.ManyToManyField(Picture, related_name='pics', verbose_name=u'起诉用图片', blank=True)


class TheoryLike(models.Model):
    """
    发起说理支持用户（说理点赞）

    一个用户一个说理，只能支持一次
    """
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    theory = models.ForeignKey(Theory, related_name='like')
    user = models.ForeignKey(User, related_name='like_user', verbose_name=u'')
    like_prosecute = models.BooleanField(verbose_name=u'支持起诉方', default=False)
    like_respondent = models.BooleanField(verbose_name=u'支持被诉方', default=False)


class TheoryReply(MPTTModel):
    """
    发起说理，内容回复
    暂时理解 只能起诉写评论，被起诉方回答评论，
    且再次回答需要重新填写评论

    考虑是否将blogReply和TheoryReply合并一张表
    """
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    is_delete = models.BooleanField(default=False, db_index=True)

    theory = models.ForeignKey(Theory, related_name='reply', verbose_name=u'发起说理')
    user = models.ForeignKey(User, verbose_name=u'评论的用户', blank=True)
    content = models.TextField(default='', verbose_name=u'评论的内容')
    parent = models.ForeignKey('self', verbose_name=u'回答哪条内容', blank=True, null=True)
