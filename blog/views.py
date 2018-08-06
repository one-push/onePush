# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from blog.models import Blog
from blog.serializer import BlogListSerializer, \
    BlogCreateSerializer, BlogDetailSerializer


class BlogViews(ModelViewSet):

    def get_serializer_class(self):
        return BlogListSerializer

    def list(self, request, *args, **kwargs):

        params = request.GET.dict()
        params['user_id'] = request.user.id
        block = params.get('block')

        args = dict(
            user_id=params.get('user_id'),
            is_delete=False,
            block=block,
            about=params.get('about'),
            source_area=params.get('source_area')
        )

        # 删除为空的参数
        tmp = args.copy()
        for key, val in tmp.items():
            if key != 'is_delete' and not val:
                args.pop(key)

        self.serializer_class = BlogListSerializer
        self.queryset = Blog.objects.filter(**args)
        ret = super(BlogViews, self).list(request)

        context = dict(data=ret.data)
        html = block + '.html'
        return render(request, html, context)

    def create(self, request, *args, **kwargs):
        data = request.POST.dict()
        article = data.get('article')
        intro = article[:100] if len(article) > 100 else article
        data['intro'] = intro + '...'

        self.serializer_class = BlogCreateSerializer
        serial = self.serializer_class(data=data)
        if not serial.is_valid():
            return Response(status=400, error=serial.errors)

        serial.save()
        return HttpResponseRedirect('block?block={}'.format(data.get('block')))

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        blog = Blog.objects.filter(id=pk).first()
        serial = BlogDetailSerializer(blog)
        data = serial.data
        context = dict(data=data)
        return render(request, 'blog-detail.html', context)


class AreaViews(ModelViewSet):
    def list(self, request, *args, **kwargs):
        context = dict()
        return render(request, 'rankings.html', context)



