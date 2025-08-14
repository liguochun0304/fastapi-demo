# -*- coding: utf-8 -*-
# @Time    : 2025/8/14 上午11:03
# @Author  : liguochun
# @FileName: neo4j.py
# @Software: PyCharm
# @Email   ：liguochun0304@163.com
from pydantic import BaseModel

class Neo4jConfig(BaseModel):
    uri: str = "bolt://localhost:7687"
    username: str = "neo4j"
    password: str = "password"

neo4j_config = Neo4jConfig()
