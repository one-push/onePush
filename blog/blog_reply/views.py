#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: views.py.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 07/08/2018 20:37
"""
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from blog.serializer import ReplyBlogCreateSerializer, ReplyBlogListSerializer
from blog.models import BlogReply
from blog.service import update_score


class BlogReplyViews(ModelViewSet):

    def get_serializer_class(self):
        return ReplyBlogListSerializer

    def list(self, request, *args, **kwargs):

        blog_id = request.GET.get('blog_id')
        if not blog_id:
            return Response(status=400, error=u'博客不存在')

        self.serializer_class = ReplyBlogListSerializer
        self.queryset = BlogReply.objects.filter(blog_id=blog_id)
        ret = super(BlogReplyViews, self).list(request)

        context = dict(data=ret.data,
                       reply_count=self.queryset.count())
        return HttpResponseRedirect('block/{}'.format(blog_id), context)

    def create(self, request, *args, **kwargs):
        data = request.POST.dict()
        serial = ReplyBlogCreateSerializer(data=data)
        if not serial.is_valid():
            return Response(status=400, error=serial.errors)

        ins = serial.save()
        if ins:
            update_score(request.user, 'comments', ins.id)
        return HttpResponseRedirect('block/{}'.format(data.get('blog_id')))

    def retrieve(self, request, *args, **kwargs):
        context = dict()
        # return render(request, '', context)
