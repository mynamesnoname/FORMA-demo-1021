import os
from typing import Optional, Dict, Any
from pydantic import BaseModel

from FORMA.core.config._utils import getenv_float


# ------------------------
# LLM / VLM 配置
# ------------------------

class ModelConfig(BaseModel):
    llm: Dict[str, Any]
    vlm: Dict[str, Any]

    @classmethod
    def from_env(cls) -> "ModelConfig":
        def parse_max_tokens(v: Optional[str]) -> Optional[int]:
            if v and v.strip():
                try:
                    return int(v.strip())
                except ValueError:
                    print(f"⚠️ MAX_TOKENS invalid format / 格式错误: {v}, using None / 使用 None")
            return None

        llm={
            "api_key": os.getenv("LLM_API_KEY"),
            "base_url": os.getenv("LLM_BASE_URL"),
            "model": os.getenv("LLM_MODEL"),
            # Client default.  Every live stage builds its own client with
            # `temperature_for(stage)` (config/model_calls.json), so this value
            # currently governs no live call: its only consumer is the preserved,
            # commented-out vision path in BaseAgent.call_llm_with_context, which has
            # no live caller.
            # 客户端默认值。每个活动阶段都用 `temperature_for(stage)`
            # （config/model_calls.json）自行构造客户端，因此该值目前管不到任何活调用：它唯一
            # 的消费者是 BaseAgent.call_llm_with_context 中保留但已注释的视觉路径，而该路径
            # 没有活调用者。
            "temperature": getenv_float("LLM_TEMPERATURE", 0.1),
            "max_tokens": parse_max_tokens(os.getenv("LLM_MAX_TOKENS")),
            "thinking": os.getenv("LLM_THINKING", "disabled"),
        }
        vlm={
            "api_key": os.getenv("VLM_API_KEY"),
            "base_url": os.getenv("VLM_BASE_URL"),
            "model": os.getenv("VLM_MODEL"),
            "temperature": getenv_float("VLM_TEMPERATURE", 0.1),
            "max_tokens": parse_max_tokens(os.getenv("VLM_MAX_TOKENS")),
            "thinking": os.getenv("VLM_THINKING", "disabled"),
        }

        # ── LLM 配置校验（必填）──────────────────────────────────
        if not all([llm['api_key'], llm['model'], llm["base_url"]]):
            raise ValueError("LLM 配置不完整（LLM_API_KEY / LLM_MODEL / LLM_BASE_URL 必填）")

        # ── VLM 配置（可选，PNG 通道已注释暂不需要）────────────────
        # 如果 VLM 未配置，vlm 字典保留空值，base_agent 会在首次调用时跳过

        return cls(llm=llm, vlm=vlm)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()