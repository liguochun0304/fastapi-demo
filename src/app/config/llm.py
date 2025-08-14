# -*- coding: utf-8 -*-
# @Time    : 2025/8/14 上午11:03
# @Author  : liguochun
# @FileName: llm.py
# @Software: PyCharm
# @Email   ：liguochun0304@163.com
from pydantic import BaseModel

class LLMConfig(BaseModel):
    provider: str = "openai"
    api_key: str = "your-api-key"
    model_name: str = "gpt-3.5-turbo"

llm_config = LLMConfig()
