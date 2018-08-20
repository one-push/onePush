# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect
from blog.models import Blog, BlogReply, BlogRelationUser
from blog.serializer import BlogListSerializer, \
    BlogCreateSerializer, BlogDetailSerializer
from blog.blog_reply.serializer import ReplyBlogCreateSerializer, \
    ReplyBlogListSerializer
from service import update_score
from onepush.pagination import Pagination
from account.models import OTHER_AREA

PAGE_SIZE = settings.REST_FRAMEWORK.get('PAGE_SIZE', 10)


class BlogViews(ModelViewSet):

    def get_serializer_class(self):
        return BlogListSerializer

    @staticmethod
    def get_intro(article):
        intro = article[:100] if len(article) > 100 else article
        lines = ['\r\n', '\n']
        for item in lines:
            if item in intro:
                return intro[0:intro.index(item)] + '...'
        return intro + '...' if len(article) > 100 else intro

    def list(self, request, *args, **kwargs):

        params = request.GET.dict()
        block = params.get('block', 'news')
        source_area=params.get('source_area')

        args = dict(
            # user_id=request.user.id,
            is_delete=False,
            block=block,
            about=params.get('about'),
        )

        # 删除为空的参数
        tmp = args.copy()
        for key, val in tmp.items():
            if key != 'is_delete' and not val:
                args.pop(key)

        self.serializer_class = BlogListSerializer
        self.queryset = Blog.objects.filter(**args)
        if source_area == u'hot':
            self.queryset = self.queryset.filter(~Q(source__in=OTHER_AREA))
        elif source_area == u'otherArea':
            self.queryset = self.queryset.filter(source__in=OTHER_AREA)
        ret = super(BlogViews, self).list(request)

        data = ret.data
        page_objs = Pagination(
            total_count=data.get('count', 0),
            offset=params.get('offset', 0),
            limit=params.get('limit', PAGE_SIZE),
        )

        ps = page_objs.page_str()
        limit_str = '&limit={}'.format(PAGE_SIZE)
        page_str = ps.replace(limit_str, limit_str + '&block={}'.format(block))

        context = dict(data=ret.data.get('results', []),
                       page_str=page_str)
        html = block + '.html'
        return render(request, html, context)

    def create(self, request, *args, **kwargs):
        data = request.POST.dict()
        block = data.get('block')
        article = data.get('article')
        data['intro'] = BlogViews.get_intro(article)

        self.serializer_class = BlogCreateSerializer
        serial = self.serializer_class(data=data)
        if not serial.is_valid():
            return Response(status=400, error=serial.errors)

        ins = serial.save()
        if ins:
            update_score(request.user, block, ins.id)
        return HttpResponseRedirect('block?block={}'.format(block))

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        blog = Blog.objects.filter(id=pk).first()

        # 博客自己查看不加1
        # if request.user != blog.user:
        blog.see_count += 1
        blog.save()

        serial = BlogDetailSerializer(blog, current_user=request.user)
        data = serial.data

        reply_queryset = BlogReply.objects.filter(blog=blog)
        reply_serial = ReplyBlogListSerializer(reply_queryset, many=True)

        context = dict(
            data=data,
            reply=reply_serial.data,
            reply_count=reply_queryset.count(),
            favorite_count=BlogRelationUser.objects.filter(blog=blog).count(),
            username=blog.user.username,
            params=json.dumps(dict(
                cur_user_id=request.user.id,
                blog_id=blog.id)
            )
        )
        return render(request, 'blog-detail.html', context)


class AreaViews(ModelViewSet):
    def list(self, request, *args, **kwargs):
        context = dict()
        return render(request, 'rankings.html', context)


@api_view(['GET'])
def deploy_blog(request):
    return render(request, 'news-add.html', context={})


@api_view(['POST'])
def reply_blog(request):
    data = request.POST.dict()

    serial = ReplyBlogCreateSerializer(data=data)
    if not serial.is_valid():
        return Response(status=400, error=serial.errors)

    ins = serial.save()
    return HttpResponseRedirect('block/{}'.format(data.get('blog_id')))
