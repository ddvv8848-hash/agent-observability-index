#!/usr/bin/env python3
"""Static site generator for the Agent Observability Index (by Panshi)."""
import json, os, re, shutil, html, math
from datetime import date

BASE = "https://panshi.io/tools"  # brand-v2: merged under panshi.io/tools (was https://tools.panshi.io)
SITE = "Agent Observability Index"
TAG = "Every AI agent observability, evals, guardrails & cost tool — compared by a neutral third party."
OUT = "site"
BUILD_DATE = date.today().isoformat()
OG_IMAGE = BASE + "/og.png"
CF_BEACON = ("<script defer src='https://static.cloudflareinsights.com/beacon.min.js' "
             "data-cf-beacon='{\"token\": \"47f87bd8826546019d26f62a05a61859\"}'></script>")

# Linear-style DARK design system, injected into every page <head>. Colors match
# the brand site (src/styles/global.css) exactly so /tools feels like one product.
# Defined as a literal <style> block (not Tailwind) so arbitrary dark hex values
# survive Tailwind purge. NO green/emerald anywhere — indigo #5E6AD2 accent only.
DARK_CSS = """<style>
:root{--accent:#5E6AD2;--accent-hover:#6E79E0;--bg:#08090A;--surface1:#0F1011;--surface2:#16171A;--hairline:rgba(255,255,255,.08);--hairline-strong:rgba(255,255,255,.14);--t1:#F7F8F8;--t2:#9CA0A8;--t3:#62666D;}
html{background:#08090A;color-scheme:dark;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;scroll-behavior:smooth;}
body{font-feature-settings:'cv11','ss01';letter-spacing:-0.011em;}
h1,h2,h3{letter-spacing:-0.02em;}
::selection{background:rgba(94,106,210,.32);color:#fff;}
.ps-link{color:var(--accent);font-weight:500;transition:color .15s;}
.ps-link:hover{color:var(--accent-hover);}
/* dark recolor of long-form article body (blog posts) */
.prose-dark{color:var(--t2);}
.prose-dark p{color:var(--t2);}
.prose-dark h2,.prose-dark h3,.prose-dark strong{color:var(--t1);}
.prose-dark a{color:var(--accent);}
.prose-dark a:hover{color:var(--accent-hover);}
.prose-dark code{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:.85em;background:rgba(255,255,255,.06);border:1px solid var(--hairline);border-radius:4px;padding:.05em .35em;color:var(--t1);}
.prose-dark pre{background:#0a0b0c;border:1px solid var(--hairline);border-radius:10px;}
.prose-dark table th{color:var(--t1);border-color:var(--hairline-strong)!important;}
.prose-dark td,.prose-dark th{border-color:var(--hairline)!important;}
/* search input */
.ps-search{background:#0F1011;border:1px solid var(--hairline-strong);color:var(--t1);}
.ps-search::placeholder{color:var(--t3);}
.ps-search:focus{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent);}
/* filter + sort chips (states toggled by inline JS) */
.fbtn{background:transparent;border:1px solid var(--hairline-strong);color:var(--t2);transition:all .15s;}
.fbtn:hover{border-color:rgba(255,255,255,.28);color:var(--t1);}
.fbtn-on{background:var(--accent);border:1px solid var(--accent);color:#fff;}
.fbtn-on:hover{background:var(--accent-hover);border-color:var(--accent-hover);color:#fff;}
.sbtn{background:transparent;border:1px solid var(--hairline-strong);color:var(--t2);transition:all .15s;}
.sbtn:hover{border-color:rgba(255,255,255,.28);color:var(--t1);}
.sbtn-on{border-color:var(--accent);color:#aab2ee;}
/* account dropdown (#ps-acct) — replicated from Brand.astro so the header account
   menu behaves identically on directory/blog pages */
.nav-dd{position:relative;}
.nav-dd__btn{cursor:pointer;padding:0;margin:0;background:none;border:0;color:inherit;font:inherit;line-height:1;}
.nav-dd__chev{opacity:.65;transition:transform .18s ease;}
.nav-dd:hover .nav-dd__chev,.nav-dd[data-open="true"] .nav-dd__chev{transform:rotate(180deg);}
.nav-dd__panel{position:absolute;top:100%;left:0;margin-top:12px;width:280px;background:#16171A;border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:6px;box-shadow:0 16px 48px rgba(0,0,0,.55);opacity:0;visibility:hidden;transform:translateY(-6px);transition:opacity .16s ease,transform .16s ease,visibility .16s;z-index:50;}
.nav-dd__panel::before{content:'';position:absolute;top:-12px;left:0;right:0;height:12px;}
.nav-dd:hover .nav-dd__panel,.nav-dd:focus-within .nav-dd__panel,.nav-dd[data-open="true"] .nav-dd__panel{opacity:1;visibility:visible;transform:translateY(0);}
.ps-acct__item{transition:background .12s ease,color .12s ease;}
.ps-acct__item:hover{background:rgba(255,255,255,.05);color:#F7F8F8;}
</style>"""

CATS = {
 "observability": ("Observability & Tracing", "Trace, log and monitor LLM and agent calls in production."),
 "evals": ("Evals & Testing", "Score outputs, run regression suites and red-team agent behavior."),
 "guardrails": ("Guardrails & Safety", "Block prompt injection, PII leakage and unsafe outputs at runtime."),
 "prompt-mgmt": ("Prompt Management", "Version, test and deploy prompts with team workflows."),
 "cost": ("Cost & FinOps", "Track token spend, unit economics and budgets across providers."),
 "debugging": ("Agent Debugging & Replay", "Step-level replay and simulation for long-running agents."),
}

COMPARE_PAIRS = [
 ("Langfuse","LangSmith"),("Langfuse","Helicone"),("Langfuse","Arize Phoenix"),
 ("Braintrust","LangSmith"),("Opik (Comet)","Langfuse"),("Promptfoo","Confident AI (DeepEval)"),
 ("Ragas","Promptfoo"),("AgentOps","Langfuse"),("Datadog LLM Observability","LangSmith"),
 ("Helicone","Portkey"),("Guardrails AI","NVIDIA NeMo Guardrails"),("Lakera Guard","LLM Guard (Protect AI)"),("garak","PyRIT"),("TensorZero","Langfuse"),
 ("Arize Phoenix","SigNoz"),("Traceloop (OpenLLMetry)","OpenLIT"),("Helicone","LiteLLM"),
 ("Datadog LLM Observability","Langfuse"),("W&B Weave","Langfuse"),("Opik (Comet)","Arize Phoenix"),
 ("Galileo","Braintrust"),("Confident AI (DeepEval)","Ragas"),("Pydantic Logfire","Langfuse"),
 ("Portkey","LiteLLM"),("Braintrust","Langfuse"),("Maxim AI","Langfuse"),
    ("LangSmith","Helicone"),("Datadog LLM Observability","New Relic AI Monitoring"),
    ("Braintrust","Confident AI (DeepEval)"),("Galileo","Arize Phoenix"),
    ("Langfuse","SigNoz"),("Arize Phoenix","OpenLIT"),("Maxim AI","Braintrust"),
    ("Helicone","OpenLIT"),("Promptfoo","OpenAI Evals"),("Langfuse","MLflow (Tracing & GenAI)"),
]

try:
    from posts import POSTS
except Exception:
    POSTS = []

BEST_PAGES = [
 {"slug": "best-self-hostable-llm-observability-tools",
  "title": "Best self-hostable LLM observability tools (2026)",
  "h1": "Best self-hostable LLM observability tools",
  "lead": "LLM observability and tracing tools you can run inside your own infrastructure, ranked by our public GitHub maturity signal.",
  "crit": "self-hostable + in the observability, debugging or cost categories",
  "match": lambda t: t.get("self_hostable") and t.get("category") in ("observability", "debugging", "cost")},
 {"slug": "best-opentelemetry-native-llm-observability-tools",
  "title": "Best OpenTelemetry-native LLM observability tools (2026)",
  "h1": "Best OpenTelemetry-native LLM observability tools",
  "lead": "LLM tracing tools that speak OpenTelemetry (OTLP) natively, so there is no proprietary-SDK lock-in. Ranked by our GitHub maturity signal.",
  "crit": "OpenTelemetry-native (verified from docs/repo)",
  "match": lambda t: t.get("otel_native") is True},
 {"slug": "best-open-source-llm-evals-tools",
  "title": "Best open-source LLM evals & testing tools (2026)",
  "h1": "Best open-source LLM evals & testing tools",
  "lead": "Open-source frameworks for scoring LLM output, running regression suites and red-teaming, ranked by our GitHub maturity signal.",
  "crit": "open-source + in the evals category",
  "match": lambda t: t.get("open_source") and t.get("category") == "evals"},
 {"slug": "best-free-llm-observability-tools",
  "title": "Best free LLM observability tools (2026)",
  "h1": "Best free LLM observability tools",
  "lead": "LLM observability tools with a free or freemium tier, ranked by our GitHub maturity signal.",
  "crit": "free or freemium pricing + in the observability category",
  "match": lambda t: t.get("pricing_model") in ("free", "freemium") and t.get("category") == "observability"},
 {"slug": "best-llm-guardrails-tools",
  "title": "Best LLM guardrails & safety tools (2026)",
  "h1": "Best LLM guardrails & safety tools",
  "lead": "Tools that block prompt injection, PII leakage and unsafe output at runtime, ranked by our GitHub maturity signal.",
  "crit": "in the guardrails & safety category",
  "match": lambda t: t.get("category") == "guardrails"},
 {"slug": "best-llm-cost-tracking-tools",
  "title": "Best LLM cost tracking & FinOps tools (2026)",
  "h1": "Best LLM cost tracking & FinOps tools",
  "lead": "Tools to track token spend, unit economics and budgets across providers, ranked by our GitHub maturity signal.",
  "crit": "in the cost & FinOps category",
  "match": lambda t: t.get("category") == "cost"},
]

