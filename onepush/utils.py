#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: utils.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 06/08/2018 16:50
"""

from datetime import datetime

DAY_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def format_datetime(dt):
    """
    Args:
        dt:
    Returns:

    """
    return dt.strftime(DATETIME_FORMAT)


class DisableCSRF(object):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)