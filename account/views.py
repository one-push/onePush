# -*- coding: utf-8 -*-

"""
Create at 2018/7/4
"""

__author__ = 'TT'

from account.models import UserInfo, UserScore, UserFavorites, UserInfoShow
from account.models import UserAttributes
from account.models import VIP_LEVEL, OTHER_AREA, SOURCE_AREA
from account.models import Question, Answer
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from onepush import settings
from blog.models import Blog, Trade, Theory, BlogRelationUser, BlogReply
from blog.serializer import BlogListSerializer
from blog.trade.serializer import TradeListSerializer
from blog.theory.serializer import TheoryListSerializer
from serializer import UserInfoListSerializer, UserInfoShowListSerializer
from serializer import QuestionAnswerListSerializer
from blog.service import update_score, hot_area


def index(request):
    """首页"""
    user, users = None, None
    if request.user:
        if isinstance(request.user, User):
            user = request.user
    queryset = UserInfo.objects.filter(is_vip=True)[:11]
    users = UserInfoListSerializer(queryset, many=True,
                                   current_user=user)

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
    info_ins = UserInfo.objects.create(user=user)
    # UserScore.objects.create(user=user)
    login(req, user)
    update_score(req.user, 'login', info_ins.id)
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
    key_list = [u'head_img', u'desc', u'goods', u'source',
                u'wx', u'qq', u'phone', u'email', u'www']
    attr_person = [u'attr_user_name', u'attr_user_address']
    attr_company = [u'attr_outside_company', u'attr_outside_address',
                    u'attr_inside_company', u'attr_inside_address']
    info = req.user.info
    print(req.POST)
    print(info.id)
    if req.method == 'POST':
        req_data = req.POST.dict()

        # 用户性质更新
        vip_type = req_data.get('vip_type', 'person')
        user_attr, is_crea = UserAttributes.objects.get_or_create(user=req.user, type=vip_type)
        attr_data = dict()
        if vip_type == 'person':
            for k in attr_person:
                attr_data[k.replace('attr_', '')] = req_data.get(k, '')
        elif vip_type == 'company':
            for k in attr_company:
                attr_data[k.replace('attr_', '')] = req_data.get(k, '')
        if user_attr:
            UserAttributes.objects.filter(pk=user_attr.id).update(**attr_data)
            UserAttributes.objects.filter(
                user=req.user,
                type='person' if vip_type == 'company' else 'company'
            ).delete()

        # 用户信息
        for key in key_list:
            setattr(info, key, req.POST.get(key, ''))
        info.is_vip = True
        info.save()
        return HttpResponseRedirect('/accounts/center')
    elif req.method == 'GET':
        pass

    # 达人页面信息
    attr = UserAttributes.objects.filter(user=req.user).first()
    # attr = attr if attr else dict()
    # if not attr:
    #     attr['user_name'] = req.user.username
    #     attr['user_address'] = info.address
    # if attr and attr.type == 'person':
    #     un = req.user.username if not attr.user_name else attr.user_name
    #     ua = info.address if not attr.user_address else info.address
    #     attr.user_name = un
    #     attr.user_address = ua
    # else:
    if not attr:
        attr = UserAttributes(user_name=req.user.username, user_address=info.address)

    context = dict(
        STATIC_URL=settings.STATIC_URL,
        user_info=info,
        attr=attr,
        contries=[dict(name=k, value=v) for k, v in SOURCE_AREA],
    )
    return render(req, 'release.html', context)


@login_required()
def user_update(req):
    if not req.method.upper() == 'POST':
        return user_center(req)

    pdata = req.POST.dict()
    show_data = dict()
    user_info_data = dict()
    for k, v in pdata.items():
        if "is_" in k:
            # val = bool(v) if v.upper() in ('FALSE', 'TRUE') else False
            show_data[k.replace('is_', '')] = v
        else:
            user_info_data[k] = v

    user_show, is_create = UserInfoShow.objects.get_or_create(user=req.user)
    if user_show:
        UserInfoShow.objects.filter(pk=user_show.id).update(**show_data)

    if 'user_name' in user_info_data:
        user_name = user_info_data.pop('user_name')
        req.user.username = user_name
        req.user.save()
    UserInfo.objects.filter(pk=req.user.info.id).update(**user_info_data)

    return user_center(req)


