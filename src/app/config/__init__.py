# -*- coding: utf-8 -*-
# @Time    : 2025/8/14 上午10:55
# @Author  : liguochun
# @FileName: __init__.py.py
# @Software: PyCharm
# @Email   ：liguochun0304@163.com
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "iextract-service"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

# 导出其他配置对象
from app.config.llm import llm_config
from app.config.models import model_registry
from app.config.neo4j import neo4j_config

__all__ = ["settings", "llm_config", "model_registry", "neo4j_config"]