def slug(s):
    return re.sub(r"-+","-",re.sub(r"[^a-z0-9]+","-",s.lower())).strip("-")

def esc(s):
    return html.escape(s or "")

def fmt_stars(n):
    if n is None: return "—"
    if n >= 1000:
        v = f"{n/1000:.1f}k"
        return v.replace(".0k", "k")
    return str(n)

def recency_points(pushed):
    if not pushed: return 0
    try:
        y, m, d = map(int, pushed.split("-"))
        days = (date.today() - date(y, m, d)).days
    except Exception:
        return 0
    if days <= 30: return 35
    if days <= 90: return 25
    if days <= 180: return 14
    if days <= 365: return 6
    return 0

def recency_label(pushed):
    if not pushed: return "—"
    try:
        y, m, d = map(int, pushed.split("-"))
        days = (date.today() - date(y, m, d)).days
    except Exception:
        return pushed
    if days <= 30: return f"active (commit {pushed})"
    if days <= 90: return f"maintained (commit {pushed})"
    if days <= 365: return f"slow ({pushed})"
    return f"stale ({pushed})"

def maturity(t):
    """Maturity score 0-100 from PUBLIC GitHub signals only — popularity (log
    stars) + maintenance recency + a permissive-license bonus. Reproducible
    computed signal, NOT an editorial quality judgment. Full formula: /methodology.html"""
    if not t.get("github") or t.get("gh_stars") is None:
        return None
    stars = t.get("gh_stars") or 0
    pop = min(55, round(13.7 * math.log10(stars + 1)))
    rec = recency_points(t.get("gh_pushed_at"))
    openness = 10 if t.get("gh_license") else 0
    return min(100, pop + rec + openness)

def maturity_label(score):
    # Linear-dark palette: indigo accent for the strongest signal, neutral otherwise.
    if score is None: return ("—", "neutral")
    if score >= 80: return ("Mature", "indigo")
    if score >= 60: return ("Established", "indigo")
    if score >= 40: return ("Growing", "neutral")
    return ("Early", "neutral")

def lang_chrome(lang, root, alt_url):
    """Build the language-aware chrome (logo link, header nav, account widget,
    EN/中 switcher, footer) for a directory/blog page.

    🔴 This nav is an EXACT replica of src/layouts/Brand.astro's nav so that
    navigating between the main Astro site and the /tools directory/blog is
    seamless — same items, same links, same language logic. The page's language
    determines `sp` (zh → "/zh", en → ""), so EVERY link stays in the page's
    language: a zh page's logo → /zh/, 服务 → /zh/services, etc. No English leak.

    The switcher NEVER 404s: the inactive side points to a real same-section page
    in the other language (alt_url) when one exists, else that language's home."""
    html_lang = "zh-CN" if lang == "zh" else "en"
    sp = "/zh" if lang == "zh" else ""          # language path prefix (Brand: sp)
    logo_href = f"{sp}/"                          # Brand: a href={`${sp}/`}
    blog_url = "/tools/blog/zh/" if lang == "zh" else "/tools/blog/"  # Brand: blogUrl

    L = {
        "zh": {"tools": "工具", "services": "服务", "pricing": "定价", "history": "我的记录",
               "blog": "博客", "contact": "联系", "login": "登录", "account": "我的账户",
               "logout": "退出登录", "points": "点", "methodology": "方法论"},
        "en": {"tools": "Tools", "services": "Services", "pricing": "Pricing", "history": "History",
               "blog": "Blog", "contact": "Contact", "login": "Login", "account": "Account",
               "logout": "Log out", "points": "pts", "methodology": "Methodology"},
    }[lang]

    # Header nav — identical item set + order + classes to Brand.astro.
    # (Tools is a plain link to the directory, mirroring Brand's footer Tools link;
    #  the catalog dropdown lives on the Astro /services page.)
    nav_links = (
        f'<a href="/tools/" class="transition-colors hover:text-white">{L["tools"]}</a>'
        f'<a href="{sp}/services" class="transition-colors hover:text-white">{L["services"]}</a>'
        f'<a href="{sp}/pricing" class="transition-colors hover:text-white">{L["pricing"]}</a>'
        f'<a href="{sp}/history" class="transition-colors hover:text-white">{L["history"]}</a>'
        f'<a href="{blog_url}" class="transition-colors hover:text-white">{L["blog"]}</a>'
        f'<a href="{sp}/about" class="transition-colors hover:text-white">{L["contact"]}</a>')

    # Account affordance — server-rendered 登录/Login link (same markup as Brand);
    # the acct_script below replaces it with the points menu when /u/me has a session.
    acct_html = (
        f'<div id="ps-acct" class="text-sm" style="min-width:1px;">'
        f'<a href="{sp}/signin" class="transition-colors hover:text-white" style="color:#9CA0A8;">{L["login"]}</a>'
        f'</div>')

    if lang == "zh":
        en_target = alt_url or "https://panshi.io/tools/"
        switcher = (
            f'<a href="{en_target}" class="transition-colors hover:text-white" style="color:#62666D;">EN</a>'
            '<span style="color:#36383d;">/</span>'
            '<span style="color:#F7F8F8;font-weight:600;">中</span>')
        footer_tagline = ("由一名在生产环境运行多 agent 自动化的工程师打造。本目录独立于任何厂商,"
                          "数据均对照一手来源核实,欢迎指正。")
    else:
        zh_target = alt_url or "https://panshi.io/zh/"
        switcher = (
            '<span style="color:#F7F8F8;font-weight:600;">EN</span>'
            '<span style="color:#36383d;">/</span>'
            f'<a href="{zh_target}" class="transition-colors hover:text-white" style="color:#62666D;">中</a>')
        footer_tagline = (f"Built by an engineer running multi-agent automation in production. {SITE} is an "
                          "independent directory with no vendor affiliation — data verified against primary "
                          "sources, corrections welcome.")

    # Footer links — same item set as Brand's footer (+ directory-specific methodology).
    footer_links = (
        f'<a class="transition-colors hover:text-white" href="/tools/">{L["tools"]}</a>'
        f'<a class="transition-colors hover:text-white" href="{sp}/services">{L["services"]}</a>'
        f'<a class="transition-colors hover:text-white" href="{sp}/pricing">{L["pricing"]}</a>'
        f'<a class="transition-colors hover:text-white" href="{sp}/history">{L["history"]}</a>'
        f'<a class="transition-colors hover:text-white" href="{blog_url}">{L["blog"]}</a>'
        f'<a class="transition-colors hover:text-white" href="{root}methodology.html">{L["methodology"]}</a>'
        '<a class="ps-link" href="mailto:hi@panshi.io">hi@panshi.io</a>')

    # Account script — ported from Brand.astro's #ps-acct inline script. Renders
    # the points menu from cache + /u/me, with logout. sp/labels injected per-lang.
    acct_script = f"""<script>
(function () {{
  var box = document.getElementById('ps-acct');
  if (!box) return;
  var sp = {json.dumps(sp)};
  var nav = {{ points: {json.dumps(L["points"])}, account: {json.dumps(L["account"])}, history: {json.dumps(L["history"])}, logout: {json.dumps(L["logout"])}, login: {json.dumps(L["login"])} }};
  var CACHE_KEY = 'ps_acct';
  function esc(s){{return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}}
  function renderAccount(d) {{
    window.__PS_USER = true;
    box.innerHTML =
      '<div class="nav-dd">' +
        '<button type="button" class="nav-dd__btn flex items-center gap-1.5 transition-colors hover:text-white" aria-haspopup="true" aria-expanded="false" style="color:#F7F8F8;">' +
          '<span style="display:inline-block;width:7px;height:7px;border-radius:999px;background:#5E6AD2;"></span>' +
          '<span style="font-weight:600;">' + esc(d.points) + ' ' + esc(nav.points) + '</span>' +
          '<svg class="nav-dd__chev" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>' +
        '</button>' +
        '<div class="nav-dd__panel" role="menu" style="left:auto;right:0;width:220px;">' +
          '<div style="padding:8px 10px 6px;font-size:12px;color:#62666D;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:4px;word-break:break-all;">' + esc(d.email) + '</div>' +
          '<a href="' + sp + '/account" class="ps-acct__item" role="menuitem" style="display:block;padding:9px 10px;border-radius:9px;font-size:14px;color:#9CA0A8;text-decoration:none;">' + esc(nav.account) + '</a>' +
          '<a href="' + sp + '/history" class="ps-acct__item" role="menuitem" style="display:block;padding:9px 10px;border-radius:9px;font-size:14px;color:#9CA0A8;text-decoration:none;">' + esc(nav.history) + '</a>' +
          '<button type="button" id="ps-logout" class="ps-acct__item" role="menuitem" style="display:block;width:100%;padding:9px 10px;border-radius:9px;font-size:14px;color:#9CA0A8;background:none;border:0;text-align:left;cursor:pointer;">' + esc(nav.logout) + '</button>' +
        '</div>' +
      '</div>';
    var dd = box.querySelector('.nav-dd');
    var btn = dd && dd.querySelector('.nav-dd__btn');
    if (btn) {{
      btn.addEventListener('click', function (e) {{
        e.preventDefault();
        var open = dd.getAttribute('data-open') === 'true';
        dd.setAttribute('data-open', open ? 'false' : 'true');
        btn.setAttribute('aria-expanded', open ? 'false' : 'true');
      }});
      document.addEventListener('click', function (e) {{ if (!dd.contains(e.target)) dd.setAttribute('data-open','false'); }});
    }}
    var lo = box.querySelector('#ps-logout');
    if (lo) lo.addEventListener('click', function () {{
      try {{ localStorage.removeItem(CACHE_KEY); }} catch (e) {{}}
      window.__PS_USER = false;
      fetch('/u/logout', {{ method: 'POST' }}).then(function () {{ location.reload(); }});
    }});
  }}
  function renderLogin() {{
    window.__PS_USER = false;
    box.innerHTML = '<a href="' + sp + '/signin" class="transition-colors hover:text-white" style="color:#9CA0A8;">' + esc(nav.login) + '</a>';
  }}
  var renderedFromCache = false;
  try {{
    var raw = localStorage.getItem(CACHE_KEY);
    if (raw) {{ var cached = JSON.parse(raw); if (cached && cached.email != null) {{ renderAccount(cached); renderedFromCache = true; }} }}
  }} catch (e) {{}}
  fetch('/u/me').then(function(r){{return r.json();}}).then(function(d){{
    if (d && d.ok) {{
      try {{ localStorage.setItem(CACHE_KEY, JSON.stringify({{ email: d.email, points: d.points }})); }} catch (e) {{}}
      renderAccount(d);
    }} else {{
      try {{ localStorage.removeItem(CACHE_KEY); }} catch (e) {{}}
      if (renderedFromCache) renderLogin();
    }}
  }}).catch(function(){{}});
}})();
</script>"""

    return html_lang, logo_href, nav_links, acct_html, switcher, footer_tagline, footer_links, acct_script


