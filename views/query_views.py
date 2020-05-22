#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2020/5/14 上午10:09
# @Author : Zh
# @Project : zh
# @File   : query_views.py
# @Software: PyCharm

from fastapi import APIRouter

from fastapi import Query, HTTPException
from pydantic import BaseModel
from fastapi import status
from typing import List


from utils.db_utils import DBReader
from db.sql import name_data, data_format, sql_name_format
from utils.page import page_limit

from basemodels.response_models import SuccessResponse, FailureResponse

router = APIRouter()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


def sn_to_username(sn):
    _sn = sn[8:]
    username = ["42{_type}{sn}".format(_type=i, sn=_sn) for i in ['41', '51', '52', '42']]
    return username


@router.get("/",
            status_code=status.HTTP_200_OK,  # http 状态码
            response_description='''

                    2020

            ''',
            summary="路由的介绍",
            )
def read_root():
    response = SuccessResponse()
    response.result = {"Hello": "World"}
    return response


@router.get("/query/{sql_name}",
            status_code=status.HTTP_200_OK,

            response_description='''
            
                    "query_resource_by_sn": "通过sn查询资源信息",
                    "query_resource_by_order_no": "通过订单编号查询资源信息",
                    "query_radius_attr_by_sn": "通过sn查询radius属性", page_size:12， 可用参数：csn-4230000254
                            
            
            ''',
            summary="查询",

            )
async def query(sql_name: str = "", sn: str = None, order_no: str = None, page: int = 1, page_size: int = 10):
    sql = name_data.get(sql_name, None)
    if not sql:
        raise HTTPException(status_code=404, detail="page not find!")
    _data_format = data_format[sql_name]
    _name = sql_name_format.get(sql_name, None)
    db = DBReader()
    username = ""
    if sql_name == "query_radius_attr_by_sn":
        username = sn_to_username(sn)
    _username = ()
    if username:
        _username = tuple(username)
    _data = {
        "sn": sn,
        "order_no": order_no,
        "username": _username
    }
    _SQL = sql.format_map(_data)
    if sql_name == "query_radius_attr_by_sn":
        page_size = 12
    print(_name, _SQL)
    resp = db.readList(_SQL)
    counts = 0
    results = []
    if resp:
        counts = len(resp)
        s, e = page_limit(page=page, page_size=page_size)
        for each in resp[s: e]:
            _result = {_data_format[i]: each[i] for i in range(len(each))}
            results.append(_result)

    return {"sql_name": sql_name, "name": _name, "page": page, "page_size": page_size, "counts": counts,
            "result": results}


@router.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@router.get('/test',
            response_description=
            '''
            {
            "id": 3,    #课程id
            "name": "五年级语文",  #课程名称
            "subject": "语文"    #课程科目
            }   
            ''',
            summary="查找课程列表",
            )
async def test(can_query: List[str] = Query(
    ["query_resource_by_sn", "query_resource_by_order_no", 'query_radius_attr_by_sn'])):
    print(can_query, '----------------')
    print(can_query[0], '=================')
    return {}
