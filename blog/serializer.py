#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: serializer.py.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 05/08/2018 14:26
"""

from models import Blog
from rest_framework.serializers import ModelSerializer


class BlogListSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = ('title', 'block', 'intro', 'source_area', 'article',
                  'see_count', 'forward_count', 'reply_count', 'user_id',
                  'created_at')


