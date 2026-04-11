#!/usr/bin/env python3
"""最小 LangChain 冒烟：验证依赖可 import，或在有 Key 时各调一次对话模型。

支持：
- DeepSeek：OpenAI 兼容接口，使用 langchain_openai.ChatOpenAI + base_url
- 通义 Qwen：DashScope，使用 langchain_community ChatTongyi

用法（在项目根目录）：
  source .venv/bin/activate
  cp .env.example .env   # 填入任一平台的 API Key
  python scripts/smoke_test_langchain.py

仅测 import、不调 API：
  ONLY_IMPORTS=1 python scripts/smoke_test_langchain.py
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

load_dotenv()


def _only_imports() -> int:
    import langchain
    from langchain_community.chat_models import ChatTongyi
    from langchain_openai import ChatOpenAI

    print("imports_ok", f"langchain={langchain.__version__}")
    _ = ChatOpenAI  # noqa: F841
    _ = ChatTongyi  # noqa: F841
    return 0


def _build_llm():
    backend = (os.environ.get("LLM_BACKEND") or "").strip().lower()
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    dashscope_key = os.environ.get("DASHSCOPE_API_KEY", "").strip()

    if not backend:
        if deepseek_key:
            backend = "deepseek"
        elif dashscope_key:
            backend = "qwen"

    if backend == "deepseek":
        if not deepseek_key:
            raise RuntimeError("已选择 deepseek 但未设置 DEEPSEEK_API_KEY")
        from langchain_openai import ChatOpenAI

        model = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat").strip() or "deepseek-chat"
        return ChatOpenAI(
            model=model,
            api_key=deepseek_key,
            base_url="https://api.deepseek.com",
        )

    if backend == "qwen":
        if not dashscope_key:
            raise RuntimeError("已选择 qwen 但未设置 DASHSCOPE_API_KEY")
        from langchain_community.chat_models import ChatTongyi

        model = os.environ.get("QWEN_MODEL", "qwen-turbo").strip() or "qwen-turbo"
        return ChatTongyi(model=model, api_key=dashscope_key)

    raise RuntimeError(
        "请设置 LLM_BACKEND=deepseek 或 qwen，并配置对应 Key；"
        "或只设置 DEEPSEEK_API_KEY / DASHSCOPE_API_KEY 其一以自动选择。"
    )


def main() -> int:
    if os.environ.get("ONLY_IMPORTS", "").lower() in ("1", "true", "yes"):
        return _only_imports()

    from langchain_core.messages import HumanMessage

    try:
        llm = _build_llm()
    except RuntimeError as e:
        print(e, file=sys.stderr)
        print(
            "提示：可先用 ONLY_IMPORTS=1 python scripts/smoke_test_langchain.py 验证依赖。",
            file=sys.stderr,
        )
        return 2

    msg = HumanMessage(content='用一句话回答：1+1等于几？只输出数字。')
    out = llm.invoke([msg])
    text = out.content if hasattr(out, "content") else str(out)
    print("llm_reply:", text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