def page(title, desc, body, path, root="", jsonld=None, og_type="website", lang="en", alt_url=None):
    url = f"{BASE}/{path}"
    ld = ('<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + "</script>") if jsonld else ""
    html_lang, logo_href, nav_links, acct_html, switcher, footer_tagline, footer_links, acct_script = lang_chrome(lang, root, alt_url)
    h = f"""<!doctype html><html lang="{html_lang}" class="antialiased"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#08090A">
<link rel="icon" href="/tools/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{esc(SITE)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/tools/styles.css">{DARK_CSS}{CF_BEACON}{ld}</head>
<body class="font-sans antialiased min-h-screen flex flex-col" style="background:#08090A;color:#9CA0A8;">
<header class="sticky top-0 z-40 backdrop-blur-xl" style="background:rgba(8,9,10,0.72);border-bottom:1px solid rgba(255,255,255,0.08);">
<div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
<a href="{logo_href}" class="flex items-center gap-2.5 font-semibold tracking-tight" style="color:#F7F8F8;">
<span class="inline-block w-2.5 h-2.5 rounded-sm" style="background:#5E6AD2;"></span>
<span class="text-[15px]">Panshi</span>
</a>
<nav class="hidden sm:flex items-center gap-8 text-sm font-medium" style="color:#9CA0A8;">
{nav_links}
</nav>
<div class="flex items-center gap-4">
{acct_html}
<div class="flex items-center gap-2.5 text-sm" data-lang-switch>
{switcher}
</div>
</div>
</div>
</header>
<main class="flex-1">
{body}
</main>
<footer class="mt-24" style="border-top:1px solid rgba(255,255,255,0.08);background:#0B0C0D;">
<div class="max-w-6xl mx-auto px-6 py-14 text-sm" style="color:#62666D;">
<div class="flex items-center gap-2.5 font-semibold tracking-tight" style="color:#F7F8F8;">
<span class="inline-block w-2.5 h-2.5 rounded-sm" style="background:#5E6AD2;"></span>
<span>Panshi</span>
</div>
<p class="mt-4 max-w-md leading-relaxed">{footer_tagline}</p>
<p class="mt-6 flex flex-wrap gap-x-6 gap-y-2 font-medium">
{footer_links}
</p>
<p class="mt-8 text-xs font-mono" style="color:#3f4248;">© 2026 panshi.io</p>
</div>
</footer>
{acct_script}
</body></html>"""
    fp = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(h)
    return path

def crumbs(items):
    """items: list of (name, path-or-None). Returns BreadcrumbList json-ld."""
    el = []
    for i, (name, p) in enumerate(items, 1):
        it = {"@type": "ListItem", "position": i, "name": name}
        if p:
            it["item"] = f"{BASE}/{p}"
        el.append(it)
    return {"@type": "BreadcrumbList", "itemListElement": el}

def faq(qas):
    """qas: list of (question, answer). Returns (html_section, FAQPage schema dict).
    GEO: answer-engines quote FAQ Q&A; every answer here is generated from verified data."""
    items = "".join(
        f'<div class="mt-4"><p class="font-medium" style="color:#F7F8F8;">{esc(q)}</p>'
        f'<p class="mt-1" style="color:#9CA0A8;">{esc(a)}</p></div>' for q, a in qas)
    h = ('<section class="mt-12"><h2 class="text-xl font-semibold" style="color:#F7F8F8;">'
         'Frequently asked questions</h2>' + items + '</section>')
    sch = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]}
    return h, sch

def tool_qas(t):
    qas = []
    if t.get("open_source"):
        qas.append((f"Is {t['name']} open source?",
                    "Yes." + (f" Licensed under {t['gh_license']}." if t.get("gh_license") else "")))
    else:
        qas.append((f"Is {t['name']} open source?",
                    f"No — {t['name']} is a proprietary/commercial product."))
    qas.append((f"Can I self-host {t['name']}?",
                f"Yes — {t['name']} can run in your own infrastructure." if t.get("self_hostable")
                else f"No — {t['name']} is cloud-only; there is no self-hosted deployment."))
    if "otel_native" in t:
        qas.append((f"Is {t['name']} OpenTelemetry-native?",
                    f"Yes — {t['name']} speaks OpenTelemetry (OTLP) natively, so there is no proprietary-SDK lock-in."
                    if t["otel_native"] else
                    f"No — {t['name']} relies on a proprietary SDK/format rather than native OpenTelemetry."))
    if t.get("pricing_model"):
        ans = t["pricing_model"].capitalize() + "." + (f" {t['pricing_note']}" if t.get("pricing_note") else "")
        qas.append((f"How much does {t['name']} cost?", ans))
    return qas

def vs_verdict(a, b):
    diffs = []
    if bool(a.get("open_source")) != bool(b.get("open_source")):
        o, c = (a, b) if a.get("open_source") else (b, a)
        diffs.append(f"{o['name']} is open-source while {c['name']} is proprietary")
    if bool(a.get("self_hostable")) != bool(b.get("self_hostable")):
        o, c = (a, b) if a.get("self_hostable") else (b, a)
        diffs.append(f"{o['name']} can be self-hosted while {c['name']} is cloud-only")
    if a.get("otel_native") is not None and b.get("otel_native") is not None and a.get("otel_native") != b.get("otel_native"):
        o, c = (a, b) if a.get("otel_native") else (b, a)
        diffs.append(f"{o['name']} is OpenTelemetry-native (no lock-in) while {c['name']} uses a proprietary SDK")
    if not diffs:
        return (f"{a['name']} and {b['name']} are closely matched on licensing, self-hosting and "
                "OpenTelemetry support — the decision comes down to pricing and framework integrations below.")
    return "Key difference: " + "; ".join(diffs) + "."

