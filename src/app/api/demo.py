# -*- coding: utf-8 -*-
# @Time    : 2025/8/14 上午11:00
# @Author  : liguochun
# @FileName: demo.py
# @Software: PyCharm
# @Email   ：liguochun0304@163.com
from fastapi import APIRouter
from app.utils.response import response
from app.form.demo import Demo

router = APIRouter()

@router.post("/extract", summary="JSON 推理接口")
def extract(body: Demo):
    # if not body.text.strip():
    #     raise ServiceException("text is empty", code=1001, status_code=400)
    result = body.name.upper()
    return response(data={"text": body.name, "result": result})
