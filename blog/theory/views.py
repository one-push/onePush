#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: views.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 2018/8/1 20:13
"""


from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from blog.serializer import TheoryListSerializer
from blog.models import Theory


# @login_required()
def theory(req):
    context = dict()
    return render(req, 'theory.html', context)


class TheoryViews(ModelViewSet):

    def get_serializer_class(self):
        return TheoryListSerializer

    def list(self, request, *args, **kwargs):

        params = request.GET.dict()
        params['user_id'] = request.user.id

        args = dict(
            user_id=params.get('user_id'),
            is_delete=False,
        )

        self.serializer_class = TheoryListSerializer
        self.queryset = Theory.objects.filter(**args)
        ret = super(TheoryViews, self).list(request)

        context = dict(data=ret.data)
        return render(request, 'theory.html', context)

    # def create(self, request, *args, **kwargs):
    #     data = request.POST.dict()
    #     article = data.get('article')
    #     intro = article[:100] if len(article) > 100 else article
    #     data['intro'] = intro + '...'
    #
    #     self.serializer_class = BlogCreateSerializer
    #     serial = self.serializer_class(data=data)
    #     if not serial.is_valid():
    #         return Response(error=serial.errors)
    #
    #     serial.save()
    #     return HttpResponseRedirect('block?block={}'.format(data.get('block')))
    #
    # def retrieve(self, request, *args, **kwargs):
    #     pk = kwargs.get('pk')
    #     blog = Blog.objects.filter(id=pk).first()
    #     serial = BlogDetailSerializer(blog)
    #     data = serial.data
    #     context = dict(data=data)
    #     return render(request, 'blog-detail.html', context)
