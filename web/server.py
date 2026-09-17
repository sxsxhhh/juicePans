#!/usr/bin/env python3
"""果汁搜盘 — stdlib-only local web UI for juicePans search_core."""

from __future__ import annotations

import json
import os
import re
import sys
import threading
import traceback
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
HOST = os.environ.get("JUICEPANS_HOST", "127.0.0.1")
PORT = int(os.environ.get("JUICEPANS_PORT", "8765"))

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import search_core  # noqa: E402

try:
    import check_links  # noqa: E402
except Exception:
    check_links = None  # type: ignore

BLOCKED_PATTERNS = [
    r"破解",
    r"\bcrack\b",
    r"\bwarez\b",
    r"序列号",
    r"注册机",
    r"keygen",
    r"色情",
    r"成人视频",
    r"黄片",
    r"av女优",
    r"porn",
    r"xxx",
    r"赌博",
    r"博彩",
    r"赌场",
    r"六合彩",
    r"威尼斯人",
]

ENGINE_ALIAS = {
    "盘搜": "pansou",
    "小云": "yunso",
    "海搜": "haisou",
    "盘小子": "panxiaozi",
    "tg库": "ghspider",
    "tg": "ghspider",
    "pansou": "pansou",
    "yunso": "yunso",
    "haisou": "haisou",
    "panxiaozi": "panxiaozi",
    "ghspider": "ghspider",
}

DEFAULT_ENGINES = "pansou,yunso,haisou"

MIME = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".ico": "image/x-icon",
    ".woff2": "font/woff2",
}


def is_blocked_query(q: str) -> bool:
    text = (q or "").strip().lower()
    if not text:
        return False
    for pat in BLOCKED_PATTERNS:
        if re.search(pat, text, re.I):
            return True
    return False


def normalize_engines(raw: str | None) -> str:
    if not raw or not raw.strip():
        return DEFAULT_ENGINES
    out = []
    seen = set()
    for part in raw.split(","):
        key = part.strip().lower()
        if not key:
            continue
        eng = ENGINE_ALIAS.get(key) or ENGINE_ALIAS.get(part.strip()) or key
        if eng not in seen:
            seen.add(eng)
            out.append(eng)
    return ",".join(out) if out else DEFAULT_ENGINES


def normalize_clouds(raw: str | None) -> str | None:
    if raw is None:
        return None
    s = raw.strip()
    if not s or s in ("综合", "all", "*"):
        return None
    return s


def label_results(payload: dict) -> dict:
    items = payload.get("results") or []
    for rec in items:
        rec["label"] = "公开检索（未核验）"
        rec["link_state"] = rec.get("link_state") or "uncertain"
        if not rec.get("cloud_name"):
            c = rec.get("cloud") or "others"
            rec["cloud_name"] = search_core.CLOUD_NAMES.get(c, c)
    payload["disclaimer"] = "公开检索（未核验）— 结果来自公开聚合源，链接有效性未核验，请自行判断。"
    return payload


def _check_one_url(url: str, password: str = "") -> dict:
    """Return {state, summary} using check_links when available."""
    if not check_links or not url:
        return {"state": "uncertain", "summary": "验链模块不可用"}
    dtype = check_links.detect_disk_type(url)
    if dtype in ("magnet", "ed2k"):
        return {"state": "unsupported", "summary": "磁力/电驴不做存活检测"}
    quark = None
    try:
        quark = check_links.detect_quark()
    except Exception:
        quark = None
    try:
        if dtype == "quark" and quark:
            state, summary = check_links.verify_quark(quark[0], quark[1], url, password or "")
            return {"state": state, "summary": summary}
        state, summary = check_links.verify_anon(url, dtype, password or "")
        return {"state": state or "uncertain", "summary": summary or ""}
    except Exception as e:
        return {"state": "uncertain", "summary": "验链异常：%s" % e}


