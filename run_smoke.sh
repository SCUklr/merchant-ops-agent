#!/usr/bin/env bash
# 一键：确保 venv → 安装依赖 → 运行 LangChain 冒烟测试
# 用法：
#   ./run_smoke.sh              # 真实调用模型（需 .env 或已 export Key）
#   ONLY_IMPORTS=1 ./run_smoke.sh   # 只验证 import
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

resolve_python312() {
  if [[ -n "${PYTHON312:-}" && -x "${PYTHON312}" ]]; then
    echo "${PYTHON312}"
    return
  fi
  if [[ -x /opt/homebrew/bin/python3.12 ]]; then
    echo /opt/homebrew/bin/python3.12
    return
  fi
  if command -v python3.12 >/dev/null 2>&1; then
    command -v python3.12
    return
  fi
  echo "未找到 python3.12。请安装 Python 3.12，或设置 PYTHON312=/path/to/python3.12" >&2
  exit 1
}

PY="$(resolve_python312)"

if [[ ! -d .venv ]]; then
  echo "创建虚拟环境: $PY -m venv .venv"
  "$PY" -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

if [[ ! -f requirements.txt ]]; then
  echo "缺少 requirements.txt" >&2
  exit 1
fi

echo "安装/同步依赖 (pip install -r requirements.txt) ..."
pip install -q -r requirements.txt

echo "运行 scripts/smoke_test_langchain.py ..."
exec python scripts/smoke_test_langchain.py "$@"
