# FORMA FA 感知模块：从 LLM Vote 到专用 ML 的数据与窗口设计

**日期：** 2026-10-24  
**状态：** 设计讨论整理 / Experimental Design Draft（尚未实施或完成验证）  
**适用范围：** FORMA demo 的 FA Feature Reality，涉及 VI/CWT、Gaussian Fit、SH 与下游类型调查。  
**相关文档：** [DESIGN_ASSESSMENT_2026-10-22.md](./DESIGN_ASSESSMENT_2026-10-22.md)

> 本文记录讨论达成的方向、当前仓库已经存在的实现、拟开展的实验，以及尚未确定的超参数。它**不是**训练效果报告或既定实现规范。以下提到的 100/2000 条光谱、分箱阈值、512 点等均为实验候选值，不是已验证的最佳设置。

## 0. 一页结论

1. **研究目标保持不变。** FORMA 不是要替换 Redrock、QuasarNET 或专业光谱 Pipeline；它研究的是专家 VI 中的 **Evidence Synthesis、Investigation Orchestration、Auditable Verification**。专用 ML 可以替换低层 *perception backend*，Agent 仍负责证据整合与调查调度。
2. **目前最直接的痛点是 FA Reality 的假阴性。** 经用户近期试验，LLM Vote 对平缓、宽的真实发射特征（重点为 C IV、C III]）可能误判为不存在，且不稳定的科学代价较高。这个观察目前是定性发现，需保留案例并量化。
3. **原始数据保留全谱，训练与预测使用局部窗口。** 全谱与专家标注窗口独立存储；训练/预测执行同一 Window Extraction Policy。只有将来要直接承担全谱 Candidate Detection，才进一步考虑全谱或滑窗定位网络。
4. **优先实验专用轻量 ML。** 用统计特征 + boosted trees 和 small 1D CNN 比较现有 LLM Vote；不预设神经网络必然更准。
5. **重点实验用户提出的 FWHM-binned Windowing。** 按 CWT/Gaussian Fit 测得的 FWHM 选观察尺度，再重采样为固定输入长度。要为大于 2000 km/s 的宽线、错误线宽、无效测量和窗口边界设计回退。
6. **不要把模型分数等同于科学置信度。** 需要独立标注、校准、针对宽线的漏检评估、弃权策略，以及对最终 FORMA 调查流程的影响测量。

---

## 1. 背景：为什么尝试替代 LLM FA Vote

### 1.1 原始 Vote 设计：隐式弃权，而非简单多数决

用户解释过，原先每个 LLM Session 必须在 `yes/no` 中作答，不直接给模型 `abstain`，以避免模型倾向于选择安全的显式弃权。执行框架再根据独立会话的三票样本构造四档：

| Yes/Total | Yes fraction | 设计语义 | 期望的系统动作 |
| --- | ---: | --- | --- |
| 0/3 | 0 | Assured No | Reject |
| 1/3 | 1/3 | Contested, leaning No | Abstain / unresolved |
| 2/3 | 2/3 | Contested, leaning Yes | Abstain / unresolved |
| 3/3 | 1 | Assured Yes | Accept |

原设计中的四个比例区间为 `0–0.25`、`0.25–0.50`、`0.50–0.75`、`0.75–1`（最终实现时需要规定端点归属）。三票时恰好落在以上四个离散点。

用户初步人工比对观察到：0/3、3/3 的判断多数与个人检查一致；1/3、2/3 与个人检查一致的情况大约各占一半。**这是探索性人工观察**，没有给出经过仲裁的标注集、样本数、置信区间或科学错误率，不能视为对 Assurance Calibration 的验证。

统计解释：在固定输入数据 `D` 和模型配置 `M` 下，每次 LLM 的 `P(vote=yes | D,M)` 是模型的**条件输出分布**；给定 `D,M` 后的独立采样在理论上可以成立，但重复投票不等于获取了新的独立光谱证据。采样一致性不等同于真实特征概率。同一模型可能对某种噪声或宽线形态稳定地犯错。

### 1.2 当前实现与设计意图的落差

