# -*- coding: utf-8 -*-
# @Time    : 2025/8/14 下午3:03
# @Author  : liguochun
# @FileName: loader.py
# @Software: PyCharm
# @Email   ：liguochun0304@163.com
from __future__ import annotations
import asyncio
from typing import Dict, List, Any, Type
from app.models.registry import Registry, ModelSpec
from app.models.pipelines.base import BasePipeline
from app.models.pipelines.echo import EchoPipeline

# 可选映射（transformers 装了才会用到）
try:
    from app.models.pipelines.hf_text import HFTextPipeline
    _HF_AVAILABLE = True
except Exception:
    HFTextPipeline = None  # type: ignore
    _HF_AVAILABLE = False

TYPE_MAP: Dict[str, Type[BasePipeline]] = {
    "echo": EchoPipeline,
}
if _HF_AVAILABLE:
    TYPE_MAP["hf_text"] = HFTextPipeline  # sentiment / tc 等

class ModelLoader:
    """进程内懒加载 + 并发信号量限流"""
    def __init__(self, max_concurrency: int = 8):
        self.registry = Registry()
        self._instances: Dict[str, BasePipeline] = {}
        self._locks: Dict[str, asyncio.Lock] = {}
        self._sem = asyncio.Semaphore(max_concurrency)

    async def load(self, name: str) -> BasePipeline:
        if name in self._instances:
            return self._instances[name]
        spec = self.registry.get(name)
        if not spec:
            from app.utils.exceptions import BaseAPIException
            raise BaseAPIException(code=400, error_code=2001, message=f"模型 {name} 未在注册表中")
        async with self._locks.setdefault(name, asyncio.Lock()):
            if name in self._instances:
                return self._instances[name]
            cls = TYPE_MAP.get(spec.type)
            if not cls:
                from app.utils.exceptions import BaseAPIException
                raise BaseAPIException(code=400, error_code=2003, message=f"不支持的模型类型: {spec.type}")
            inst = cls(**spec.params)
            self._instances[name] = inst
            return inst

    async def unload(self, name: str):
        inst = self._instances.pop(name, None)
        if inst:
            await inst.close()

    async def predict(self, name: str, texts: List[str]) -> List[Dict[str, Any]]:
        m = await self.load(name)
        async with self._sem:
            return await m.predict(texts)
