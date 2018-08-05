# -*- coding: utf-8 -*-

"""
Create at 2018/7/8
"""

__author__ = 'TT'

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from views import *
from blog.theory.views import theory

router = DefaultRouter(trailing_slash=False)
router.register(r'block', BlogViews, base_name='blocks')
router.register(r'area', AreaViews, base_name='areas')

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^theory/?$', theory, name='theory'),
]
