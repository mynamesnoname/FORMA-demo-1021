"""SH harness entry points reused by the agentic graph.

agentic 图复用的 SH 执行框架入口。

The historical synthesis and report-writer aliases left with the fixed pipeline;
only the Redrock SH runner remains here.
历史综合与报告撰写别名随固定流水线移除；此处只保留 Redrock SH 执行器。
"""

from .single_hypothesis import run, arun

__all__ = ["run", "arun"]