_BADGE = {
    # Linear-dark tints (inline styles, purge-proof): neutral hairline pill by
    # default, indigo for the primary accent, restrained red/amber for
    # sunset/acquired status. NO emerald/green anywhere.
    "neutral":"background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#9CA0A8;",
    "slate":  "background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#9CA0A8;",
    "indigo": "background:rgba(94,106,210,0.12);border:1px solid rgba(94,106,210,0.35);color:#aab2ee;",
    "blue":   "background:rgba(94,106,210,0.12);border:1px solid rgba(94,106,210,0.35);color:#aab2ee;",
    "sky":    "background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#9CA0A8;",
    "violet": "background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#9CA0A8;",
    "teal":   "background:rgba(94,106,210,0.12);border:1px solid rgba(94,106,210,0.35);color:#aab2ee;",
    "amber":  "background:rgba(217,164,65,0.12);border:1px solid rgba(217,164,65,0.35);color:#e2b25c;",
    "red":    "background:rgba(220,80,80,0.12);border:1px solid rgba(220,80,80,0.38);color:#f08a8a;",
    "rose":   "background:rgba(220,80,80,0.12);border:1px solid rgba(220,80,80,0.38);color:#f08a8a;",
}
def badge(txt, color="neutral"):
    st = _BADGE.get(color, _BADGE["neutral"])
    return f'<span class="text-xs px-2 py-0.5 rounded" style="{st}">{esc(txt)}</span>'

def card(t, root=""):
    badges = [badge(CATS[t["category"]][0], "indigo")]
    if t.get("open_source"): badges.append(badge("open source","neutral"))
    if t.get("self_hostable"): badges.append(badge("self-hostable","neutral"))
    pm = t.get("pricing_model")
    if pm: badges.append(badge(pm,"amber"))
    if t.get("otel_native"): badges.append(badge("OTel-native","indigo"))
    for tg in (t.get("tags") or []): badges.append(badge(tg,"indigo"))
    ms = maturity(t); ml = maturity_label(ms)
    if t.get("gh_stars") is not None:
        badges.append(badge("★ " + fmt_stars(t.get("gh_stars")), "neutral"))
        badges.append(badge(ml[0], ml[1]))
    note = t.get("funding_note") or ""
    status = ""
    low = (note + (t.get("pricing_note") or "")).lower()
    if "shut down" in low or "maintenance mode" in low: status = badge("⚠ sunset/maintenance","red")
    elif "acquired" in low: status = badge("acquired","rose")
    return f"""<article class="rounded-xl p-5 transition-all" style="background:#0F1011;border:1px solid rgba(255,255,255,0.08);" onmouseover="this.style.borderColor='rgba(255,255,255,0.14)'" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'" data-cat="{t['category']}" data-tags="{esc(','.join(t.get('tags') or []).lower())}" data-name="{esc(t['name'].lower())}" data-stars="{t.get('gh_stars') or 0}" data-maturity="{ms or 0}">
<div class="flex items-start justify-between gap-2">
<h3 class="font-semibold" style="color:#F7F8F8;"><a href="{root}tools/{slug(t['name'])}.html" class="ps-link" style="color:#F7F8F8;" onmouseover="this.style.color='#6E79E0'" onmouseout="this.style.color='#F7F8F8'">{esc(t['name'])}</a></h3>
<div class="flex flex-wrap gap-1 justify-end">{status}</div></div>
<p class="text-sm mt-2" style="color:#9CA0A8;">{esc(t['one_liner'])}</p>
<div class="flex flex-wrap gap-1.5 mt-3">{''.join(badges)}</div>
</article>"""

def tool_page(t):
    c = CATS[t["category"]]
    rows = [
        ("Category", c[0]),
        ("Open source", "Yes" if t.get("open_source") else "No"),
        ("Self-hostable", "Yes" if t.get("self_hostable") else "No"),
        ("Pricing model", t.get("pricing_model") or "—"),
        ("Pricing notes", t.get("pricing_note") or "—"),
        ("Framework integrations", ", ".join(t.get("frameworks") or []) or "—"),
        ("Funding / ownership", t.get("funding_note") or "—"),
    ]
    if "otel_native" in t:
        rows.insert(1, ("OpenTelemetry-native", "Yes — no proprietary-SDK lock-in" if t["otel_native"] else "No (proprietary SDK/format)"))
    if t.get("tags"):
        rows.append(("Tags", ", ".join(t["tags"])))
    has_gh = bool(t.get("github") and t.get("gh_stars") is not None)
    if has_gh:
        ms = maturity(t); ml = maturity_label(ms)
        rows += [
            ("GitHub stars", f"{t['gh_stars']:,}"),
            ("Maintenance", recency_label(t.get("gh_pushed_at"))),
            ("License (GitHub)", t.get("gh_license") or "not detected"),
            ("Open issues", str(t.get("gh_open_issues")) if t.get("gh_open_issues") is not None else "—"),
            ("Maturity signal", f"{ms}/100 ({ml[0]})  — computed from public GitHub signals, see methodology"),
        ]
    tr = "".join(f'<tr style="border-bottom:1px solid rgba(255,255,255,0.08);"><td class="py-2 pr-6 align-top whitespace-nowrap" style="color:#62666D;">{esc(k)}</td><td class="py-2" style="color:#C8CCD2;">{esc(v)}</td></tr>' for k,v in rows)
    links = f'<a href="{esc(t["url"])}" rel="nofollow" class="inline-block font-semibold px-5 py-2.5 rounded-lg transition-colors" style="background:#5E6AD2;color:#fff;" onmouseover="this.style.background=\'#6E79E0\'" onmouseout="this.style.background=\'#5E6AD2\'">Website ↗</a>'
    if t.get("github"):
        links += f' <a href="{esc(t["github"])}" rel="nofollow" class="inline-block px-5 py-2.5 rounded-lg ml-2 transition-colors" style="border:1px solid rgba(255,255,255,0.14);color:#F7F8F8;" onmouseover="this.style.borderColor=\'rgba(255,255,255,0.28)\'" onmouseout="this.style.borderColor=\'rgba(255,255,255,0.14)\'">GitHub ↗</a>'
    ev = t.get("evidence_url")
    evp = f'<p class="text-xs mt-6" style="color:#62666D;">Pricing/feature source: <a class="underline ps-link" rel="nofollow" href="{esc(ev)}">{esc(ev)}</a></p>' if ev else ""
    mnote = ('<p class="text-xs mt-2" style="color:#62666D;">Maturity signal is computed from public GitHub data only. '
             '<a class="underline ps-link" href="../methodology.html">How it is calculated</a>.</p>') if has_gh else ""
    faq_html, faq_sch = faq(tool_qas(t))
    body = f"""<div class="max-w-3xl mx-auto px-6 py-12">
<p class="text-sm mb-2" style="color:#62666D;"><a href="../index.html" class="hover:text-white" style="color:#62666D;">Home</a> / <a href="../categories/{t['category']}.html" class="ps-link">{esc(c[0])}</a></p>
<h1 class="text-3xl font-bold" style="color:#F7F8F8;">{esc(t['name'])}</h1>
<p class="mt-3 text-lg" style="color:#9CA0A8;">{esc(t['one_liner'])}</p>
<div class="mt-6">{links}</div>
<table class="w-full text-sm mt-8">{tr}</table>{evp}{mnote}{faq_html}</div>"""
    soft = {"@type": "SoftwareApplication", "name": t["name"], "applicationCategory": "DeveloperApplication",
            "operatingSystem": "Web", "description": t["one_liner"], "url": t["url"]}
    if t.get("github"):
        soft["sameAs"] = [t["github"]]
    jsonld = {"@context": "https://schema.org", "@graph": [soft, faq_sch,
              crumbs([("Home", "index.html"), (c[0], f"categories/{t['category']}.html"), (t["name"], f"tools/{slug(t['name'])}.html")])]}
    return page(f"{t['name']} — pricing, self-hosting & alternatives | {SITE}",
        f"{t['name']}: {t['one_liner'][:140]}", body, f"tools/{slug(t['name'])}.html", root="../",
        jsonld=jsonld, og_type="article")

def vs_row(label, a, b):
    return f'<tr style="border-bottom:1px solid rgba(255,255,255,0.08);"><td class="py-2 pr-4 whitespace-nowrap align-top" style="color:#62666D;">{esc(label)}</td><td class="py-2 pr-4 align-top" style="color:#C8CCD2;">{esc(a)}</td><td class="py-2 align-top" style="color:#C8CCD2;">{esc(b)}</td></tr>'

