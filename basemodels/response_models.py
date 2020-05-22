#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2020/5/16 下午12:15
# @Author : Zh
# @Project : zh
# @File   : response_models.py
# @Software: PyCharm

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    code: int = 1
    msg: str = "success"
    result: dict = {}


class FailureResponse(SuccessResponse):
    code: int = 0
    msg: str = "failure"
