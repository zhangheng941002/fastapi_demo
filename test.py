#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2020/5/13 下午4:50
# @Author : Zh
# @Project : zh
# @File   : test.py
# @Software: PyCharm

def sn_to_usernmae(sn):
    _sn = sn[8:]
    username = ["42{_type}{sn}".format(_type=i, sn=_sn) for i in ['41', '51', '52', '42']]
    print(tuple(username))


sn_to_usernmae("csn-4230000001")