def compare_page(a, b):
    def f(t,k,d="—"): return t.get(k) or d
    yn = lambda v: "Yes" if v else "No"
    def mat(t):
        ms = maturity(t)
        return f"{ms}/100 ({maturity_label(ms)[0]})" if ms is not None else "— (no public repo)"
    def on(t):
        v = t.get("otel_native")
        return "Yes" if v is True else ("No" if v is False else "—")
    rows = "".join([
        vs_row("One-liner", a["one_liner"], b["one_liner"]),
        vs_row("Category", CATS[a["category"]][0], CATS[b["category"]][0]),
        vs_row("OpenTelemetry-native", on(a), on(b)),
        vs_row("Open source", yn(a.get("open_source")), yn(b.get("open_source"))),
        vs_row("Self-hostable", yn(a.get("self_hostable")), yn(b.get("self_hostable"))),
        vs_row("Pricing model", f(a,"pricing_model"), f(b,"pricing_model")),
        vs_row("Pricing notes", f(a,"pricing_note"), f(b,"pricing_note")),
        vs_row("Frameworks", ", ".join(a.get("frameworks") or []), ", ".join(b.get("frameworks") or [])),
        vs_row("GitHub stars", fmt_stars(a.get("gh_stars")), fmt_stars(b.get("gh_stars"))),
        vs_row("Maturity (GitHub signal)", mat(a), mat(b)),
        vs_row("Funding / ownership", f(a,"funding_note"), f(b,"funding_note")),
    ])
    pick = []
    if a.get("open_source") and not b.get("open_source"):
        pick.append(f"Choose {a['name']} if open-source licensing or full data control is a hard requirement.")
    if b.get("open_source") and not a.get("open_source"):
        pick.append(f"Choose {b['name']} if open-source licensing or full data control is a hard requirement.")
    if a.get("self_hostable") and not b.get("self_hostable"):
        pick.append(f"{a['name']} can run inside your own infrastructure; {b['name']} is cloud-only.")
    if b.get("self_hostable") and not a.get("self_hostable"):
        pick.append(f"{b['name']} can run inside your own infrastructure; {a['name']} is cloud-only.")
    pick.append("Both link to primary pricing sources below — verify current tiers before committing; this market shifts monthly.")
    picks = "".join(f"<li>{esc(p)}</li>" for p in pick)
    sa, sb = slug(a["name"]), slug(b["name"])
    vverdict = vs_verdict(a, b)
    yn3 = lambda v: "Yes" if v else "No"
    cqas = [
        (f"Is {a['name']} or {b['name']} open source?",
         f"{a['name']}: {yn3(a.get('open_source'))}. {b['name']}: {yn3(b.get('open_source'))}."),
        (f"Can {a['name']} and {b['name']} be self-hosted?",
         f"{a['name']}: {yn3(a.get('self_hostable'))}. {b['name']}: {yn3(b.get('self_hostable'))}."),
        (f"{a['name']} vs {b['name']}: which should I choose?", vverdict),
    ]
    cfaq_html, cfaq_sch = faq(cqas)
    body = f"""<div class="max-w-3xl mx-auto px-6 py-12">
<p class="text-sm mb-2" style="color:#62666D;"><a href="../index.html" class="hover:text-white" style="color:#62666D;">Home</a> / Comparisons</p>
<h1 class="text-3xl font-bold" style="color:#F7F8F8;">{esc(a['name'])} vs {esc(b['name'])}</h1>
<div class="mt-4 rounded-r-lg px-5 py-4" style="background:#0F1011;border:1px solid rgba(255,255,255,0.08);border-left:3px solid #5E6AD2;"><p class="text-sm font-semibold" style="color:#aab2ee;">Quick verdict</p><p class="mt-1" style="color:#C8CCD2;">{esc(vverdict)}</p></div>
<p class="mt-4" style="color:#9CA0A8;">Side-by-side comparison from the {SITE}: licensing, self-hosting, pricing model and integrations — no vendor copy, primary sources linked.</p>
<table class="w-full text-sm mt-8"><thead><tr class="text-left" style="color:#F7F8F8;border-bottom:1px solid rgba(255,255,255,0.14);">
<th class="py-2 pr-4"></th><th class="py-2 pr-4"><a class="ps-link" href="../tools/{sa}.html">{esc(a['name'])}</a></th><th class="py-2"><a class="ps-link" href="../tools/{sb}.html">{esc(b['name'])}</a></th></tr></thead>
<tbody>{rows}</tbody></table>
<h2 class="text-xl font-semibold mt-10" style="color:#F7F8F8;">How to choose</h2>
<ul class="list-disc list-inside mt-3 space-y-1" style="color:#9CA0A8;">{picks}</ul>
<p class="text-xs mt-8" style="color:#62666D;">Sources: <a class="underline ps-link" rel="nofollow" href="{esc(a.get('evidence_url') or a['url'])}">{esc(a['name'])}</a> · <a class="underline ps-link" rel="nofollow" href="{esc(b.get('evidence_url') or b['url'])}">{esc(b['name'])}</a></p>
{cfaq_html}
</div>"""
    jsonld = {"@context": "https://schema.org", "@graph": [cfaq_sch,
        crumbs([("Home", "index.html"), (f"{a['name']} vs {b['name']}", f"compare/{sa}-vs-{sb}.html")])]}
    return page(f"{a['name']} vs {b['name']} (2026) — pricing, self-hosting, integrations | {SITE}",
        f"Neutral {a['name']} vs {b['name']} comparison: licensing, self-hosting, pricing and framework integrations, with primary sources.",
        body, f"compare/{sa}-vs-{sb}.html", root="../", jsonld=jsonld, og_type="article")

# Linear-dark favicon: a #08090A rounded square with an indigo mark, matching the brand.
FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="13" fill="#08090A"/>'
           '<rect x="20" y="20" width="24" height="24" rx="5" fill="#5E6AD2"/></svg>')

def og_svg(n_tools):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">'
            f'<rect width="1200" height="630" fill="#08090A"/>'
            f'<rect x="40" y="40" width="1120" height="550" rx="24" fill="none" stroke="rgba(255,255,255,0.10)" stroke-width="2"/>'
            f'<rect x="100" y="118" width="44" height="44" rx="9" fill="#5E6AD2"/>'
            f'<text x="164" y="154" font-family="Inter,Segoe UI,Helvetica,Arial,sans-serif" font-size="40" font-weight="700" fill="#F7F8F8">Panshi · Tools</text>'
            f'<text x="100" y="320" font-family="Inter,Segoe UI,Helvetica,Arial,sans-serif" font-size="70" font-weight="800" fill="#F7F8F8">The neutral index of</text>'
            f'<text x="100" y="408" font-family="Inter,Segoe UI,Helvetica,Arial,sans-serif" font-size="70" font-weight="800" fill="#8b95ec">AI agent observability tooling</text>'
            f'<text x="100" y="510" font-family="Inter,Segoe UI,Helvetica,Arial,sans-serif" font-size="34" fill="#9CA0A8">{n_tools} tools · observability · evals · guardrails · cost — facts checked vs primary sources</text>'
            f'</svg>')