def apply_link_validation(payload: dict, max_check: int = 40) -> dict:
    """When validate=on: check up to max_check links, drop confirmed bad, annotate others."""
    items = list(payload.get("results") or [])
    if not items:
        payload["validate"] = True
        payload["disclaimer"] = "已开启链接存活检验，但本次无结果可检。"
        return payload

    to_check = items[:max_check]
    rest = items[max_check:]
    checked = []

    def work(rec):
        url = rec.get("url") or ""
        pwd = rec.get("password") or rec.get("pwd") or ""
        verdict = _check_one_url(url, pwd)
        out = dict(rec)
        out["link_state"] = verdict.get("state") or "uncertain"
        out["link_summary"] = verdict.get("summary") or ""
        icon = {
            "ok": "有效",
            "suspect": "疑似失效",
            "bad": "确认失效",
            "locked": "需提取码",
            "unsupported": "未检",
            "uncertain": "未核验",
        }.get(out["link_state"], "未核验")
        out["label"] = "存活检验 · " + icon
        return out

    from concurrent.futures import ThreadPoolExecutor, as_completed

    with ThreadPoolExecutor(max_workers=min(8, max(1, len(to_check)))) as pool:
        futs = {pool.submit(work, rec): i for i, rec in enumerate(to_check)}
        slots = [None] * len(to_check)
        for fut in as_completed(futs):
            i = futs[fut]
            try:
                slots[i] = fut.result()
            except Exception as e:
                r = dict(to_check[i])
                r["link_state"] = "uncertain"
                r["link_summary"] = str(e)
                r["label"] = "存活检验 · 未核验"
                slots[i] = r

    kept = []
    dropped = 0
    for rec in slots:
        if not rec:
            continue
        if rec.get("link_state") == "bad":
            dropped += 1
            continue
        kept.append(rec)
    for rec in rest:
        r = dict(rec)
        r["link_state"] = "uncertain"
        r["label"] = "公开检索（未核验·超出本次检验上限）"
        kept.append(r)

    payload["results"] = kept
    payload["total"] = len(kept)
    payload["validate"] = True
    payload["validate_dropped"] = dropped
    payload["disclaimer"] = (
        "已开启链接存活检验：确认失效已隐藏；其余为有效/疑似/未核验。夸克优先 CLI，其它走匿名检测。"
    )
    return payload


class Handler(BaseHTTPRequestHandler):
    server_version = "JuicePans/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, code: int, obj: dict):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _file(self, path: Path):
        if not path.is_file():
            self.send_error(404, "Not Found")
            return
        data = path.read_bytes()
        ctype = MIME.get(path.suffix.lower(), "application/octet-stream")
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self._cors()
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path or "/"
        qs = urllib.parse.parse_qs(parsed.query)

        if path == "/api/search":
            self.handle_search(qs)
            return
        if path == "/api/health":
            self._json(200, {"ok": True, "service": "果汁搜盘", "port": PORT})
            return
        if path in ("/", "/index.html"):
            self._file(STATIC / "index.html")
            return
        if path.startswith("/static/"):
            rel = path[len("/static/") :]
            self._file((STATIC / rel).resolve())
            return
        # allow /app.css /app.js etc under static
        candidate = (STATIC / path.lstrip("/")).resolve()
        try:
            candidate.relative_to(STATIC.resolve())
        except ValueError:
            self.send_error(403)
            return
        if candidate.is_file():
            self._file(candidate)
            return
        self.send_error(404, "Not Found")

    def handle_search(self, qs: dict):
        q = (qs.get("q") or qs.get("kw") or [""])[0].strip()
        clouds = (qs.get("clouds") or qs.get("cloud_types") or [""])[0]
        engines = (qs.get("engines") or qs.get("engine") or [""])[0]
        validate_raw = (qs.get("validate") or qs.get("check") or ["0"])[0].strip().lower()
        do_validate = validate_raw in ("1", "true", "yes", "on")

        if not q:
            self._json(400, {"ok": False, "error": "请输入搜索关键词。"})
            return
        if is_blocked_query(q):
            self._json(
                400,
                {
                    "ok": False,
                    "error": "查询包含敏感或违规内容（破解/色情/赌博等），已拒绝检索。请更换合法关键词。",
                },
            )
            return

        cloud_types = normalize_clouds(clouds)
        engine = normalize_engines(engines)
        try:
            limit = int((qs.get("limit") or ["30"])[0] or 30)
            if limit < 1:
                limit = 30
            if limit > 80:
                limit = 80
            payload = search_core.run_search(
                q,
                cloud_types=cloud_types,
                engine=engine,
                limit=limit,
                fresh=True,
                as_json=True,
            )
            payload = label_results(payload)
            payload["ok"] = True
            payload["engines"] = engine
            payload["clouds"] = cloud_types or "综合全部"
            payload["validate"] = False
            if do_validate:
                payload = apply_link_validation(payload)
            self._json(200, payload)
        except Exception as e:
            traceback.print_exc()
            self._json(500, {"ok": False, "error": "搜索失败：%s" % e})


def main():
    STATIC.mkdir(parents=True, exist_ok=True)
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print("果汁搜盘已启动 → http://%s:%s/" % (HOST, PORT), flush=True)
    print("按 Ctrl+C 停止。仅本机访问。", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。", flush=True)
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
