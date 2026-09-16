#!/bin/bash
# PanSou 自部署一键部署（供 search.py 的 --engine local 与 check_links.py 的验链接口使用）
# 用法: bash deploy.sh [--port 8888] [--web] [--auth user:pass] [--channels ch1,ch2] [--plugins p1,p2]
set -e
PORT=8888
WEB_MODE=false
AUTH_ENABLED=false
AUTH_USERS=""
CHANNELS=""
PLUGINS=""
NAME="netdisk-search"
while [[ $# -gt 0 ]]; do
  case $1 in
    --port) PORT="$2"; shift 2;;
    --web) WEB_MODE=true; shift;;
    --auth) AUTH_ENABLED=true; AUTH_USERS="$2"; shift 2;;
    --channels) CHANNELS="$2"; shift 2;;
    --plugins) PLUGINS="$2"; shift 2;;
    -h|--help) echo "用法: bash deploy.sh [--port 8888] [--web] [--auth user:pass]"; exit 0;;
    *) echo "未知参数: $1"; exit 1;;
  esac
done
if ! command -v docker &> /dev/null; then echo "未安装 Docker，请先安装: https://docs.docker.com/get-docker/"; exit 1; fi
if ! docker info &> /dev/null; then echo "Docker 未启动，请先启动 Docker"; exit 1; fi
if docker ps -a --format '{{.Names}}' | grep -q "^${NAME}$"; then
  docker stop "$NAME" 2>/dev/null || true; docker rm "$NAME" 2>/dev/null || true
fi
if [ "$WEB_MODE" = true ]; then
  IMAGE="ghcr.io/fish2018/pansou-web:latest"; ARGS="-d --name ${NAME}-web -p ${PORT}:80"
else
  IMAGE="ghcr.io/fish2018/pansou:latest"; ARGS="-d --name ${NAME} -p ${PORT}:8888"
fi
[ -n "$CHANNELS" ] && ARGS="$ARGS -e CHANNELS=${CHANNELS}"
[ -n "$PLUGINS" ] && ARGS="$ARGS -e ENABLED_PLUGINS=${PLUGINS}"
[ "$AUTH_ENABLED" = true ] && ARGS="$ARGS -e AUTH_ENABLED=true -e AUTH_USERS=${AUTH_USERS}"
docker pull "$IMAGE"
eval docker run $ARGS "$IMAGE"
echo "等待启动..."; for i in $(seq 1 30); do
  if curl -sf "http://localhost:${PORT}/api/health" >/dev/null 2>&1; then echo "✅ 启动成功"; break; fi
  [ $i -eq 30 ] && { echo "启动超时"; exit 1; }; sleep 2
done
echo "API: http://localhost:${PORT}   后续搜索: export PANSOU_URL=http://localhost:${PORT}"
