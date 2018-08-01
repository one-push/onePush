#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: views.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 2018/8/1 20:04
"""

from __future__ import unicode_literals

from django.shortcuts import render


# @login_required()
def overseas_news(req):
    context = dict()
    return render(req, 'news.html', context)