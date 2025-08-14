# -*- coding: utf-8 -*-
# @Time    : 2025/8/14 上午11:03
# @Author  : liguochun
# @FileName: models.py
# @Software: PyCharm
# @Email   ：liguochun0304@163.com
from pydantic import BaseModel
from typing import Dict

class ModelInfo(BaseModel):
    name: str
    type: str
    path: str

# 这里用字典模拟模型注册表
model_registry: Dict[str, ModelInfo] = {
    "echo-v1": ModelInfo(name="echo-v1", type="demo", path="./weights/echo-v1"),
    "test-v1": ModelInfo(name="test-v1", type="demo", path="./weights/test-v1"),
}
