# -*- coding: utf-8 -*-

"""
Create at 2018/7/8
"""

__author__ = 'TT'

from django.conf.urls import url
from blog.news.views import overseas_news

from blog.man.views import man

from blog.want.views import want

from blog.theory.views import theory

from views import area

urlpatterns = [
    url(r'^news/?$', overseas_news, name='news'),

    url(r'^man/?$', man, name='man'),

    url(r'^want/?$', want, name='want'),

    url(r'^theory/?$', theory, name='theory'),

    url(r'^area/?$', area, name='area'),
]
