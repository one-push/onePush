#!/usr/bin/env python
# encoding: utf-8

"""
  > FileName: pagination.py
  > Author: Yin
  > Mail: yjd48676@ly.com
  > CreatedTime: 08/08/2018 17:52
"""


class Pagination(object):
    """
    分页
    """

    def __init__(self, total_count, offset=0, limit=10, max_page_num=5):

        self.offset = int(offset)
        self.limit = int(limit)          # 每页显示数据条目数
        self.total_count = total_count          # 数据条目总数
        self.current_page = self.offset/self.limit    # 当前页页码值
        self.max_page_num = max_page_num        # 页码区域最多显示页码数
        if self.current_page == 0:
            self.current_page = 1

    def start(self):
        """开始页"""
        return (self.current_page - 1) * self.limit

    def end(self):
        """结束页"""
        return self.current_page * self.limit

    @property
    def num_pages(self):
        """
        求出总页数
        """
        a, b = divmod(self.total_count, self.limit)
        if b == 0:
            return a
        else:
            return a + 1

    def pager_num_page(self):
        """
        分页区域显示页码范围
        """
        part = self.max_page_num/2
        if self.num_pages < self.max_page_num:
            return range(1, self.num_pages+1)
        elif self.current_page <= part:
            return range(1, self.max_page_num+1)
        elif self.current_page + part > self.num_pages:
            return range(self.num_pages-self.max_page_num, self.num_pages+1)
        else:
            return range(self.current_page-part, self.current_page+part+1)

    def page_str(self):
        """
        html返回到templates，templates中需引入bootStrap的css样式
        """
        page_list = []
        first = u"""<a href='?offset=0&limit=%s'>首页</a>""" % self.limit
        page_list.append(first)
        if self.current_page == 1:
            prev_page = u"""
            <span class="disabled">
                <span aria-hidden="true">&laquo;</span>
            </span>
            """
        else:
            prev_page = u"""
            <a href="?offset=%s&limit=%s" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
            </a>
            """ % ((self.current_page - 1) * self.limit, self.limit)
        page_list.append(prev_page)
        for i in self.pager_num_page():
            if i == self.current_page:
                temp = u"""
                    <a href="#" class="active">%s</a>
                """ % i
            else:
                temp = u"""
                    <a href="?offset=%s&limit=%s">%s</a>
                """ % ((i - 1) * self.limit, self.limit, i)
            page_list.append(temp)

        if self.current_page == self.num_pages:
            next_page = u"""
                <span class="disabled">
                    <span aria-hidden="true">&raquo;</span>
                </span>
            """
        else:
            next_page = u"""
                <a href="?offset=%s&limit=%s" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                </a>
            """ % ((self.current_page + 1) * self.limit, self.limit)
        page_list.append(next_page)
        last = u"""<a href='?offset=%s&limit=%s'>尾页</a>"""\
               % ((self.num_pages - 1) * self.limit, self.limit)

        page_list.append(last)
        return u''.join(page_list)