def best_page(spec, tools):
    sel = [t for t in tools if spec["match"](t)]
    sel.sort(key=lambda t: (maturity(t) or -1, t.get("gh_stars") or -1), reverse=True)
    n = len(sel)
    top = sel[0] if sel else None
    rows = ""
    for i, t in enumerate(sel, 1):
        ms = maturity(t); ml = maturity_label(ms)
        score = f"{ms}/100 ({ml[0]})" if ms is not None else "—"
        flags = []
        if t.get("open_source"): flags.append("OSS")
        if t.get("self_hostable"): flags.append("self-host")
        if t.get("otel_native"): flags.append("OTel-native")
        rows += (f'<tr style="border-bottom:1px solid rgba(255,255,255,0.08);"><td class="py-2 pr-4" style="color:#62666D;">{i}</td>'
                 f'<td class="py-2 pr-4"><a class="ps-link" href="../tools/{slug(t["name"])}.html">{esc(t["name"])}</a></td>'
                 f'<td class="py-2 pr-4" style="color:#C8CCD2;">{esc(score)}</td>'
                 f'<td class="py-2 pr-4" style="color:#C8CCD2;">{esc(t.get("pricing_model") or "—")}</td>'
                 f'<td class="py-2" style="color:#C8CCD2;">{esc(", ".join(flags))}</td></tr>')
    tp_name = esc(top["name"]) if top else "—"
    lead_ans = (f"Top pick by our maturity signal: <strong style=\"color:#F7F8F8;\">{tp_name}</strong>. "
                f"Below are all {n} {spec['crit']} tools we track, ranked by the same objective GitHub-derived score. "
                "Maturity measures adoption and upkeep, not subjective quality — pick by your own constraints.")
    body = f"""<div class="max-w-3xl mx-auto px-6 py-12">
<p class="text-sm mb-2" style="color:#62666D;"><a href="../index.html" class="hover:text-white" style="color:#62666D;">Home</a> / Best lists</p>
<h1 class="text-3xl font-bold" style="color:#F7F8F8;">{esc(spec['h1'])}</h1>
<div class="mt-4 rounded-r-lg px-5 py-4" style="background:#0F1011;border:1px solid rgba(255,255,255,0.08);border-left:3px solid #5E6AD2;"><p class="text-sm font-semibold" style="color:#aab2ee;">Quick answer</p><p class="mt-1" style="color:#C8CCD2;">{lead_ans}</p></div>
<p class="mt-4" style="color:#9CA0A8;">{esc(spec['lead'])} Ranking method is public — see <a class="ps-link" href="../methodology.html">methodology</a>. Note: maturity reflects total GitHub adoption, so large general-purpose platforms (e.g. Grafana, Sentry, PostHog) can rank high on the strength of their parent project even where their LLM-specific features are newer — read the flags and pick by your constraints. Listings are free and editorially independent; sponsorship never changes facts or ranking.</p>
<table class="w-full text-sm mt-8"><thead><tr class="text-left" style="color:#F7F8F8;border-bottom:1px solid rgba(255,255,255,0.14);"><th class="py-2 pr-4">#</th><th class="py-2 pr-4">Tool</th><th class="py-2 pr-4">Maturity</th><th class="py-2 pr-4">Pricing</th><th class="py-2">Flags</th></tr></thead><tbody>{rows}</tbody></table></div>"""
    items = [{"@type": "ListItem", "position": i, "name": t["name"],
              "url": f"{BASE}/tools/{slug(t['name'])}.html"} for i, t in enumerate(sel, 1)]
    qas = [(spec["h1"].replace("Best", "What is the best") + "?",
            (f"By our public maturity signal (GitHub stars + recency + license), {top['name']} ranks highest among the {n} {spec['crit']} tools we track. Maturity reflects adoption and upkeep, not subjective quality." if top else "No tools currently match.")),
           ("How is this ranking decided?",
            "Tools are ranked by a reproducible maturity score computed only from public GitHub signals (log of stars + last-commit recency + license). The formula is published on our methodology page; ranking is never sold.")]
    fhtml, fsch = faq(qas)
    body = body.replace("</main>", fhtml + "</main>", 1)
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ItemList", "name": spec["h1"], "numberOfItems": n, "itemListElement": items},
        fsch, crumbs([("Home", "index.html"), (spec["h1"], f"best/{spec['slug']}.html")])]}
    return page(f"{spec['title']} | {SITE}",
                spec["lead"][:155], body, f"best/{spec['slug']}.html", root="../", jsonld=jsonld)