核查文件：
- `src/FORMA/agentic_graph/feature_registry.py`：`cast_vote()` 计算 `yes_fraction`、`assurance=assured/contested`；但 `observed_signal_state` 仍通过 **Yes 是否超过半数** 写成 `signal_present/signal_absent`。
- `src/FORMA/agentic_graph/cleaned_line_view.py`：`signal_present → adopted`，`signal_absent → rejected_measurement`；未直接将 `contested` 映射为 unresolved。
- `src/FORMA/agentic_graph/type_entry_router.py`：可使用 `cleaned_pairing == adopted` 作为后续调查入口证据。
- `src/FORMA/agentic_graph/fa_feature_reality.py` 和 `prompts/fa_real_feature_system.md`：单个投票禁止根据红移、谱线名称及天体类别决策，只针对观测特征的存在性。

因此，当前仓库的**执行状态**与用户所期望的「分票通常视为 Abstain」**不完全一致**。这属于需单独处理的下游语义问题，并不是 ML 模型自动能修复的缺陷。

### 1.3 新的经验性失败模式

用户近期进一步发现：FA Vote 仍然不稳定，尤其是较平缓的 C IV / C III] 宽发射线存在被误判 `absent` 的风险。方向因而转为先验证专用数值模型是否更擅长一维谱线形态识别。

有必要分解失败发生的位置：

```text
Full Spectrum
  → CWT / Gaussian Fit：是否提出候选？         [Candidate Detection Recall]
  → SH：是否正确保留/关联候选？                 [Association / Pairing]
  → FA：已有候选是否被错误否决？                [Feature Reality Recall]
  → Type Graph / HS：误差是否导致错误结论？     [End-to-End Verification]
```

仅替换 FA 分类器无法挽回**从未进入 FA 候选集**的真实宽线。因此要额外建立从专家谱线位置出发的 *line-centered* 评估集。

---

## 2. 明确 ML 任务边界

**第一阶段任务：Candidate-centered Spectral Feature Reality。**

输入：候选中心、候选类型（emission/absorption）、邻域一维光谱数值（flux、噪声/IVAR、mask、波长坐标），可选候选测得线宽等 metadata。

输出：特征真实性的模型分数，以及由执行策略决定的 `accept/reject/unresolved`。不由该模型直接预测 Redshift、C IV/C III] 身份、QSO 类型或最终分类。

不应将下列不同问题混为一个标签：
- **Reality:** 观测中是否确实存在 coherent local feature？
- **Identity:** 该观测特征是否可以解释为特定谱线？
- **Physical origin:** 是天体信号、天空线残差、仪器效应还是其他来源？
- **Classification:** 是否足以判断对象类型？

FA 第一版只解决 *reality*；SH、Ontology Rule、Type Graph、HS 继续处理后续语义和竞争假设。

建议 Window Label：
- `real_emission`
- `real_absorption`
- `artifact_or_noise`
- `uncertain`（人类也无法清楚确定）
- `unassessable`（缺乏足够有效数据）

初版也可按 emission/absorption 分任务训练二分类；`uncertain` 和 `unassessable` 不应被强制归入负样本。另存 `broad/narrow`、blend、非对称、BAL 等**形态属性**。训练时正样本不能只来自理想、高 SNR 的明显峰。

## 3. 数据保存形式：Full Spectrum 是 Source of Truth；Window 是 Sample

### 3.1 明确的选择

| 环节 | 保存/输入 |
| --- | --- |
| 原始训练数据仓库 | **完整一维光谱** + 人工标注区域/中心 + Label + 来源与版本 |
| 模型训练 | 从全谱**动态提取**候选附近窗口，按一致的 Policy 预处理 |
| 模型推理 | 从实际 CWT / Gaussian Fit 候选中心**提取同种窗口** |
| 扩展上游漏检检测 | 可从人工确认的理论/观测线位，或额外 Sliding Windows 生成候选 |

不建议只保存固定裁剪好的 NumPy 窗口或 PNG：否则改变窗口尺度、归一化与插值时，需要回溯重建数据。应始终能追溯到完整源光谱。

### 3.2 建议数据字段

**Spectrum-level：**
- `spectrum_id`、`target_id`，可能还有 observation/exposure/group ID；
- wavelength、flux、IVAR/uncertainty、pixel validity/mask、仪器臂与适用的分辨率数据；
- raw source path / checksum / processing release；经专家确认的 redshift、spectype 可以留作**审计或分层元数据**，不作为第一版 FA Reality 输入；
- 保存是否缺失可靠 IVAR。不要将 assumed SNR 伪装成真实噪声测量。

