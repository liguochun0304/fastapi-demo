# -*- coding: utf-8 -*-
# @Time    : 2025/8/14 上午10:59
# @Author  : liguochun
# @FileName: demo.py
# @Software: PyCharm
# @Email   ：liguochun0304@163.com

from pydantic import BaseModel, Field


class Demo(BaseModel):
    name: str = Field(..., description="名称")
    author: str = Field(None, description="作者")