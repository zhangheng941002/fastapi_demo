#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2020/5/13 下午3:00
# @Author : Zh
# @Project : zh
# @File   : main.py
# @Software: PyCharm

from fastapi import FastAPI
from views.query_views import router
from app.settings import TITLE, DESC, VER, DOCS_URL, REDOC_URL

app = FastAPI(
    title=TITLE,
    description=DESC,
    version=VER,
    docs_url=DOCS_URL,  # 文档接口URL
    redoc_url=REDOC_URL  # 文档接口二
)

app.include_router(router)


if __name__ == '__main__':
    import uvicorn

    # 不知道为什么加入reload后workers就失效了
    # uvicorn.run('main:app', host='0.0.0.0', port=9999, workers=4)
    uvicorn.run('main:app', host='0.0.0.0', port=9999, reload=True)
