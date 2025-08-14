# -*- coding: utf-8 -*-
"""
FastAPI 版本的全局异常类 + 处理器
保留原有 BaseAPIException 设计，兼容 Flask 项目的字段
"""
import json
from fastapi import Request
from fastapi.responses import JSONResponse


class BaseAPIException(Exception):
    """
    基础 API 异常类
    - code: HTTP 状态码（默认 200，方便接口层不走 HTTP 错误）
    - error_code: 业务错误码
    - message: 错误信息
    """
    code = 200
    error_code = -1
    message = "服务器未知错误"

    def __init__(self, code: int = None, message: str = None, error_code: int = None):
        if code is not None:
            self.code = code
        if message is not None:
            self.message = message
        if error_code is not None:
            self.error_code = error_code

    def to_dict(self):
        """返回 JSON 可序列化字典"""
        return {
            "code": self.error_code,
            "message": self.message
        }


class UnknownException(BaseAPIException):
    """未知错误"""
    code = 500
    error_code = -1
    message = "服务器未知错误"


class ContentTypeException(BaseAPIException):
    """Content-Type 不支持"""
    error_code = -2
    message = "不支持的 content-type 类型"


# ========== FastAPI 全局异常处理器 ==========

async def base_api_exception_handler(request: Request, exc: BaseAPIException):
    """
    捕获 BaseAPIException 及子类
    返回统一 JSON 格式
    """
    return JSONResponse(
        status_code=exc.code,
        content=exc.to_dict()
    )


async def global_exception_handler(request: Request, exc: Exception):
    """
    捕获未处理的其他异常（兜底）
    """
    # 生产环境可以加日志
    return JSONResponse(
        status_code=500,
        content={
            "code": -1,
            "message": "服务器未知错误"
        }
    )
