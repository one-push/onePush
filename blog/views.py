# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponseRedirect
from blog.models import Blog


class BlogViews(ModelViewSet):

    def list(self, request, *args, **kwargs):

        params = request.GET.dict()
        params['user_id'] = 1
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

        values = Blog.objects.filter(**args).values()
        context = dict(data=[item for item in values])

        html = block + '.html'
        return render(request, html, context)

    def create(self, request, *args, **kwargs):
        data = request.POST.dict()
        article = data.get('article')
        intro = article[:100] if len(article) > 100 else article
        data['intro'] = intro + '...'
        Blog.objects.create(**data)
        return HttpResponseRedirect('block?block={}'.format(data.get('block')))

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        values = Blog.objects.filter(id=pk).values()

        context = dict(data=values[0] if len(values) else dict())
        return render(request, 'blog-detail.html', context)


class AreaViews(ModelViewSet):
    def list(self, request, *args, **kwargs):
        context = dict()
        return render(request, 'rankings.html', context)

# @login_required()
# def area(req):
#     context = dict()
#     return render(req, 'rankings.html', context)
