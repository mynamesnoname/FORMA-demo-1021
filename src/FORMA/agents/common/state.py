import json
import numpy as np
from dataclasses import field
from typing import Any, Dict, Optional, List, Union
from matplotlib.figure import Figure
import re
from langgraph.graph import MessagesState

# @dataclass
class SpectroState(MessagesState):
    """
    LangGraph Agent 的光谱上下文状态。
    支持：
    - 自动 JSON 解析
    - 安全 set / append 操作
    - 自动创建未声明字段或列表
    """

    # ===========================
    # 🔹 原始输入
    # ===========================
    file_path: Optional[str] = None
    file_name: Optional[str] = None
    output_dir: Optional[str] = None
    crop_path: Optional[str] = None
    spec_extract_path: Optional[str] = None
    continuum_path: Optional[str] = None

    # ===========================
    # 🔹 图像识别与像素映射信息
    # ===========================
    axis_info: Optional[dict] = None
    OCR_detected_ticks: Optional[List[Dict[str, Union[float, int, List[int]]]]] = None
    tick_pixel_raw: Optional[List[Dict[str, Union[int, float, None]]]] = None
    chart_border: Optional[dict] = None
    tick_pixel_remap: Optional[List[Dict[str, Union[int, float, None]]]] = None
    pixel_to_value: Optional[dict] = None

    # ===========================
    # 🔹 光谱提取与特征数据
    # ===========================
    curve_points: Optional[List[List[int]]] = None
    curve_gray_values: Optional[Union[List[float], np.ndarray]] = None
    spectrum: Optional[Dict[str, Union[List[float], float]]] = None
    continuum: Optional[Dict[str, Any]] = None
    residual_spectrum: Optional[Dict[str, Union[List[float], float]]] = None
    peaks: Optional[List[Dict[str, float]]] = None
    troughs: Optional[List[Dict[str, float]]] = None
    redshift_hypotheses: Optional[List[Dict[str, Any]]] = None  # Redrock fit hypotheses
    absorption_records: Optional[List[Dict[str, Any]]] = None
    emission_records: Optional[List[Dict[str, Any]]] = None
    overlap_regions: Optional[Dict[str, List[float]]] = None
    redshift_scoring: Optional[Dict[str, Any]] = None              # VI output: low_z/high_z hypothesis lists
    hypothesis_results: Optional[List[Dict[str, Any]]] = None       # per-hypothesis harness output (report + feature_catalog)
    labeled_hypotheses: Optional[List[Dict[str, Any]]] = None       # WP-039: hypotheses with neutral labels, assigned at the Redrock boundary
    hypothesis_label_map: Optional[Dict[str, Any]] = None          # neutral label -> fit/znum map (WP-020/WP-039)
    evidence_graph: Optional[Any] = None                          # optional per-spectrum EvidenceGraph (WP-007)
    evidence_graph_projection_problems: Optional[List[str]] = None  # WP-035: skipped/ambiguous graph links, kept for audit
    telemetry: Optional[Any] = None                               # run/stage telemetry (WP-013)
    effective_parameters: Optional[Dict[str, Any]] = None          # resolved method/rule values at run creation
    frozen_parameters: Optional[Dict[str, Any]] = None             # per-run digest and declaration sources
    spectrum_npz_path: Optional[str] = None                      # path to saved spectrum .npz for harness use
    # ===========================
    # 🔹 可视化对象
    # ===========================
    spectrum_fig: Optional[Figure] = None
    features_fig: Optional[Figure] = None

    # ===========================
    # 🔹 LLM 解释与分析历史
    # ===========================
    # visual_interpretation: Optional[List] = field(default=None)
    qualitative_analysis: Optional[Dict[str, Any]] = field(default_factory=dict)
    preliminary_classification: Optional[str] = None
    preliminary_classification_with_absention: Optional[str] = None
    preliminary_classification_monkey: Optional[str] = None
    possible_object: Optional[List] = field(default=None)
    verdict: Optional[str] = None                         # historical audit verdict string
    final_report: Optional[str] = None                    # historical final-report text
    hypothesis_analysis: Optional[Dict[str, Any]] = None
    feature_audit_verdict: Optional[Dict[str, Any]] = None    # FeatureAuditor output
    harness_dir: Optional[str] = None                          # per-spectrum harness output directory
    auditor_verdict: Optional[str] = None                      # historical Stage-B verdict string
    auditor_verdict_json: Optional[Dict[str, Any]] = None      # historical Stage-B verdict record
    harness_rule_trace: Optional[Dict[str, Any]] = None       # Ontology rules on selected harness CSV
    auditor_rule_trace: Optional[Dict[str, Any]] = None       # Ontology rules after result audit
    in_brief: Optional[Dict[str, Any]] = None
    _no_features: Optional[bool] = None                      # set by orchestrator when VI finds zero features
    margin: Optional[Dict[str, int]] = None               # crop margins
    _failure_recorded: Optional[bool] = None              # failure bookkeeping
