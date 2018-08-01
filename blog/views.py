# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import render


# @login_required()
def area(req):
    context = dict()
    return render(req, 'rankings.html', context)