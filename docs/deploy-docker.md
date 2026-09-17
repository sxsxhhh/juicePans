# Docker 部署（果汁搜盘站点）

在任意已安装 Docker 的主机上（x86_64 / ARM，含玩客云一类板子）运行 `web/` 站点。

## 快速启动

```bash
cd web
docker compose up -d --build
# 若系统只有旧版 docker-compose：
# docker-compose up -d --build
```

访问：`http://<主机IP>:8765/`

## 无 compose 插件时（如部分 Docker 20.10）

```bash
cd web
docker build -t juicepans:local .
docker rm -f juicepans 2>/dev/null || true
docker run -d --name juicepans --restart unless-stopped \
  -p 8765:8765 \
  -e JUICEPANS_HOST=0.0.0.0 \
  -e JUICEPANS_PORT=8765 \
  juicepans:local
```

## 常用命令

```bash
docker ps --filter name=juicepans
docker logs -f juicepans
docker restart juicepans
docker stop juicepans
```

更新代码后重新构建：

```bash
cd web
docker compose up -d --build
# 或无 compose 时：重新 docker build + docker run（见上）
```

## 注意事项

- 镜像基于 `python:3.12-slim`，首次构建会拉基础镜像
- 容器内默认监听 `0.0.0.0:8765`，并映射到宿主机 `8765`
- 防火墙需放行 `8765/tcp`（若启用了 ufw/firewalld）
- ARM（如 armv7）可在设备上原生 `docker build`；勿假设必须用 `docker compose` 子命令
