FROM python:3.12-slim
WORKDIR /app
# Copy site sources (exclude docker metadata via .dockerignore)
COPY server.py search_core.py check_links.py start.sh ./
COPY static/ ./static/
COPY docs/ ./docs/
COPY README_zh.md 使用说明.txt ./
ENV JUICEPANS_HOST=0.0.0.0
ENV JUICEPANS_PORT=8765
ENV PYTHONUNBUFFERED=1
EXPOSE 8765
CMD ["python3", "server.py"]
