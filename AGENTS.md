# AGENTS.md — FORMA（demo 分支）

## 项目概述

FORMA 是一个 LLM 驱动的代理系统，对 DESI 一维光谱执行**有界的图引导调查**。当前
（demo）分支只保留 agentic graph reasoning 路径：确定性测量 → 逐假设 SH 线审 → FA
独立投票 → 代码拥有的类型路由 → 类型专属图 → HS 合并 → HS 跨组比较。

输出是**暂定的类型阶段候选**（`Type 1 QSO` / `Type 2 QSO` / `ELG` / `LRG/BGS` 之一加
锚红移），或显式弃权。**图止于 RA 之前**：没有最终分类、最终报告或缺陷评级。

旧固定六阶段流水线与 `_plan/` 计划树不在本分支；它们保留在研究分支
（`feature/agentic-graph-reasoning`、`feature/evidence-graph`）与 Git 历史中。

## 工作流架构

```text
FITS ──VI──▶ 冻结测量 ──SH 线审──▶ FA 投票 ──代码入口路由──▶ 类型图
        (CWT + Redrock；         (ID 绑定 CSV +        (现实性/森林/双线        (QSO / ELG /
         运行级 CWT ID、          判读；无报告、          奇数票配额)             LRG-BGS)
         假设内高斯拟合)          无分类)
  ──▶ HS 合并（同类型 + 精确共享诊断线对）──▶ HS 比较 ──▶ 停止（RA 未实现）
```

关键不变量：

- **代码拥有数值**：模型提交 ID 与判读，程序完成测量投影与校验（`sh_line_review.py`、
  `graph_workflow.py`、各类型图节点）。
- **FA 票不可变**：每票独立会话与独立产物；票满配额后才更新条目的信号状态
  （`fa_feature_reality.py`、`vote_runtime.py`）。
- **入口类型是调查日程**：`type_entry_router.py` 按 `[Ne V]` → QSO 诊断线 → Dn4000/Ca H/K
  → `[O II]/[O III]` 顺序记录全部检查，第一个合格图只是起点；无正向证据时记未决，
  不因模型 `null` 剪枝。
- **分支谱系**：每个节点/尝试写入 `reasoning_tree.json`，含产物相对路径与 SHA-256；回到
  旧节点应创建子分支而非覆盖（`reasoning_trace.py`、`execution_artifacts.py`）。
- **提示词打包**：20 个模型提示词位于 `src/FORMA/agentic_graph/prompts/`，由
  `prompts.PROMPT_DIR` 读取；不要在包外新增运行期文件。

## 仓库结构

```text
src/FORMA/agentic_graph/        # 新图实现（35 模块）+ prompts/ + data/
src/FORMA/agents/multi_agents/
  harness/                      # 被复用的 Redrock SH 执行器、工具、SH 溯源
  utils/                        # FITS 读取、CWT、用量统计
src/FORMA/core/
  config/                       # 声明参数加载（analysis method、model calls、冻结快照）
  reasoning/ontology/           # 版本化本体注册表、查询、规则参数、宽度词汇
  line_status.py  constants.py  llm.py
demo.py                         # 演示入口：预检/单样本/五样本
example/basic/                  # 五个 DESI VI 质量 4 示例光谱
docs/architecture/  docs/graphs/# 本机材料（未跟踪）：契约/参数/示例配置；SH/FA/RA 规则
agenticGraphReasoningDesign/    # 本机材料（未跟踪）：设计说明、Canvas、契约
tests/agentic_graph/  tests/reasoning/
```

## 配置

- `.env`（被忽略）从 `.env.example` 复制：`LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`、
  Redrock 的 `RR_TEMPLATE_DIR`、`ARCHETYPE_DIR`、`USE_ARCHETYPES`、`NMINIMA`、`NNEAREST`。
- 本机方法配置同样被忽略：从示例复制
  `config/{analysis_method,model_calls,rule_parameters}.json`。`analysis_method.json`
  必须保留 `instrument.arms`（FITS 读取需要相机臂配置）。
- 绝对不得提交 `.env` 或本机 `config/*.json`；仓库只跟踪 `.example.json` 模板。

## 构建与运行

```bash
python3.12 -m pip install -r requirements.txt
python demo.py --preflight-only
python demo.py --samples QSO_116
python demo.py
PYTHONPATH=src python -m FORMA.agentic_graph --status
```

注意：`NO_PROXY` 含 `[::1]` 时 httpx 会抛 `InvalidURL: Invalid port: ':1]'`，运行时取消
代理变量；`/dev/shm` 只读时确保 `rrdesi` 指向串行包装器（`--mp 1`）。

## 测试

```bash
python -m unittest discover -s tests/agentic_graph -p 'test_*.py'
python -m unittest discover -s tests/reasoning    -p 'test_*.py'
```

两个测试目录都不是 Python 包（`tests/agentic_graph` 的用例按同级模块互相导入），
因此分别指定 `-s`；不要改用 `discover -s tests`，否则只会找到一个子集或零个用例。

## 代码风格与约定

- Python 3.12，asyncio / `ainvoke` 全异步；`FORMA` 包内绝对导入。
- 注释与 docstring 中英双语，匹配周围风格。
- 配置只经 Pydantic 模型或声明加载器读取；不要在新代码里散落 `os.getenv`。
- 主观质量不能替代证据：新判定需要记录来源、摘要、未决原因与可复现产物。
- 修改提示词只改 `src/FORMA/agentic_graph/prompts/`，并保持 `tests/agentic_graph/
  test_prompt_resources.py` 通过。
- 模型输出具有随机性；不要用单次运行宣称准确率或稳定性。

## 安全

- `.env` 含密钥，始终忽略；`config/*.json` 同理。
- 流水线以子进程运行 Redrock `rrdesi`，并向配置的 LLM 端点发起 HTTPS 请求。
- `.data/`、`test_set/`、`log/` 等为忽略目录；不要把生成产物提交到仓库。