**Window-level（人工标注）：**
- `window_id`、`spectrum_id`、`annotation_center_angstrom`；
- `annotation_left/right`（人工指出的特征范围；**不是模型输入边界**）；
- `label`、`profile`、`quality`、`annotator_id`、`review_status`；
- `line_identity_for_audit`（若已知，仅用于分组与失效分析）；
- `candidate_origin`: CWT / Gaussian Fit / predicted-position / manual；
- `candidate_center`、`measured_fwhm_kms`、`fwhm_source`、`fwhm_quality`（对 FA 的实际输入和偏差分析都重要）。

**标注注意：** 人工知道的真实中心与真实宽度，**不能直接取代推理时不可靠的 CWT/Gaussian Fit 输出**来构造训练窗口，否则训练数据过于理想；需要复现真实候选中心的误差，或做显式中心扰动增强。单独保留 `expert_fwhm_kms` 只用于审计。

### 3.3 目录草案（未来数据产物，不建议直接提交大体积观测文件）

```text
dataset/
  spectra/
    <spectrum_id>.npz                  # 原始/可追溯全谱
  annotations/
    windows.parquet                    # 标签、坐标、形态与审核状态
    adjudications.parquet              # 多人标注、分歧和仲裁
  splits/
    train_spectra.txt
    val_spectra.txt
    test_spectra.txt
  preprocessing/
    window_policy.yaml                # 版本化窗口与归一化规则
```

实际大规模观测数据建议保存在独立存储/数据集服务；Git 仓库记录 Schema、配置模板、构建脚本、校验与数据索引，而不是直接纳入大量 FITS/NPZ 或专家工作资料。

### 3.4 训练/推理一致性

```python
# Schematic only; not an existing FORMA API.
spectrum = load_spectrum(spectrum_id)
window = extract_window(
    spectrum,
    candidate_center=center_from_actual_measurement,
    measured_fwhm_kms=fwhm_from_actual_measurement,
    config=frozen_window_policy,
)
score = model(window.values, window.metadata)
decision = calibrated_policy(score, window.quality)
```

同一个 `extract_window` 必须用于训练和推理；模型的预处理版本、权重版本、噪声处理、mask、重采样参数都应进入可审计元数据。

---

## 4. 用户提出的 FWHM-binned Adaptive Window

### 4.1 原始提案（需保留，不能误写成既定模型参数）

根据 CWT / Gaussian Fit 提供的 **measured FWHM** 将候选分为三档：

| Measured FWHM | 观察尺度（用户提案） | 截取**总**窗口速度宽度 | 半宽 |
| --- | --- | ---: | ---: |
| < 1000 km/s | Narrow / scale-1000 | 1000 × 3 = 3000 km/s | ±1500 km/s |
| 1000–1500 km/s | Transition / scale-1500 | 1500 × 3 = 4500 km/s | ±2250 km/s |
| 1500–2000 km/s | Broad / scale-2000 | 2000 × 3 = 6000 km/s | ±3000 km/s |
| ≥2000 km/s | **原提案尚未覆盖** | 需新档位或 fallback | 需定义 |

随后将每个速度窗口重采样为固定 `N` 点（例如 `N=512`），作为 FA 模型的局部数值输入。这里的「×3」明确指**总窗口宽度**，不是在中心左右各取 ×3。

**设计亮点：**
- 避免所有候选一律使用相同 Å 观察范围；
- 输入尺度和实际已测宽度大致匹配；
- 采用分档而非完全连续的 FWHM 缩放，减弱小幅拟合噪声造成的窗口尺度抖动；
- 训练/推理均能够复用已有 CWT 和 Gaussian Fit 的 measured FWHM，无需额外 LLM 判宽。

**注意概念边界：** 这是**感知模型的 window-scale buckets**，不是严格的谱线物理分类。现有 `src/FORMA/core/reasoning/ontology/feature_width.py` 已有 measured narrow/intermediate/broad 词汇，它的阈值由 formal rules 管理；新窗口策略不应该偷偷修改 Ontology 分类或复用名称而赋予不同语义。建议使用独立字段 `window_scale_id`。

### 4.2 为什么尤其需要扩展 >2000 km/s

用户的主要痛点是 C IV、C III] 等较宽、平缓的 QSO 发射线，这些线的实际宽度可远大于 2000 km/s。对于最后一个「broad」档简单固定总窗口 6000 km/s，可能只能看到中心凸起、看不到足够连续谱或线翼。

