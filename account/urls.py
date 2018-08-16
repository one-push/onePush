# -*- coding: utf-8 -*-

"""
Create at 2018/7/5
"""

__author__ = 'TT'

from django.conf.urls import url
from account.views import index, sign_up, sign_in, sign_out, \
    user_center, user_setting, UserList
from account.favorite.views import create_favorite, dis_favorite

urlpatterns = [
    url(r'^/?$', index, name='index'),
    url(r'^index/?$', index, name='index'),
    url(r'^sign/up/?$', sign_up, name='sign'),
    url(r'^sign/in/?$', sign_in, name='sign'),
    url(r'^login/?$', sign_in, name='sign'),
    url(r'^sign/out/?$', sign_out, name='sign'),
    url(r'^logout/?$', sign_out, name='sign'),
    url(r'^setting/?$', user_setting, name='account'),
    url(r'^center/?$', user_center, name='account'),
    url(r'^users/?$', UserList.as_view({'get': 'list'}), name='users'),
    url(r'^favorite/?$', create_favorite, name='favorite'),
    url(r'^dis_favorite/?$', dis_favorite, name='dis_favorite'),
]
