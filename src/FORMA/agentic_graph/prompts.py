"""Packaged prompt resources for the agentic graph.

agentic 图的打包提示词资源。

The model-facing prompts are data files shipped with the package.  They are read at
runtime by the SH line review, FA vote nodes, QSO report, HS merge/comparison and the
LRG/BGS targeted Ca review, so they live here instead of a design directory that a
demo checkout may not carry.

面向模型的提示词随包分发的数据文件。它们由 SH 线审、FA 投票节点、QSO 报告、HS 合并/比较与
LRG/BGS 定向 Ca 复核在运行时读取，因此放在包内，而不是可能不随 demo 检出的设计目录。
"""

from pathlib import Path

#: Directory holding the packaged ``*.md`` prompt files.
#: 打包 ``*.md`` 提示词文件所在目录。
PROMPT_DIR = Path(__file__).resolve().parent / "prompts"
