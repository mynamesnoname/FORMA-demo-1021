# FORMA 演示版

[English README](README.md)

FORMA 使用有界的 agentic 图调查 DESI 一维光谱。本仓库是 **demo 版本**：从 FITS 出发，经过 VI 测量、SH 逐线审查、FA 特征投票、类型专属图和 HS 综合比较，**在 RA 之前停止**。输出是带锚红移的暂定 `Type 1 QSO`、`Type 2 QSO`、`ELG`、`LRG/BGS` 候选，或明确弃权；它不是最终分类或缺陷评级。

```text
FITS → VI（CWT、Redrock、高斯拟合）→ SH（逐线审查）→ FA（独立投票）
     → 代码决定类型图入口 → QSO / ELG / LRG-BGS 图 → HS 合并 → HS 跨组比较
     → 暂定结果或弃权；RA 尚未实现
```

## 运行 demo

在仓库根目录使用 Python 3.12。`example/basic/` 已包含五条带标签的示例 FITS。

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e . --no-deps
```

还需在**同一个环境**中安装 DESI Redrock，使 `rrdesi` 出现在 `PATH`。如果已有 Redrock 源码目录，可执行 `python -m pip install -e /path/to/redrock`，再用 `rrdesi --help` 检查。Redrock 模板和启用 archetype 时所需的 archetype 目录属于外部输入，仓库不提供。

复制本机配置模板：

```bash
cp .env.example .env
cp config/analysis_method.example.json config/analysis_method.json
cp config/model_calls.example.json config/model_calls.json
cp config/rule_parameters.example.json config/rule_parameters.json
```

在 `.env` 中填写 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL` 和 `RR_TEMPLATE_DIR`。示例默认 `USE_ARCHETYPES=true`，此时还需填写 `ARCHETYPE_DIR`。请在实际运行的 shell 中确认 `rrdesi` 和目录可访问。三个 JSON 分别管理方法参数、模型调用温度和 ontology 规则参数；示例数值已与本机 demo 配置对齐。`analysis_method.json` 必须保留 `instrument.arms`。`.env.example` 只保留当前 demo 使用的配置项；已有 `.env` 中的旧流水线变量不会影响 demo 路径。

```bash
python demo.py --preflight-only       # 只读取 FITS 标签，不调用 Redrock 或 LLM
python demo.py --samples QSO_116     # 单条光谱
python demo.py                       # 五条：BGS_2、ELG_6、LRG_1、QSO_4、QSO_116
```

`--samples` 可选择上述任意子集；`--output-root DIR` 可指定输出父目录；`--sh-concurrency`、`--fa-concurrency`、`--fa-max-attempts` 控制执行量。完整运行会调用 Redrock 和配置的 LLM 服务，可能耗时并产生费用：**五条示例完整跑一遍通常需要 30–50 分钟**，具体取决于机器和模型服务；只想确认环境是否正常时，先用 `--samples` 跑单条。预检只需要 FITS 读取依赖。每次完整运行都会新建带时间戳的目录，不会续跑或覆盖旧目录。

## 理解产物

默认输出位置为 `.data/output_/demo/<UTC 时间>-<id>/`。首先查看 `index.json`：

```text
<run>/
├── index.json                          整轮状态；每条样本的结果或错误
└── QSO_116/                          每条光谱各有一个目录
    ├── spectrum.png / spectrum.npz     全谱图 / 数值数组
    ├── VI/
    │   ├── features.png                CWT 与高斯拟合特征图
    │   └── measurements/manifest.json  冻结测量与假设引用
    ├── SH/H1/.../lines.csv             每个 Redrock 假设的 ID 绑定线表
    ├── FA/shared/ 和 FA/H*/             特征投票与咨询性检查
    ├── HS/merge_groups/                合并后的候选组
    ├── HS/compare_groups/.../report.md 跨组比较说明
    ├── type_graph_summary.json         路由、存活假设、HS 组与胜出组
    ├── reasoning_tree.json             分支和节点谱系、产物引用
    └── visualization_data.json         供浏览器读取的 VI/SH 投影
```

`index.json` 的 `status: completed` 表示所选样本全部跑完；若部分失败，则为 `completed_with_failures`。每条记录的 `workflow_status` 表示该样本状态；失败记录还包含 `error_type` 和 `error`。成功记录中的 `winner_type`、`winner_redshift`、`winner_group_id` 是 **HS 暂定选择**；`winner_group_id: null` 表示弃权。`truth`、`type_matches_vi` 和 `absolute_vi_redshift_error` 是与 FITS `FIBERMAP` VI 标签的事后对照，不是 HS 的判定输入，也不是独立准确率评估。

对单条样本，先读 `type_graph_summary.json` 的 `hypotheses`、`surviving_hypotheses`、`hs_groups` 和 `hs_comparison`。`hs_comparison.reason` 说明选出或弃权的理由；`ra_review_pending: true` 与 `final_classification_available: false` 标明结论边界。随后沿 `reasoning_tree.json` 的引用进入各 `node.json` 查看具体判断。SH 的 `lines.csv` 保存谱线与 feature 的配对；FA 的独立票据保存特征真实性投票。`stage1_session.md` 等会话 Markdown 保存模型提示和回复。`visualization_data.json` 与图片便于阅读，原始节点产物仍是证据来源。

对一次**成功完成**的运行，可额外生成离线 HTML 节点画廊：

```bash
python scripts/build_demo_node_gallery.py .data/output_/demo/<运行目录>
# 用浏览器打开 <运行目录>/ui/index.html；file:// 可直接使用。
```

画廊展示阶段路径、节点判断、票数及光谱定位，支持中英文切换。它由本次运行产物生成，`demo.py` 不会自动创建。运行结果与画廊均被 Git 忽略；新克隆的仓库需要先运行 demo 才有这些文件。

如果只想先看看完整运行结果长什么样，可以直接打开仓库中预先跑好的五条示例画廊：`example/basic/output/20261019T110542Z-e9a5abd8/ui/index.html`。

## 配置与边界

`config/analysis_method.example.json` 管理仪器范围和测量、审查方法；`config/model_calls.example.json` 管理各阶段采样温度；`config/rule_parameters.example.json` 管理已声明的 ontology 规则参数。运行会记录冻结参数的来源与摘要。`.env` 和本机 `config/*.json` 被 Git 忽略，不要提交密钥。模型提示词位于 `src/FORMA/agentic_graph/prompts/`。

五条光谱是开发示例，不是独立评估集；模型输出可能随运行变化。图止于 HS，不声称已完成 RA 审查、最终报告或最终分类。失败样本可能保留部分阶段产物，以及供排查的 `run_outcome.json`。

## 测试

```bash
python -m unittest discover -s tests/agentic_graph -p 'test_*.py'
python -m unittest discover -s tests/reasoning -p 'test_*.py'
```

许可证：MIT。
