# -*- coding: utf-8 -*-
# @Time    : 2025/8/14 下午3:03
# @Author  : liguochun
# @FileName: re_extract.py
# @Software: PyCharm
# @Email   ：liguochun0304@163.com
from __future__ import annotations
from typing import Any, Dict, List
from .base import BasePipeline
from app.utils.exceptions import BaseAPIException

class HFTextPipeline(BasePipeline):
    """
    通用 text-classification 演示。params:
      - task: 默认 'sentiment-analysis'
      - model: 模型名或路径
      - device: -1/0/1 ...
    """
    def __init__(self, **params):
        super().__init__(**params)
        try:
            from transformers import pipeline
        except Exception:
            raise BaseAPIException(
                code=500, error_code=2002,
                message="transformers 未安装，请在 requirements 中启用或 pip install transformers"
            )
        task = self.params.get("task", "sentiment-analysis")
        model = self.params.get("model", "distilbert-base-uncased-finetuned-sst-2-english")
        device = int(self.params.get("device", -1))
        self._pl = pipeline(task=task, model=model, device=device)

    async def predict(self, texts: List[str]) -> List[Dict[str, Any]]:
        preds = self._pl(texts)
        # pipeline 对单条/批量返回形态不同，做一下统一
        if isinstance(preds, dict):
            preds = [preds]
        results = []
        for t, p in zip(texts, preds):
            results.append({"text": t, "result": p})
        return results
