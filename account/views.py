# -*- coding: utf-8 -*-

"""
Create at 2018/7/4
"""

__author__ = 'TT'

from account.models import UserInfo, UserScore
from account.models import VIP_LEVEL
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from onepush import settings
from blog.models import Blog, Trade, Theory
from blog.serializer import BlogListSerializer
from blog.trade.serializer import TradeListSerializer
from blog.theory.serializer import TheoryListSerializer


def index(req):
    """首页"""
    user = None
    if req.user:
        if isinstance(req.user, User):
            print(True)
            user = req.user
    context = dict(
        STATIC_URL=settings.STATIC_URL,
        da_list=[],
        user=user
    )
    return render(req, 'index.html', context)


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

    context = dict(
        STATIC_URL=settings.STATIC_URL,
        user_info=req.user.info,
        level_text=dict(VIP_LEVEL).get(req.user.info.level, u'菜鸟'),
        blogs=blogs_serial.data,
        trades=trades_serial.data,
        trades_waiting=trades_waiting_serial.data if trades_waiting_serial else [],
        theorys=theorys_serial.data,
        user=req.user,
        blog_count=blogs.count(),
        trade_count=trades.count() + (trades_waiting.count() if trades_waiting else 0),
        theory_count=theorys.count(),
    )

    return render(req, html, context)