建议与原始三档一同测试的**扩展候选**（非最终决定）：

| Measured FWHM | 总窗口速度宽度 |
| --- | ---: |
| <1000 km/s | 3000 km/s |
| 1000–2000 km/s | 6000 km/s |
| 2000–4000 km/s | 12000 km/s |
| 4000–8000 km/s | 24000 km/s |
| ≥8000 km/s / measurement unavailable | 明确的超宽线或缺测 fallback |

此扩展方案与用户原始的 1000–1500、1500–2000 两档**不同**；要通过 Ablation 而非主观选择决定保留哪种边界。

### 4.3 速度窗口与波长窗口的转换

对于候选观测中心 `lambda_c` 和总速度宽度 `W_v`，可以用局部非相对论近似：

```text
total_wavelength_width ≈ lambda_c * W_v / c
window ≈ [lambda_c - 0.5 * total_wavelength_width,
           lambda_c + 0.5 * total_wavelength_width]
```

也可在 `v = c ln(lambda/lambda_c)` 的相对 log-wavelength 坐标中构造对称速度窗口。两种定义在小速度下近似一致，**实现必须选择一种固定规则并版本化**。波长必须使用观测波长，不要混用 rest 和 observed FWHM。

示例：`lambda_c = 5000 Å`，总宽度 `W_v=3000 km/s`，对应总波长范围约 50 Å。模型若直接重采样为 512 点，可能大量依赖插值；**插值不提供新的独立观测信息**。应同时比较 128、256、512 点，保留原始有效采样数、mask 与噪声信息。

### 4.4 必须防范的三种风险

**(A) FWHM 系统性低估 → 截错窗口。** 宽而平缓的真实 C IV 可能只让 CWT 检出线内部的小凸起；估计 FWHM 偏小，窗口因此仅覆盖真实线的一小段。恰好会延续当前宽线漏检问题。需要 `measured_fwhm / expert_fwhm` 误差分析、中心偏移增强，以及 FWHM 不可靠时扩大窗口/多尺度回退。

**(B) 归一化后丢掉物理尺度。** 3000 与 24000 km/s 都重采样成相同点数，外观可能趋同；必要时给模型额外输入 measured FWHM、observed center、window width、原始像素数、有效样本数和局部分辨率。不要假设归一化输入能独立重建真实线宽。

**(C) 固定倍率无法处理复杂剖面。** C III] blend、C IV 不对称/BAL、continuum fitting 的宽线削弱、skyline residual 可能无法被单一 3×FWHM 窗口正确表达。使用更宽的上下文和原始 flux / residual 双路输入进行对照。

### 4.5 与多尺度输入的区别

- **Binned single-window（用户提案）**：选择一档，仅看一个尺度；成本较低，依赖 FWHM 的质量。
- **Multi-scale（替代方案）**：同时看局部峰形与更宽连续谱；成本稍高，但可能对测宽误差更鲁棒。
- **FWHM-binned + wider fallback**：折中方案；普通对象只用单尺度，测量不可靠或预测未决时升级到更大尺度。

需要对 C IV/C III] 特定困难样本做直接的错误率对比，而不是仅看全体窗口 Accuracy。

---

## 5. 数据集采样与人工标注：先小样本，后扩展

### 5.1 不要只选成功进入 FA 的候选

建立两个互补的集合：

1. **Candidate-centered**：原始 CWT/Gaussian Fit/SH 成功提出的候选，标注真实/伪特征；直接评估「替换 FA 是否有效」。
2. **Line-centered**：从专家确认红移和目标线位出发，包含 CWT、SH 未找到但确实存在的宽线；用来测量上游 **Candidate Detection Recall**。预测时若由已知红移假设提供预期中心，这本身仍是 agent 选择调查位置，而非模型知道最终谱线身份。

特别保存 FA **0/3 或 1/3 误拒绝的真实宽线**，并补充形态相似的噪声、天空线和 continuum 伪峰作为难负例。但不要只用这些困难个案训练，否则可能不符合实际 VI 的分布。

### 5.2 标注准则建议