def main():
    tools = json.load(open("data/tools.json", encoding="utf-8"))
    tools.sort(key=lambda t: t["name"].lower())
    by = {}
    for t in tools: by.setdefault(t["category"], []).append(t)
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    paths = []

    for t in tools: paths.append(tool_page(t))

    name2tool = {t["name"]: t for t in tools}
    cmp_links = []
    for an, bn in COMPARE_PAIRS:
        a, b = name2tool[an], name2tool[bn]
        paths.append(compare_page(a, b))
        cmp_links.append(f'<a href="compare/{slug(an)}-vs-{slug(bn)}.html" class="transition-all rounded-lg px-4 py-3 text-sm" style="background:#0F1011;border:1px solid rgba(255,255,255,0.08);color:#C8CCD2;" onmouseover="this.style.borderColor=\'rgba(255,255,255,0.14)\'" onmouseout="this.style.borderColor=\'rgba(255,255,255,0.08)\'">{esc(an)} <span style="color:#62666D;">vs</span> {esc(bn)}</a>')

    for spec in BEST_PAGES:
        paths.append(best_page(spec, tools))

    for ck,(cn,cd) in CATS.items():
        items = "".join(card(t, root="../") for t in by.get(ck, []))
        body = f"""<div class="max-w-5xl mx-auto px-6 py-12">
<p class="text-sm mb-2" style="color:#62666D;"><a href="../index.html" class="hover:text-white" style="color:#62666D;">Home</a> / {esc(cn)}</p>
<h1 class="text-3xl font-bold" style="color:#F7F8F8;">{esc(cn)}</h1><p class="mt-2" style="color:#9CA0A8;">{esc(cd)} {len(by.get(ck,[]))} tools tracked.</p>
<div class="grid md:grid-cols-2 gap-4 mt-8">{items}</div></div>"""
        jsonld = {"@context": "https://schema.org", "@graph": [
            {"@type": "CollectionPage", "name": cn, "description": cd, "url": f"{BASE}/categories/{ck}.html"},
            crumbs([("Home", "index.html"), (cn, f"categories/{ck}.html")])]}
        paths.append(page(f"{cn} tools (2026) — {len(by.get(ck,[]))} compared | {SITE}", cd, body, f"categories/{ck}.html", root="../", jsonld=jsonld))

    cat_chips = '<button data-f="all" class="fbtn fbtn-on px-3 py-1.5 rounded-lg text-sm font-semibold">All</button>' + "".join(
        f'<button data-f="{k}" class="fbtn px-3 py-1.5 rounded-lg text-sm">{esc(v[0])} ({len(by.get(k,[]))})</button>' for k,v in CATS.items())
    _all_tags = {}
    for _t in tools:
        for _tg in (_t.get("tags") or []):
            _all_tags[_tg] = _all_tags.get(_tg, 0) + 1
    for _tg in sorted(_all_tags):
        cat_chips += f'<button data-ftag="{esc(_tg.lower())}" class="fbtn px-3 py-1.5 rounded-lg text-sm">{esc(_tg)} ({_all_tags[_tg]})</button>' 
    best_chips = "".join(f'<a href="best/{esc(sp["slug"])}.html" class="transition-all rounded-lg px-4 py-3 text-sm" style="background:#0F1011;border:1px solid rgba(255,255,255,0.08);color:#C8CCD2;" onmouseover="this.style.borderColor=\'rgba(255,255,255,0.14)\'" onmouseout="this.style.borderColor=\'rgba(255,255,255,0.08)\'">{esc(sp["h1"])}</a>' for sp in BEST_PAGES)
    cards = "".join(card(t) for t in tools)
    body = f"""<section class="max-w-5xl mx-auto px-6 pt-16 pb-10">
<h1 class="text-4xl md:text-5xl font-bold leading-tight" style="color:#F7F8F8;">The neutral index of<br><span style="color:#8b95ec;">AI agent observability</span> tooling</h1>
<p class="mt-5 text-lg max-w-2xl" style="color:#9CA0A8;">{esc(TAG)} {len(tools)} tools tracked across tracing, evals, guardrails, prompt management, cost and debugging — with licensing, self-hosting and pricing-model facts checked against primary sources. Built by an engineer who runs agent fleets in production, not by a vendor marketing team.</p>
<div class="mt-4 text-sm" style="color:#62666D;">Maintained by <span class="font-medium" style="color:#F7F8F8;">Panshi</span> · updated {BUILD_DATE}</div></section>
<section id="compare" class="max-w-5xl mx-auto px-6 pb-4"><h2 class="text-xl font-semibold mb-4" style="color:#F7F8F8;">Popular comparisons</h2>
<div class="grid sm:grid-cols-2 md:grid-cols-3 gap-3">{''.join(cmp_links)}</div></section>
<section id="best" class="max-w-5xl mx-auto px-6 pb-4"><h2 class="text-xl font-semibold mb-4" style="color:#F7F8F8;">Best-of lists</h2>
<div class="grid sm:grid-cols-2 md:grid-cols-3 gap-3">{best_chips}</div></section>
<section id="tools" class="max-w-5xl mx-auto px-6 py-10">
<h2 class="text-xl font-semibold mb-4" style="color:#F7F8F8;">All tools</h2>
<div class="flex flex-col sm:flex-row gap-3 mb-5">
<input id="q" type="search" placeholder="Search {len(tools)} tools…" class="ps-search flex-1 rounded-lg px-4 py-2 text-sm outline-none" aria-label="Search tools">
<div class="flex gap-2 text-sm"><span class="py-2" style="color:#62666D;">Sort:</span>
<button data-s="name" class="sbtn px-3 py-1.5 rounded-lg">A–Z</button>
<button data-s="stars" class="sbtn px-3 py-1.5 rounded-lg">Stars</button>
<button data-s="maturity" class="sbtn px-3 py-1.5 rounded-lg">Maturity</button></div></div>
<div class="flex flex-wrap gap-2 mb-6">{cat_chips}</div>
<p id="count" class="text-xs mb-3" style="color:#62666D;"></p>
<div id="grid" class="grid md:grid-cols-2 gap-4">{cards}</div>
<p id="empty" class="hidden py-8 text-center" style="color:#62666D;">No tools match your search.</p></section>
<script>
const grid=document.getElementById('grid'),q=document.getElementById('q'),countEl=document.getElementById('count'),emptyEl=document.getElementById('empty');
let curCat='all',curTag='';
function apply(){{
 const term=(q.value||'').trim().toLowerCase();let shown=0;
 grid.querySelectorAll('[data-cat]').forEach(c=>{{
  const okCat=(curCat==='all'||c.dataset.cat===curCat)&&(!curTag||((c.dataset.tags||'').split(',').includes(curTag)));
  const okTerm=!term||c.dataset.name.includes(term)||c.textContent.toLowerCase().includes(term);
  const vis=okCat&&okTerm;c.style.display=vis?'':'none';if(vis)shown++;}});
 countEl.textContent=shown+' tool'+(shown===1?'':'s')+' shown';
 emptyEl.classList.toggle('hidden',shown!==0);}}
q.addEventListener('input',apply);
document.querySelectorAll('.fbtn').forEach(b=>b.onclick=()=>{{
 document.querySelectorAll('.fbtn').forEach(x=>{{x.classList.remove('fbtn-on','font-semibold');}});
 b.classList.add('fbtn-on','font-semibold');
 if(b.dataset.ftag!==undefined){{curTag=b.dataset.ftag;curCat='all';}}else{{curCat=b.dataset.f;curTag='';}}apply();}});
document.querySelectorAll('.sbtn').forEach(b=>b.onclick=()=>{{
 document.querySelectorAll('.sbtn').forEach(x=>x.classList.remove('sbtn-on'));
 b.classList.add('sbtn-on');
 const k=b.dataset.s,items=[...grid.children];
 items.sort((x,y)=>k==='name'?x.dataset.name.localeCompare(y.dataset.name):(Number(y.dataset[k])-Number(x.dataset[k])));
 items.forEach(i=>grid.appendChild(i));apply();}});
apply();
</script>"""
    home_ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "name": SITE, "url": BASE, "description": TAG},
        {"@type": "ItemList", "name": "AI agent observability, evals & guardrails tools",
         "numberOfItems": len(tools),
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t["name"],
                              "url": f"{BASE}/tools/{slug(t['name'])}.html"} for i, t in enumerate(tools)]}]}
    paths.append(page(f"{SITE} (2026) — {len(tools)} LLM observability, evals & guardrails tools compared", TAG, body, "index.html", jsonld=home_ld))

    # methodology page
    meth_body = """<div class="max-w-3xl mx-auto px-6 py-12">
<p class="text-sm mb-2" style="color:#62666D;"><a href="index.html" class="hover:text-white" style="color:#62666D;">Home</a> / Methodology</p>
<h1 class="text-3xl font-bold" style="color:#F7F8F8;">Methodology</h1>
<p class="mt-4" style="color:#9CA0A8;">This index is editorially independent. Listings are free and sponsorship never changes facts, scores or rankings. Here is exactly how every data point is produced, so you can audit it.</p>
<h2 class="text-xl font-semibold mt-8" style="color:#F7F8F8;">Factual fields</h2>
<p class="mt-2" style="color:#9CA0A8;">Open-source status, self-hostability, pricing model, pricing notes, framework integrations, OpenTelemetry-native support and funding/ownership are read from each tool's primary sources (official site, pricing page, repository, docs). Every tool page links its source. Spotted something stale? Email <a class="ps-link" href="mailto:hi@panshi.io">hi@panshi.io</a> and it is fixed within 24h.</p>
<h2 class="text-xl font-semibold mt-8" style="color:#F7F8F8;">GitHub signals</h2>
<p class="mt-2" style="color:#9CA0A8;">For tools with a public repository we read four objective signals directly from the GitHub API: star count, date of the last push, detected license, and open-issue count. These are facts, not opinions.</p>
<h2 class="text-xl font-semibold mt-8" style="color:#F7F8F8;">Maturity signal (0–100)</h2>
<p class="mt-2" style="color:#9CA0A8;">A reproducible composite of the public GitHub signals above. It measures adoption and upkeep — <em>not</em> product quality, and it is never sold. Tools without a public repo have no score. The formula:</p>
<pre class="rounded-lg p-4 text-sm mt-3 overflow-x-auto" style="background:#0a0b0c;border:1px solid rgba(255,255,255,0.08);color:#C8CCD2;">popularity   = min(55, round(13.7 &times; log10(stars + 1)))     # ~55 at 10k+ stars
maintenance  = 35 if pushed &le; 30d, 25 if &le; 90d, 14 if &le; 180d,
                6 if &le; 365d, else 0
openness     = 10 if an OSI license is detected, else 0
maturity     = min(100, popularity + maintenance + openness)</pre>
<p class="mt-3" style="color:#9CA0A8;">Bands: Mature &ge; 80, Established &ge; 60, Growing &ge; 40, Early below 40.</p>
<h2 class="text-xl font-semibold mt-8" style="color:#F7F8F8;">What we do not do</h2>
<p class="mt-2" style="color:#9CA0A8;">We do not inject vendor marketing copy, we do not rank by who pays, and we do not publish performance benchmarks we have not actually run. When hands-on test results are added, they will be labelled as tested and dated.</p>
</div>"""
    meth_ld = {"@context": "https://schema.org", "@graph": [crumbs([("Home", "index.html"), ("Methodology", "methodology.html")])]}
    paths.append(page(f"Methodology — how the data and scores are produced | {SITE}",
        "How the Agent Observability Index produces every factual field and the GitHub-based maturity signal. Fully reproducible, editorially independent.",
        meth_body, "methodology.html", jsonld=meth_ld))

    # advertise page
    body = f"""<div class="max-w-3xl mx-auto px-6 py-12">
<h1 class="text-3xl font-bold" style="color:#F7F8F8;">Get your tool featured</h1>
<p class="mt-4" style="color:#9CA0A8;">The index is read by engineers choosing their observability, evals and guardrails stack — transactional-intent traffic, not casual browsing.</p>
<div class="grid md:grid-cols-2 gap-6 mt-8">
<div class="rounded-2xl p-6" style="background:#0F1011;border:1px solid rgba(94,106,210,0.35);">
<h2 class="font-semibold" style="color:#F7F8F8;">Featured listing</h2>
<ul class="text-sm mt-3 space-y-1 list-disc list-inside" style="color:#9CA0A8;"><li>Pinned placement in your category + homepage</li><li>“Featured” badge and expanded card</li><li>Launch pricing, first 10 vendors</li></ul>
<p class="mt-4 font-mono" style="color:#aab2ee;">$99 / year (launch price)</p>
<a href="https://buy.stripe.com/eVqeV59sGapNcnLdCk5AQ00" class="inline-block mt-4 font-semibold px-5 py-2.5 rounded-lg transition-colors" style="background:#5E6AD2;color:#fff;" onmouseover="this.style.background='#6E79E0'" onmouseout="this.style.background='#5E6AD2'">Get featured — $99</a></div>
<div class="rounded-2xl p-6" style="background:#0F1011;border:1px solid rgba(255,255,255,0.08);">
<h2 class="font-semibold" style="color:#F7F8F8;">Category sponsor</h2>
<ul class="text-sm mt-3 space-y-1 list-disc list-inside" style="color:#9CA0A8;"><li>Exclusive banner on one category page</li><li>Included in comparison-page footers of that category</li><li>One slot per category</li></ul>
<p class="mt-4 font-mono" style="color:#aab2ee;">$490 / year</p>
<a href="https://buy.stripe.com/eVq5kvcES8hF9bzbuc5AQ01" class="inline-block mt-4 font-semibold px-5 py-2.5 rounded-lg transition-colors" style="border:1px solid rgba(255,255,255,0.14);color:#F7F8F8;" onmouseover="this.style.borderColor='rgba(255,255,255,0.28)'" onmouseout="this.style.borderColor='rgba(255,255,255,0.14)'">Sponsor a category — $490</a></div></div>
<p class="mt-8" style="color:#9CA0A8;">Listings themselves are free and editorially controlled — sponsorship never changes facts or rankings.</p>
<p class="mt-6 text-sm" style="color:#62666D;">After payment, reply to the Stripe receipt (or email <a class="ps-link" href="mailto:hi@panshi.io">hi@panshi.io</a>) with your tool name — placement goes live within 24h. Questions first? Just email.</p>
</div>"""
    paths.append(page(f"Advertise — featured listings & category sponsorship | {SITE}",
        "Reach engineers choosing their LLM observability and evals stack. Featured listings from $99/year.", body, "advertise.html"))

    # 404
    body404 = f"""<div class="max-w-3xl mx-auto px-6 py-24 text-center">
<h1 class="text-5xl font-bold" style="color:#F7F8F8;">404</h1>
<p class="mt-4" style="color:#9CA0A8;">That page is not in the index. The tool may have been renamed, or the link is out of date.</p>
<a href="/tools/index.html" class="inline-block mt-8 font-semibold px-5 py-2.5 rounded-lg transition-colors" style="background:#5E6AD2;color:#fff;" onmouseover="this.style.background='#6E79E0'" onmouseout="this.style.background='#5E6AD2'">Browse all tools</a>
</div>"""
    page("Page not found | " + SITE, "Page not found.", body404, "404.html")  # not in sitemap

    # static assets
    open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write(FAVICON)
    if os.path.isdir("static"):
        for fn in os.listdir("static"):
            shutil.copy(os.path.join("static", fn), os.path.join(OUT, fn))

    # blog — generated in BOTH languages so a zh visitor lands on Chinese content
    # and the per-page EN/中 toggle always resolves to a real counterpart (no 404).
    #   EN: /tools/blog/  +  /tools/blog/<slug>.html      (root "../")
    #   ZH: /tools/blog/zh/  +  /tools/blog/zh/<slug>.html (root "../../")
    BLOG_T = {
        "en": {"home": "Home", "blog": "Blog", "h1": "Blog",
               "lead": "Field notes on AI agent observability, GEO and choosing a neutral tooling stack.",
               "meta": "Field notes on AI agent observability, GEO and neutral tooling selection.",
               "title": lambda p: p["title"], "desc": lambda p: p["description"],
               "body": lambda p: p["body"], "faqs": lambda p: p.get("faq", [])},
        "zh": {"home": "首页", "blog": "博客", "h1": "博客",
               "lead": "关于 AI agent 可观测性、GEO 以及如何选择中立工具栈的实践笔记。",
               "meta": "关于 AI agent 可观测性、GEO 与中立工具选型的实践笔记。",
               "title": lambda p: p.get("title_zh") or p["title"], "desc": lambda p: p.get("description_zh") or p["description"],
               "body": lambda p: p.get("body_zh") or p["body"], "faqs": lambda p: p.get("faq_zh") or p.get("faq", [])},
    }
    for blang in ("en", "zh"):
        T = BLOG_T[blang]
        prefix = "blog/" if blang == "en" else "blog/zh/"
        proot = "../" if blang == "en" else "../../"
        home_href = ("../index.html" if blang == "en" else "../../index.html")
        for post in POSTS:
            ptitle, pdesc, pbodytext = T["title"](post), T["desc"](post), T["body"](post)
            fhtml, fsch = faq(T["faqs"](post))
            # cross-language counterpart for the switcher
            alt = (f"{BASE}/blog/zh/{post['slug']}.html" if blang == "en" else f"{BASE}/blog/{post['slug']}.html")
            pbody = f"""<div class="max-w-3xl mx-auto px-6 py-12">
<p class="text-sm mb-2" style="color:#62666D;"><a href="{home_href}" class="hover:text-white" style="color:#62666D;">{T['home']}</a> / <a href="index.html" class="hover:text-white" style="color:#62666D;">{T['blog']}</a></p>
<h1 class="text-3xl font-bold leading-tight" style="color:#F7F8F8;">{esc(ptitle)}</h1>
<p class="text-sm mt-3" style="color:#62666D;">{esc(post['date'])} · {esc(', '.join(post.get('tags', [])))}</p>
<div class="mt-8 prose-dark">{pbodytext}</div>
{fhtml}</div>"""
            art = {"@type": "Article", "headline": ptitle, "description": pdesc,
                   "datePublished": post["date"], "inLanguage": ("zh-CN" if blang == "zh" else "en"),
                   "author": {"@type": "Organization", "name": SITE},
                   "publisher": {"@type": "Organization", "name": "Panshi"},
                   "url": f"{BASE}/{prefix}{post['slug']}.html"}
            pld = {"@context": "https://schema.org", "@graph": [art, fsch,
                   crumbs([(T['home'], "index.html"), (T['blog'], f"{prefix}index.html"), (ptitle, f"{prefix}{post['slug']}.html")])]}
            paths.append(page(f"{ptitle} | {SITE}", pdesc, pbody,
                              f"{prefix}{post['slug']}.html", root=proot, jsonld=pld,
                              og_type="article", lang=blang, alt_url=alt))
        if POSTS:
            items = "".join(
                f'<article class="rounded-xl p-5 transition-all" style="background:#0F1011;border:1px solid rgba(255,255,255,0.08);" onmouseover="this.style.borderColor=\'rgba(255,255,255,0.14)\'" onmouseout="this.style.borderColor=\'rgba(255,255,255,0.08)\'">'
                f'<h2 class="font-semibold" style="color:#F7F8F8;"><a class="transition-colors" style="color:#F7F8F8;" href="{esc(po["slug"])}.html" onmouseover="this.style.color=\'#6E79E0\'" onmouseout="this.style.color=\'#F7F8F8\'">{esc(T["title"](po))}</a></h2>'
                f'<p class="text-xs mt-1" style="color:#62666D;">{esc(po["date"])}</p>'
                f'<p class="text-sm mt-2" style="color:#9CA0A8;">{esc(T["desc"](po))}</p></article>'
                for po in POSTS)
            bbody = f"""<div class="max-w-3xl mx-auto px-6 py-12">
<h1 class="text-3xl font-bold" style="color:#F7F8F8;">{T['h1']}</h1>
<p class="mt-2" style="color:#9CA0A8;">{T['lead']}</p>
<div class="grid gap-4 mt-8">{items}</div></div>"""
            balt = (f"{BASE}/blog/zh/" if blang == "en" else f"{BASE}/blog/")
            bld = {"@context": "https://schema.org", "@graph": [
                {"@type": "Blog", "name": f"{SITE} Blog", "url": f"{BASE}/{prefix}index.html",
                 "inLanguage": ("zh-CN" if blang == "zh" else "en")},
                crumbs([(T['home'], "index.html"), (T['blog'], f"{prefix}index.html")])]}
            paths.append(page(f"{T['h1']} | {SITE}", T["meta"],
                              bbody, f"{prefix}index.html", root=proot, jsonld=bld,
                              lang=blang, alt_url=balt))

    sm = "".join(f"<url><loc>{BASE}/{p}</loc><lastmod>{BUILD_DATE}</lastmod></url>" for p in sorted(set(paths)))
    open(os.path.join(OUT,"sitemap.xml"),"w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    # IndexNow key (accelerates Bing/Yandex indexing -> gates ChatGPT citations)
    INDEXNOW_KEY = "198c801d18754d8698ac988786a9b5ca"
    open(os.path.join(OUT, INDEXNOW_KEY + ".txt"), "w").write(INDEXNOW_KEY)
    # llms.txt — map for AI engines / coding agents
    lt = [f"# {SITE}", "", f"> A neutral, no-vendor-affiliation directory of AI agent observability, evals and guardrails tools — {len(tools)} tools, facts checked against primary sources.", ""]
    lt.append("## Best-of lists")
    for sp in BEST_PAGES:
        lt.append(f"- [{sp['h1']}]({BASE}/best/{sp['slug']}.html)")
    lt.append("")
    lt.append("## Comparisons")
    for an, bn in COMPARE_PAIRS:
        lt.append(f"- [{an} vs {bn}]({BASE}/compare/{slug(an)}-vs-{slug(bn)}.html)")
    lt.append("")
    lt.append("## Tools")
    for t in tools:
        lt.append(f"- [{t['name']}]({BASE}/tools/{slug(t['name'])}.html): {t['one_liner']}")
    lt.append("")
    lt.append("## Articles")
    for po in POSTS:
        lt.append(f"- [{po['title']}]({BASE}/blog/{po['slug']}.html): {po['description']}")
    lt.append(f"- [Methodology]({BASE}/methodology.html)")
    open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write("\n".join(lt) + "\n")
    # machine-readable data export (CC-BY) — crawlable by AI engines / list authors
    export = []
    for t in tools:
        ms = maturity(t)
        export.append({"name": t["name"], "url": t.get("url"),
                       "listing": f"{BASE}/tools/{slug(t['name'])}.html",
                       "category": t.get("category"), "open_source": t.get("open_source"),
                       "self_hostable": t.get("self_hostable"), "pricing_model": t.get("pricing_model"),
                       "otel_native": t.get("otel_native"), "gh_stars": t.get("gh_stars"),
                       "maturity": ms})
    open(os.path.join(OUT, "data.json"), "w", encoding="utf-8").write(json.dumps(
        {"name": SITE, "url": BASE, "license": "CC-BY-4.0", "generated": BUILD_DATE,
         "count": len(tools), "tools": export}, ensure_ascii=False, indent=1))
    print(f"built {len(paths)} pages + sitemap + 404 + favicon + og ({len(tools)} tools)")

if __name__ == "__main__":
    main()
