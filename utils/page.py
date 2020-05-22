#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2020/5/13 下午4:42
# @Author : Zh
# @Project : zh
# @File   : page.py
# @Software: PyCharm


def page_limit(page, page_size):
    try:
        page = int(page) if page else 1
        page_size = int(page_size) if page_size else 10
        return (page - 1) * page_size, page_size * page
    except Exception as e:
        print(' ----------- error -----------', str(e))
        return 1, 10


if __name__ == '__main__':
    print(page_limit(1, 10))
    s, e = page_limit(2, 10)
    print(s, e)