#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: serivice.py.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 04/08/2018 11:24
"""

import random
from datetime import datetime
from account.models import ACTION_SCORE, LEVEL_SCORE
from account.models import UserScore


def created_code():
    """
    创建code 格式 yy mm dd random HH MM SS
    年月日一位随机数时分秒
    :return:
    """
    now = datetime.now()
    code = [
        now.strftime('%Y%m%d'),
        str(random.randint(0, 9)),
        now.strftime('%H%M%S')
    ]

    return ''.join(code)


def update_score(user=None, action=None, blog_id=None):
    """
    积分/LEVEL变动
    TODO: 说说谁有理，发表评论(博客评论已加)，点赞或倒 未加
    :param user:
    :param action:
    :return:
    """
    if not user or not action:
        return

    score = ACTION_SCORE.get(action, 0)
    total = user.info.score + score
    data = dict(
        user=user,
        total=total,
        block=action,
        score=score,
        ref_id=blog_id
    )

    ins = UserScore.objects.create(**data)
    if not ins:
        return

    user.info.score = total
    # 更新用户level
    for level, val in dict(LEVEL_SCORE).items():
        lev_min, lev_max = val
        if level < user.info.level:
            continue

        if (lev_max == -1 and total >= lev_min) or (lev_min <= total < lev_max):
            user.info.level = level
            break

    user.info.save()
