# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.db import models
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
    about = models.CharField(max_length=50, default='', verbose_name=u'主题')
    block = models.CharField(default='', max_length=20, verbose_name=u'发布板块')
    intro = models.CharField(default='', max_length=250, verbose_name=u'文章简介')
    source_area = models.CharField(max_length=50, verbose_name=u'来源地', blank=True, null=True)
    article = models.TextField(default='', verbose_name=u'文章正文')

    see_count = models.IntegerField(default=0, verbose_name=u'浏览数')
    forward_count = models.IntegerField(default=0, verbose_name=u'转发数')
    reply_count = models.IntegerField(default=0, verbose_name=u'回复数')  # 可以在文章回复中统计


# 文章用户关系
# class BlogRelationUser(models.Model):
#     blog = models.ForeignKey(Blog, verbose_name='关联博客')
#
#     pass


class BlogReply(models.Model):
    """博客回复内容 属性"""
    blog = models.ForeignKey(Blog, related_name='reply_blog', verbose_name=u'文章')
    user = models.ForeignKey(User, related_name='reply_user', verbose_name=u'评论的用户', blank=True)
    content = models.TextField(default='', verbose_name=u'评论的内容')
    ref_reply = models.ForeignKey('self', verbose_name=u'回答哪条内容', blank=True)


class Theory(BaseModel):
    """发起说理"""
    user = models.ForeignKey(User, verbose_name=u'用户', blank=True)
    code = models.CharField(max_length=50, default='', verbose_name=u'序号')
    prosecute = models.ForeignKey(User, related_name='the_pro', verbose_name=u'起诉方')
    respondent = models.ForeignKey(User, related_name='the_res', verbose_name=u'被诉方')

    status = models.CharField(choices=THEORY_STATE, default='trial', max_length=30, verbose_name=u'状态')
    title = models.CharField(max_length=200, default='', verbose_name=u'主题')
    content = models.CharField(max_length=200, default='', verbose_name=u'内容')
    picture = models.ForeignKey(Picture, verbose_name=u'起诉用图片')

    pro_support_count = models.IntegerField(verbose_name=u'起诉方支持数')
    res_support_count = models.IntegerField(verbose_name=u'被诉方支持数')


class TheoryReply(models.Model):
    """
    发起说理，内容回复
    暂时理解 只能起诉写评论，被起诉方回答评论，
    且再次回答需要重新填写评论

    考虑是否将blogReply和TheoryReply合并一张表
    """
    theory = models.ForeignKey(Theory, related_name='reply', verbose_name=u'发起说理')
    user = models.ForeignKey(User, verbose_name=u'评论的用户', blank=True)
    content = models.TextField(default='', verbose_name=u'评论的内容')
    ref_reply = models.ForeignKey('self', verbose_name=u'回答哪条内容')


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
    screen_shot = models.ForeignKey(Picture, related_name='tra_pic', verbose_name=u'首付款截图', blank=True, null=True)