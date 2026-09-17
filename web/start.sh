#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
PORT="${JUICEPANS_PORT:-8765}"
python3 server.py &
PID=$!
sleep 1
if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "http://127.0.0.1:${PORT}/" >/dev/null 2>&1 || true
elif command -v open >/dev/null 2>&1; then
  open "http://127.0.0.1:${PORT}/" || true
fi
echo "果汁搜盘已启动 http://127.0.0.1:${PORT}/  (PID $PID)"
echo "按 Ctrl+C 停止。"
wait "$PID"