- 标注可观测的 **coherent emission/absorption feature**，与物理谱线身份分开。
- 不确定/遮挡/无有效数据要能单独标注，不许假定「没有检测到 = 不存在」。
- 同一候选允许多个独立标注者，记录分歧、仲裁与注释。
- 人工标记的 true width、center 和线身份仅供监督/误差分析；训练特征要模拟实际执行时可获取的 noisy measurement。
- 做 Blind Review 时尽可能减少已有 LLM Vote、Pipeline 推断对人工判读的锚定影响。

### 5.3 样本规模和划分

先尝试 **100–200 条**标注光谱（特别增加约 50–100 条具有宽发射线的 QSO），检查 Label Protocol 与上游漏检比例；再决定是否扩充至**约 2000 条**。

一个纯粹作为抽样讨论起点的 2000 条配比：QSO 800、ELG 400、LRG/BGS 400、针对困难情形的额外 400。困难样本可能与类别重叠；应分开记录对象类型与选样理由，不把此配比视为真实总体比例。

可从 DESI 的专家 VI Catalog 选目标并回溯谱数据，但**对象级** VI 分类/红移不等于每个局部窗口的存在性真值；仍需逐窗口人工标注。

建议按 target/spectrum/重复观测分组划分 Training/Validation/Test，例如 70/15/15。来自同一目标或强相关观测的所有窗口必须留在同一个 split。保留独立的、尽可能代表实际生产分布的测试集；另建 broad-line stress test。窗口数量可能远大于光谱数量，但不意味着获得同样多的独立观测对象。

---

## 6. 模型与窗口 Ablation 计划

在同一批标注、同样的数据划分和同样的候选集合上比较：

| Arm | Perception model | Window policy | 回答的问题 |
| --- | --- | --- | --- |
| A | 现有单次或三次 LLM Vote | 当前约 ±100 Å 输入 | 现有错误、调用成本 |
| B | Engineered features + LightGBM / XGBoost | 统一固定局部窗口 | 便宜的数值 baseline |
| C | Small 1D CNN | 统一固定速度/波长窗口 | 神经网络是否能识别宽线 |
| D | 同一个 1D CNN | **用户原始三档 FWHM window** | 三档缩放有无收益 |
| E | 同一个 1D CNN | **扩展 FWHM window buckets** | >2000 km/s 宽线是否改善 |
| F | 双尺度 1D CNN / fallback | FWHM-binned + wider context | 是否更不依赖测宽准确性 |

窗口 Policy 单独消融，尽量不同时改变网络容量、优化策略或标注分布。模型使用原始 flux、IVAR/噪声、mask、相对波长作为基本数值通道；可加 continuum/residual 做对照，但不要只喂可能抹平 broad wings 的 residual。

评估应至少包含：
- **Broad-line Recall**，单独按 C IV、C III] 和 FWHM、SNR、波长/arm 分层；
- False acceptance of noise/artifacts；Precision-Recall 与不同操作阈值；
- CWT/SH 提出候选的覆盖率（避免把上游漏检算作 FA 分类错误）；
- 输入窗口有效像素数、中心偏差、测宽偏差与模型错误的关联；
- Calibration、selective risk 与 coverage（接受/拒绝/未决的比例及错误率）；
- 每候选 latency / GPU or CPU cost，及最终 FORMA Pipeline 的 Wall Time；
- 下游 Type Graph/HS 的结果变化，尤其错误 Reject 是否造成科学结论错误。

**错误代价应非对称建模：** 对有合理支持但较平缓的真实宽线，不应仅因模型不够自信便肯定「不存在」。可能优先 `unresolved` 或增加调查尺度；策略阈值必须由独立数据校准，不能凭经验宣称可靠。

---

## 7. 与现有 FORMA 代码的整合边界

### 7.1 已核对的相关实现

- `src/FORMA/agentic_graph/fa_feature_reality.py`  
  读取观测窗口；将 wavelength/flux/usability 渲染为 Markdown，测得 FWHM 作为文本参数。这里是替换 LLM perception backend 的主要候选入口。
- `src/FORMA/core/config/analysis_method.py`  
  `AuditMethod.feature_read_half_angstrom` 默认 **100 Å**（即当前 FA 的 ±100 Å）；以后可在并行的新 ML Window Policy 中声明速度窗口，不应混改老 LLM 提示词参数。
- `src/FORMA/agents/multi_agents/utils/cwt_feature_finder.py`  
  CWT 产生 `FWHM_km_s`，并基于滤波 continuum/residual 搜索多尺度峰；须排查特别宽特征在预处理阶段被削弱的可能性。
