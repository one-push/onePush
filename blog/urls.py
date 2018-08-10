# -*- coding: utf-8 -*-

"""
Create at 2018/7/8
"""

__author__ = 'TT'

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from views import *
from blog.theory.views import TheoryViews
from blog.trade.views import TradeViews
from blog.blog_reply.views import BlogReplyViews

router = DefaultRouter(trailing_slash=False)
router.register(r'block', BlogViews, base_name='blocks')
router.register(r'area', AreaViews, base_name='areas')
router.register(r'trade', TradeViews, base_name='trades')
router.register(r'theory', TheoryViews, base_name='theory')
router.register(r'reply', BlogReplyViews, base_name='theory')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^deploy/?$', deploy_blog),
]
