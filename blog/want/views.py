#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: views.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 2018/8/1 20:11
"""

from django.shortcuts import render


# @login_required()
def want(req):
    context = dict()
    return render(req, 'want.html', context)