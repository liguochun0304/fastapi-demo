# -*- coding: utf-8 -*-
# @Time    : 2025/8/14 下午3:02
# @Author  : liguochun
# @FileName: registry.py
# @Software: PyCharm
# @Email   ：liguochun0304@163.com
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any
from app.config.models import model_registry  # 你之前的配置

@dataclass
class ModelSpec:
    name: str
    type: str
    path: str
    params: Dict[str, Any]

class Registry:
    def __init__(self):
        # 允许在 config/models.py 中用最简单的 dict 来登记
        self._specs: Dict[str, ModelSpec] = {}
        for name, info in model_registry.items():
            self._specs[name] = ModelSpec(
                name=info.name if hasattr(info, "name") else name,
                type=info.type if hasattr(info, "type") else info.get("type", "echo"),
                path=info.path if hasattr(info, "path") else info.get("path", ""),
                params=getattr(info, "params", {}) if hasattr(info, "params") else info.get("params", {}),
            )

    def list(self) -> list[str]:
        return list(self._specs.keys())

    def get(self, name: str) -> ModelSpec | None:
        return self._specs.get(name)
