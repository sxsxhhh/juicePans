(() => {
  const CLOUDS = [
    { id: "", label: "综合" },
    { id: "quark", label: "夸克" },
    { id: "baidu", label: "百度" },
    { id: "aliyun", label: "阿里" },
    { id: "123", label: "123" },
    { id: "xunlei", label: "迅雷" },
    { id: "uc", label: "UC" },
    { id: "115", label: "115" },
    { id: "tianyi", label: "天翼" },
    { id: "mobile", label: "移动" },
    { id: "lanzou", label: "蓝奏" },
    { id: "magnet", label: "磁力" },
  ];

  const CLOUD_ORDER = CLOUDS.map((c) => c.id).filter(Boolean).concat(["pikpak", "guangya", "ed2k", "others"]);
  const CLOUD_NAMES = {
    quark: "夸克网盘", baidu: "百度网盘", aliyun: "阿里云盘", "123": "123网盘",
    xunlei: "迅雷网盘", uc: "UC网盘", "115": "115网盘", tianyi: "天翼云盘",
    mobile: "移动云盘", lanzou: "蓝奏云", magnet: "磁力链接", ed2k: "电驴链接",
    pikpak: "PikPak", guangya: "光鸭云盘", others: "其他",
  };
  const CLOUD_ICONS = {
    quark: "/icons/quark.png",
    baidu: "/icons/baidu.png",
  };

  let activeCloud = "";
  const tabsEl = document.getElementById("cloudTabs");
  const form = document.getElementById("searchForm");
  const qEl = document.getElementById("q");
  const btn = document.getElementById("btnSearch");
  const statusEl = document.getElementById("status");
  const resultsEl = document.getElementById("results");

  function renderTabs() {
    tabsEl.innerHTML = "";
    CLOUDS.forEach((c) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "tab" + (c.id === activeCloud ? " active" : "");
      b.setAttribute("role", "tab");
      b.setAttribute("aria-selected", c.id === activeCloud ? "true" : "false");
      b.textContent = c.label;
      b.addEventListener("click", () => {
        activeCloud = c.id;
        renderTabs();
      });
      tabsEl.appendChild(b);
    });
  }

  function selectedEngines() {
    return Array.from(document.querySelectorAll('input[name="engine"]:checked'))
      .map((el) => el.value)
      .join(",");
  }

  function setStatus(text, kind) {
    if (!text) {
      statusEl.hidden = true;
      statusEl.textContent = "";
      statusEl.className = "status";
      return;
    }
    statusEl.hidden = false;
    statusEl.textContent = text;
    statusEl.className = "status" + (kind ? " " + kind : "");
  }

  function esc(s) {
    return String(s ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function groupByCloud(items) {
    const map = new Map();
    for (const it of items) {
      const key = it.cloud || "others";
      if (!map.has(key)) map.set(key, []);
      map.get(key).push(it);
    }
    const ordered = [];
    for (const k of CLOUD_ORDER) {
      if (map.has(k)) {
        ordered.push([k, map.get(k)]);
        map.delete(k);
      }
    }
    for (const [k, v] of map) ordered.push([k, v]);
    return ordered;
  }

  async function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
  }

  function renderResults(data) {
    resultsEl.innerHTML = "";
    const items = data.results || [];
    if (!items.length) {
      resultsEl.innerHTML = `<div class="empty">未找到相关资源。可换中文片名、英文原名，或勾选更多引擎重试。</div>`;
      return;
    }
    const groups = groupByCloud(items);
    for (const [cloud, rows] of groups) {
      const name = CLOUD_NAMES[cloud] || rows[0]?.cloud_name || cloud;
      const icon = CLOUD_ICONS[cloud];
      const sec = document.createElement("section");
      sec.className = "group";
      const logoHtml = icon
        ? `<img class="cloud-logo" src="${esc(icon)}" alt="" width="28" height="28" />`
        : "";
      sec.innerHTML = `<div class="group-head"><div class="group-head-left">${logoHtml}<h2>${esc(name)}</h2></div><span class="count">${rows.length}</span></div>`;
      for (const r of rows) {
        const item = document.createElement("article");
        item.className = "item";
        const url = r.url || "#";
        const title = r.title || r.note || r.name || url;
        const src = r.source || "";
        const dt = r.datetime || r.date || "";
        const pwd = r.password || r.pwd || "";
        const st = r.link_state || "";
        let linkLabel = r.label || "公开检索（未核验）";
        let linkCls = "warn";
        if (st === "ok") { linkCls = "ok"; linkLabel = r.label || "存活检验 · 有效"; }
        else if (st === "suspect") { linkCls = "suspect"; linkLabel = r.label || "存活检验 · 疑似失效"; }
        else if (st === "bad") { linkCls = "bad"; linkLabel = r.label || "存活检验 · 确认失效"; }
        else if (st === "locked") { linkCls = "suspect"; linkLabel = r.label || "存活检验 · 需提取码"; }
        item.innerHTML = `
          <a class="title" href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(title)}</a>
          <div class="meta">
            <span class="chip ${linkCls}">${esc(linkLabel)}</span>
            ${src ? `<span class="chip">来源 ${esc(src)}</span>` : ""}
            ${dt ? `<span class="chip">日期 ${esc(dt)}</span>` : ""}
            ${pwd ? `<span class="chip">提取码 <span class="pwd">${esc(pwd)}</span></span>` : ""}
          </div>
          <div class="item-actions">
            <a class="action-btn primary" href="${esc(url)}" target="_blank" rel="noopener noreferrer">打开链接</a>
            <button type="button" class="action-btn copy-btn" data-url="${esc(url)}">复制链接</button>
          </div>`;
        const copyBtn = item.querySelector(".copy-btn");
        copyBtn.addEventListener("click", async () => {
          try {
            await copyText(url);
            const prev = copyBtn.textContent;
            copyBtn.textContent = "已复制";
            copyBtn.classList.add("copied");
            setTimeout(() => {
              copyBtn.textContent = prev;
              copyBtn.classList.remove("copied");
            }, 1500);
          } catch (e) {
            copyBtn.textContent = "复制失败";
            setTimeout(() => { copyBtn.textContent = "复制链接"; }, 1500);
          }
        });
        sec.appendChild(item);
      }
      resultsEl.appendChild(sec);
    }
  }

  const btnAbort = document.getElementById("btnAbort");
  const optValidate = document.getElementById("optValidate");
  const VALIDATE_KEY = "juicepans_validate_links";
  let searchAbort = null;
  let abortTimer = null;
  let searchGen = 0;

  try {
    if (optValidate && localStorage.getItem(VALIDATE_KEY) === "1") {
      optValidate.checked = true;
    }
  } catch (_) {}
  if (optValidate) {
    optValidate.addEventListener("change", () => {
      try {
        localStorage.setItem(VALIDATE_KEY, optValidate.checked ? "1" : "0");
      } catch (_) {}
    });
  }

  function clearAbortUi() {
    if (abortTimer) {
      clearTimeout(abortTimer);
      abortTimer = null;
    }
    if (btnAbort) btnAbort.hidden = true;
  }

  function stopSearch(reason) {
    if (searchAbort) {
      try { searchAbort.abort(); } catch (_) {}
    }
    clearAbortUi();
    btn.disabled = false;
    setStatus(reason || "已终止搜索", "error");
  }

  if (btnAbort) {
    btnAbort.addEventListener("click", () => stopSearch("已手动终止搜索"));
  }

  async function doSearch(ev) {
    if (ev) ev.preventDefault();
    const q = qEl.value.trim();
    if (!q) return;
    const engines = selectedEngines();
    if (!engines) {
      setStatus("请至少选择一个搜索引擎。", "error");
      return;
    }
    // cancel previous
    if (searchAbort) {
      try { searchAbort.abort(); } catch (_) {}
    }
    clearAbortUi();
    const myGen = ++searchGen;
    searchAbort = new AbortController();
    const validate = !!(optValidate && optValidate.checked);

    btn.disabled = true;
    setStatus(validate ? "正在聚合检索并检验链接存活…" : "正在聚合检索，请稍候…", "loading");
    resultsEl.innerHTML = "";

    // 超过 6 秒仍无结果返回 → 显示终止按钮
    abortTimer = setTimeout(() => {
      if (myGen !== searchGen) return;
      if (btnAbort) {
        btnAbort.hidden = false;
        setStatus((validate ? "检索/验链较慢" : "检索较慢") + "，可点「终止」中断", "loading");
      }
    }, 6000);

    const params = new URLSearchParams({ q, engines });
    if (activeCloud) params.set("clouds", activeCloud);
    if (validate) params.set("validate", "1");
    try {
      const res = await fetch("/api/search?" + params.toString(), { signal: searchAbort.signal });
      if (myGen !== searchGen) return;
      const data = await res.json();
      if (!res.ok || data.ok === false) {
        setStatus(data.error || "搜索失败", "error");
        return;
      }
      const bits = [`共 ${data.total || 0} 条`, `引擎 ${data.engines || engines}`];
      if (data.validate) bits.push("已验链");
      if (data.validate_dropped) bits.push(`隐藏失效 ${data.validate_dropped}`);
      if (data.variant_used) bits.push(`变体「${data.variant_used}」`);
      if (data.errors && data.errors.length) bits.push(`部分源异常 ${data.errors.length}`);
      setStatus(bits.join(" · "));
      renderResults(data);
    } catch (e) {
      if (myGen !== searchGen) return;
      if (e && e.name === "AbortError") {
        setStatus("已终止搜索", "error");
        return;
      }
      setStatus("网络或服务异常：" + (e && e.message ? e.message : e), "error");
    } finally {
      if (myGen === searchGen) {
        clearAbortUi();
        btn.disabled = false;
        searchAbort = null;
      }
    }
  }

  form.addEventListener("submit", doSearch);
  renderTabs();
  qEl.focus();
})();