@login_required()
def user_center(req):
    """
    用户中心
    """

    user_field = (
        (u'user_name', u'用户名'),
        (u'address', u'所在地'),
        (u'phone', u'电话'),
        (u'email', u'邮箱'),
        (u'wx', u'微信'),
        (u'qq', u'QQ'),
        (u'desc', u'需求描述'),
    )

    html = 'member.html'
    params = dict(is_delete=False)
    blogs = []
    is_self = False
    user_ins = User.objects.filter(id=req.GET.get('user_id')).first()
    if user_ins == req.user:
        is_self = True
    elif not user_ins:
        user_ins = req.user
    if isinstance(user_ins.info, UserInfo) and user_ins.info.is_vip:
        params['user'] = user_ins
        html = 'member-vip.html'
        query = Blog.objects.filter(user=user_ins, block='man').order_by('-id')
        serial = BlogListSerializer(query, many=True)
        blogs = serial.data
    else:
        params['buyer'] = user_ins

    info = UserInfo.objects.filter(user=user_ins)
    info_serial = UserInfoListSerializer(info, many=True, current_user=user_ins)
    info_data = info_serial.data

    show = UserInfoShow.objects.filter(user=user_ins).first()
    show_serial = UserInfoShowListSerializer(show)
    show_data = show_serial.data

    user_data = []
    info_data = info_data[0] if len(info_data) else {}
    for k, v in user_field:
        if k in info_data:
            user_data.append(dict(name=v,
                                  value=info_data.get(k),
                                  en_name=k,
                                  is_show=show_data.get(k, False)))

    attr = UserAttributes.objects.filter(user=user_ins).first()
    context = dict(
        STATIC_URL=settings.STATIC_URL,
        user_data=user_data,
        is_self=is_self,
        is_attention=False if is_self else UserFavorites.objects.filter(attention=user_ins, user=req.user).exists(),
        blogs=blogs,
        level_text=dict(VIP_LEVEL).get(user_ins.info.level, u'菜鸟'),
        user=user_ins,
        attr=attr,
        user_info=info_data,
        favorite_count=UserFavorites.objects.filter(favorite=user_ins).count(),
        attention_count=BlogRelationUser.objects.filter(user=user_ins).count(),
        reply_count=BlogReply.objects.filter(user=user_ins).count(),
    )

    return render(req, html, context)


@login_required()
def qa(req):

    params = req.GET.dict()
    vip_user_id = params.pop('vip_user') if 'vip_user' in params else 0
    offset = params.get('offset', 0)
    limit = params.get('limit', 20)
    queryset = Question.objects.filter(a_user_id=vip_user_id).all()[offset: limit]
    serial = QuestionAnswerListSerializer(queryset, many=True)
    data = serial.data
    context = dict(
        data=data,
        vip_user=User.objects.filter(id=vip_user_id).first(),
    )
    print(data)
    return render(req, 'qa.html', context)


@login_required()
def question(req):

    data = req.POST.dict()
    data['user'] = req.user
    params = dict(
        # user=req.user,
        a_user=User.objects.filter(id=data.get('a_user_id')).first(),
        q_user=User.objects.filter(id=data.get('q_user_id')).first(),
        content=data.get('content')
    )
    ans, is_create = Question.objects.get_or_create(**params)
    return HttpResponseRedirect('/accounts/qa?vip_user=' + data.get('q_user_id'))


@login_required()
def answer(req):

    data = req.POST.dict()
    data['user'] = req.user
    ans, is_create = Answer.objects.get_or_create(**data)
    return HttpResponseRedirect('/accounts/qa')

    # queryset = Question.objects.all()[offset: limit]
    # serial = QuestionAnswerListSerializer(queryset, many=True)
    # data = serial.data
    # context = dict(
    #     data=data,
    # )
    # print(data)


class UserList(ModelViewSet):

    def list(self, request, *args, **kwargs):
        area = request.GET.dict().get('area', None)
        queryset = UserInfo.objects.filter(is_vip=True)
        if area == u'hot':
            queryset = queryset.filter(~Q(source__in=OTHER_AREA))
        elif area == u'otherArea':
            queryset = queryset.filter(source__in=OTHER_AREA)
        elif area:
            queryset = queryset.filter(source=area)

        self.serializer_class = UserInfoListSerializer
        self.queryset = queryset
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        areas = hot_area()
        if page is not None:
            serializer = UserInfoListSerializer(page, many=True, current_user=request.user)
            # ret_data = self.get_paginated_response(serializer.data)
            return render(request, 'rankings.html', dict(
                users=serializer.data,
                count=len(serializer.data),
                areas=areas,
            ))

        serializer = self.get_serializer(queryset, many=True)
        context = dict(users=serializer.data,
                       count=len(serializer.data),
                       )
        return render(request, 'rankings.html', context)