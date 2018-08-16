# -*- coding: utf-8 -*-

"""
Create at 2018/7/4
"""

__author__ = 'TT'

from account.models import UserInfo, UserScore, UserFavorites
from account.models import VIP_LEVEL
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.viewsets import ModelViewSet
from onepush import settings
from blog.models import Blog, Trade, Theory, BlogRelationUser, BlogReply
from blog.serializer import BlogListSerializer
from blog.trade.serializer import TradeListSerializer
from blog.theory.serializer import TheoryListSerializer
from serializer import UserInfoListSerializer


def index(request):
    """首页"""
    user, users = None, None
    if request.user:
        if isinstance(request.user, User):
            user = request.user
            queryset = UserInfo.objects.filter(is_vip=True)[:11]
            users = UserInfoListSerializer(queryset, many=True,
                                           current_user=request.user)

    context = dict(
        STATIC_URL=settings.STATIC_URL,
        da_list=users.data if users else [],  # 达人
        user=user,
    )
    return render(request, 'index.html', context)


def sign_up(req):
    """"""
    username = req.POST.get('username', '')
    password = req.POST.get('password', '')
    print(username, password)
    # return HttpResponseRedirect('/index')
    user = User.objects.filter(username=username).first()
    if user:
        login(req, user)
        return HttpResponseRedirect('/index')
        # return HttpResponse('user exists')
    user = User.objects.create(username=username, password=password)
    UserInfo.objects.create(user=user)
    UserScore.objects.create(user=user)
    login(req, user)
    return HttpResponseRedirect('/index')


def sign_in(req):
    """"""
    username = req.POST.get('username', '')
    password = req.POST.get('password', '')
    user = authenticate(req, username=username, password=password)
    print(user)
    if user is not None:
        return HttpResponseRedirect('/index')
    return HttpResponseRedirect('/index')


@login_required()
def sign_out(req):
    """"""
    print(2222)
    logout(req)
    print(11111)
    # context = dict(
    #     STATIC_URL=settings.STATIC_URL,
    #     da_list=[],
    #     user=req.user if req.user else None
    # )
    # return render(req, 'index.html', context)
    return HttpResponseRedirect('/index')


@login_required()
def user_setting(req):
    """"""
    key_list = [u'nickname', u'head_img', u'desc', u'goods', u'source', u'delivery', u'service',
                u'wx', u'qq', u'phone', u'email', u'www']
    info = req.user.info
    print(req.POST)
    print(info.id)
    if req.method == 'POST':
        for key in key_list:
            if req.POST.get(key, ''):
                print(key, req.POST.get(key, ''))
                setattr(info, key, req.POST.get(key, ''))
            print(getattr(info, key))
        info.save()
        return HttpResponseRedirect('/account/center')

    context = dict(
        STATIC_URL=settings.STATIC_URL,
        user_info=info
    )
    return render(req, 'release.html', context)


@login_required()
def user_center(req):
    """
    用户中心
    """

    html = 'member.html'
    trades_waiting = None
    trades_waiting_serial = None
    params = dict(is_delete=False)
    args = dict(user=req.user, is_delete=False)
    if isinstance(req.user.info, UserInfo) and req.user.info.is_vip:
        params['user'] = req.user
        html = 'member-vip.html'
        trades = Trade.objects.filter(**params).all()
    else:
        params['buyer'] = req.user
        trades = Trade.objects.filter(**dict(params, **dict(status='confirm'))).all()
        params = dict(params, **dict(status='waiting'))
        trades_waiting = Trade.objects.filter(**params).all()
        trades_waiting_serial = TradeListSerializer(trades_waiting, many=True)

    blogs = Blog.objects.filter(**args).all()
    theorys = Theory.objects.filter(**args).all()

    blogs_serial = BlogListSerializer(blogs, many=True)
    theorys_serial = TheoryListSerializer(theorys, many=True)
    trades_serial = TradeListSerializer(trades, many=True)
    info = UserInfo.objects.filter(user=req.user)
    info_serial = UserInfoListSerializer(info, many=True, current_user=req.user)
    info_data = info_serial.data

    context = dict(
        STATIC_URL=settings.STATIC_URL,
        user_info=info_data[0] if len(info_data) else {},
        level_text=dict(VIP_LEVEL).get(req.user.info.level, u'菜鸟'),
        blogs=blogs_serial.data,
        trades=trades_serial.data,
        trades_waiting=trades_waiting_serial.data if trades_waiting_serial else [],
        theorys=theorys_serial.data,
        user=req.user,
        blog_count=blogs.count(),
        trade_count=trades.count() + (trades_waiting.count() if trades_waiting else 0),
        theory_count=theorys.count(),
        favorite_count=UserFavorites.objects.filter(favorite=req.user).count(),
        attention_count=BlogRelationUser.objects.filter(user=req.user).count(),
        reply_count=BlogReply.objects.filter(user=req.user).count(),
    )

    return render(req, html, context)


class UserList(ModelViewSet):

    def list(self, request, *args, **kwargs):
        area = request.GET.dict().get('area', None)
        other_area = (u'Europe', u'America', u'Oceania', u'Asia', u'Africa',)
        queryset = UserInfo.objects.filter(is_vip=True)
        if area == u'hot':
            queryset = queryset.filter(~Q(source__in=other_area))
        elif area == u'otherArea':
            queryset = queryset.filter(source__in=other_area)
        elif area:
            queryset = queryset.filter(source=area)

        self.serializer_class = UserInfoListSerializer
        self.queryset = queryset
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserInfoListSerializer(page, many=True, current_user=request.user)
            # ret_data = self.get_paginated_response(serializer.data)
            return render(request, 'rankings.html', dict(
                users=serializer.data,
                count=len(serializer.data)
            ))

        serializer = self.get_serializer(queryset, many=True)
        context = dict(users=serializer.data, count=len(serializer.data))
        return render(request, 'rankings.html', context)