- `src/FORMA/agentic_graph/sh_measurement_refs.py`、`vi_measurements.py`  
  CWT 与 hypothesis-scoped Fit Measurement Catalog，包含 candidate IDs、`adoptable` 与测量源。
- `src/FORMA/agentic_graph/feature_registry.py`  
  冻结已采纳的 SH 对应测量，记录 FWHM 来源与 Vote 结果；现有 `assurance` 标记不等于完整的隐式弃权语义。
- `src/FORMA/core/reasoning/ontology/feature_width.py`  
  科学语义上的 measured width band，不能与 model window scale 混淆。
- `src/FORMA/agentic_graph/cleaned_line_view.py`  
  FA 的 `observed_signal_state` 投影到下游 `cleaned_pairing`；需要保留 unknown/unreviewable 的区别。

### 7.2 建议的长期接口（草案）

```text
Frozen VI Measurement / Candidate Ref
    ↓
WindowSelector(policy_version, measured_center, measured_fwhm, quality)
    ↓
SpectralWindow(flux, ivar, mask, velocity_offsets, metadata, source_refs)
    ↓
FA Perception Backend (LLM baseline | boosted trees | 1D CNN)
    ↓
Score + Calibration / Confidence Diagnostics
    ↓
Decision Policy (accept | reject | unresolved)
    ↓
Cleaned Line View / Type Investigation / HS
```

将「模型的连续分数」「模型输出稳定性」「科学证据接受/拒绝/未决」拆开记录；不应把分数直接当作谱线真实性的概率或独立证据。执行框架继续负责 Hard Gate、调查升级和 Evidential Trace。

每次决策建议保留：`measurement_id`、`spectrum_sha256`、`window_policy_version`、`model_id/version`、`input_window_sha256`、`measured_fwhm_kms`、`score`、`decision_policy_version`、`evidence_decision`、`unresolved_reason`。

### 7.3 明确不包含在本次变更

本文是设计评估；**没有**新增标注数据、训练脚本、模型权重，**没有**修改 FA 的线上行为、SH/FA/HS Prompt、Ontology、Hard Gate 或 Graph Routing。所有 Window Bucket 都待实验确认。

---

## 8. 尚待确认的问题

1. 用户原提案的 1000/1500/2000 km/s 边界是否保留，还是应该主要按更广泛的 QSO broad-line 分布扩展？
2. 3×FWHM 的**总**窗口是否足够覆盖连续谱与翼部？对哪些谱线或线型不够？
3. 输入重采样点数取 128、256、512 哪一个合算？如何保存插值相关性和原始采样信息？
4. 实际 Gaussian Fit / CWT 的 FWHM 偏差分布如何？宽线漏检中究竟多少来自测量、SH 配对还是 FA？
5. 当 candidate measured FWHM 不可靠或缺失时，使用通用宽窗口、多个尺度还是直接升级人工/LLM？
6. FA 模型是否只检查 candidate reality，还是同时支持由 Hypothesis 引导、但上游未提出的理论波长位置？
7. 标注中的宽线和高 SNR 假峰如何定义真假？多人检查的一致性和 disagreements 如何记录？
8. 经独立验证后，什么样的 selective risk/coverage 能达到 FORMA 项目的实际 VI 效率和误判要求？

## 9. 下一步最小可执行计划

**推荐的第一项交付物不是训练好的 CNN，而是可重复的数据集：**

1. 从现有真实失败案例与专家核对的 QSO 中挑选首批约 100–200 条，尤其包括 C IV、C III] 平缓宽线。
2. 冻结 full-spectrum schema 与 window-label schema；人工记录真实线位、难度、测得/专家宽度以及 CWT/SH/FA 各节点状态。
3. 实现单一、版本化的 Window Extractor；并行提供固定窗口、用户三档和宽线扩展窗口方案。
4. 训练最简单的统计 baseline 与小型 1D CNN，进行 grouped split 与宽线 stress test。
5. 在真实 FA 接口做离线回放，不改下游状态语义；确认性能和误判风险后再决定迁移。

**研究目标：** 在不削弱 FORMA 的 Evidence Synthesis 与 Investigation Orchestration 的前提下，让低层谱线真实性判断对 C IV/C III] 等宽线更可靠，并把推理成本从重复 LLM Vote 转向可量化、低延迟的数值 Perception。
