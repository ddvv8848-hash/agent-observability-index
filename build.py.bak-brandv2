#!/usr/bin/env python3
"""Static site generator for the Agent Observability Index (by Panshi)."""
import json, os, re, shutil, html, math
from datetime import date

BASE = "https://tools.panshi.io"  # custom domain live 2026-06-13
SITE = "Agent Observability Index"
TAG = "Every AI agent observability, evals, guardrails & cost tool — compared by a neutral third party."
OUT = "site"
BUILD_DATE = date.today().isoformat()
OG_IMAGE = BASE + "/og.png"
CF_BEACON = ("<script defer src='https://static.cloudflareinsights.com/beacon.min.js' "
             "data-cf-beacon='{\"token\": \"1cd7fde310f94d97a9660eedd270b154\"}'></script>")

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
    if score is None: return ("—", "slate")
    if score >= 80: return ("Mature", "emerald")
    if score >= 60: return ("Established", "sky")
    if score >= 40: return ("Growing", "violet")
    return ("Early", "slate")

def page(title, desc, body, path, root="", jsonld=None, og_type="website"):
    url = f"{BASE}/{path}"
    ld = ('<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + "</script>") if jsonld else ""
    h = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#020617">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
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
<link rel="stylesheet" href="/styles.css">{CF_BEACON}{ld}</head>
<body class="bg-slate-950 text-slate-200 antialiased">
<nav class="border-b border-slate-800"><div class="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
<a href="{root}index.html" class="font-bold text-white">Agent<span class="text-emerald-400">Obs</span> Index</a>
<div class="flex gap-5 text-sm">
<a href="{root}index.html#tools" class="hover:text-white">Tools</a>
<a href="{root}index.html#compare" class="hover:text-white">Comparisons</a>
<a href="{root}blog/index.html" class="hover:text-white">Blog</a>
<a href="{root}methodology.html" class="hover:text-white">Methodology</a>
<a href="{root}advertise.html" class="text-emerald-400 hover:text-emerald-300">Get featured</a>
</div></div></nav>
{body}
<footer class="border-t border-slate-800 mt-16"><div class="max-w-5xl mx-auto px-6 py-8 text-sm text-slate-500">
<p>{SITE} — independent directory, no vendor affiliation. Data verified against primary sources; corrections welcome via <a class="text-emerald-400" href="mailto:hi@panshi.io">email</a>.</p>
<p class="mt-2">© 2026 Panshi · <a class="hover:text-slate-300" href="{root}index.html">Home</a> · <a class="hover:text-slate-300" href="{root}methodology.html">Methodology</a> · <a class="hover:text-slate-300" href="{root}advertise.html">Advertise</a></p>
</div></footer></body></html>"""
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
        f'<div class="mt-4"><p class="font-medium text-slate-200">{esc(q)}</p>'
        f'<p class="text-slate-400 mt-1">{esc(a)}</p></div>' for q, a in qas)
    h = ('<section class="mt-12"><h2 class="text-xl font-semibold text-white">'
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

def badge(txt, color="slate"):
    return f'<span class="text-xs px-2 py-0.5 rounded bg-{color}-800/60 border border-{color}-700 text-{color}-200">{esc(txt)}</span>'

def card(t, root=""):
    badges = [badge(CATS[t["category"]][0], "emerald")]
    if t.get("open_source"): badges.append(badge("open source","sky"))
    if t.get("self_hostable"): badges.append(badge("self-hostable","violet"))
    pm = t.get("pricing_model")
    if pm: badges.append(badge(pm,"amber"))
    if t.get("otel_native"): badges.append(badge("OTel-native","teal"))
    ms = maturity(t); ml = maturity_label(ms)
    if t.get("gh_stars") is not None:
        badges.append(badge("★ " + fmt_stars(t.get("gh_stars")), "slate"))
        badges.append(badge(ml[0], ml[1]))
    note = t.get("funding_note") or ""
    status = ""
    low = (note + (t.get("pricing_note") or "")).lower()
    if "shut down" in low or "maintenance mode" in low: status = badge("⚠ sunset/maintenance","red")
    elif "acquired" in low: status = badge("acquired","rose")
    return f"""<article class="bg-slate-900 rounded-xl p-5 border border-slate-800 hover:border-slate-600" data-cat="{t['category']}" data-name="{esc(t['name'].lower())}" data-stars="{t.get('gh_stars') or 0}" data-maturity="{ms or 0}">
<div class="flex items-start justify-between gap-2">
<h3 class="font-semibold text-white"><a href="{root}tools/{slug(t['name'])}.html" class="hover:text-emerald-400">{esc(t['name'])}</a></h3>
<div class="flex flex-wrap gap-1 justify-end">{status}</div></div>
<p class="text-sm text-slate-400 mt-2">{esc(t['one_liner'])}</p>
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
    tr = "".join(f'<tr class="border-b border-slate-800"><td class="py-2 pr-6 text-slate-400 align-top whitespace-nowrap">{esc(k)}</td><td class="py-2">{esc(v)}</td></tr>' for k,v in rows)
    links = f'<a href="{esc(t["url"])}" rel="nofollow" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold px-5 py-2.5 rounded-lg">Website ↗</a>'
    if t.get("github"):
        links += f' <a href="{esc(t["github"])}" rel="nofollow" class="border border-slate-700 hover:border-slate-500 px-5 py-2.5 rounded-lg ml-2">GitHub ↗</a>'
    ev = t.get("evidence_url")
    evp = f'<p class="text-xs text-slate-600 mt-6">Pricing/feature source: <a class="underline" rel="nofollow" href="{esc(ev)}">{esc(ev)}</a></p>' if ev else ""
    mnote = ('<p class="text-xs text-slate-600 mt-2">Maturity signal is computed from public GitHub data only. '
             '<a class="underline" href="../methodology.html">How it is calculated</a>.</p>') if has_gh else ""
    faq_html, faq_sch = faq(tool_qas(t))
    body = f"""<main class="max-w-3xl mx-auto px-6 py-12">
<p class="text-sm text-slate-500 mb-2"><a href="../index.html" class="hover:text-slate-300">Home</a> / <a href="../categories/{t['category']}.html" class="text-emerald-400">{esc(c[0])}</a></p>
<h1 class="text-3xl font-bold text-white">{esc(t['name'])}</h1>
<p class="mt-3 text-lg text-slate-400">{esc(t['one_liner'])}</p>
<div class="mt-6">{links}</div>
<table class="w-full text-sm mt-8">{tr}</table>{evp}{mnote}{faq_html}</main>"""
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
    return f'<tr class="border-b border-slate-800"><td class="py-2 pr-4 text-slate-400 whitespace-nowrap align-top">{esc(label)}</td><td class="py-2 pr-4 align-top">{esc(a)}</td><td class="py-2 align-top">{esc(b)}</td></tr>'

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
    body = f"""<main class="max-w-3xl mx-auto px-6 py-12">
<p class="text-sm text-slate-500 mb-2"><a href="../index.html" class="hover:text-slate-300">Home</a> / Comparisons</p>
<h1 class="text-3xl font-bold text-white">{esc(a['name'])} vs {esc(b['name'])}</h1>
<div class="mt-4 bg-slate-900 border-l-4 border-emerald-500 rounded-r-lg px-5 py-4"><p class="text-sm font-semibold text-emerald-400">Quick verdict</p><p class="text-slate-300 mt-1">{esc(vverdict)}</p></div>
<p class="mt-4 text-slate-400">Side-by-side comparison from the {SITE}: licensing, self-hosting, pricing model and integrations — no vendor copy, primary sources linked.</p>
<table class="w-full text-sm mt-8"><thead><tr class="text-left text-slate-300 border-b border-slate-700">
<th class="py-2 pr-4"></th><th class="py-2 pr-4"><a class="text-emerald-400" href="../tools/{sa}.html">{esc(a['name'])}</a></th><th class="py-2"><a class="text-emerald-400" href="../tools/{sb}.html">{esc(b['name'])}</a></th></tr></thead>
<tbody>{rows}</tbody></table>
<h2 class="text-xl font-semibold text-white mt-10">How to choose</h2>
<ul class="list-disc list-inside text-slate-400 mt-3 space-y-1">{picks}</ul>
<p class="text-xs text-slate-600 mt-8">Sources: <a class="underline" rel="nofollow" href="{esc(a.get('evidence_url') or a['url'])}">{esc(a['name'])}</a> · <a class="underline" rel="nofollow" href="{esc(b.get('evidence_url') or b['url'])}">{esc(b['name'])}</a></p>
{cfaq_html}
</main>"""
    jsonld = {"@context": "https://schema.org", "@graph": [cfaq_sch,
        crumbs([("Home", "index.html"), (f"{a['name']} vs {b['name']}", f"compare/{sa}-vs-{sb}.html")])]}
    return page(f"{a['name']} vs {b['name']} (2026) — pricing, self-hosting, integrations | {SITE}",
        f"Neutral {a['name']} vs {b['name']} comparison: licensing, self-hosting, pricing and framework integrations, with primary sources.",
        body, f"compare/{sa}-vs-{sb}.html", root="../", jsonld=jsonld, og_type="article")

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="13" fill="#020617"/>'
           '<circle cx="32" cy="32" r="17" fill="none" stroke="#34d399" stroke-width="5"/>'
           '<circle cx="32" cy="32" r="5.5" fill="#34d399"/></svg>')

def og_svg(n_tools):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">'
            f'<rect width="1200" height="630" fill="#020617"/>'
            f'<rect x="40" y="40" width="1120" height="550" rx="24" fill="none" stroke="#1e293b" stroke-width="2"/>'
            f'<circle cx="120" cy="140" r="34" fill="none" stroke="#34d399" stroke-width="9"/><circle cx="120" cy="140" r="11" fill="#34d399"/>'
            f'<text x="184" y="154" font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="40" font-weight="700" fill="#ffffff">AgentObs Index</text>'
            f'<text x="100" y="320" font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="70" font-weight="800" fill="#ffffff">The neutral index of</text>'
            f'<text x="100" y="408" font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="70" font-weight="800" fill="#34d399">AI agent observability tooling</text>'
            f'<text x="100" y="510" font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="34" fill="#94a3b8">{n_tools} tools · observability · evals · guardrails · cost — facts checked vs primary sources</text>'
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
        rows += (f'<tr class="border-b border-slate-800"><td class="py-2 pr-4 text-slate-500">{i}</td>'
                 f'<td class="py-2 pr-4"><a class="text-emerald-400" href="../tools/{slug(t["name"])}.html">{esc(t["name"])}</a></td>'
                 f'<td class="py-2 pr-4">{esc(score)}</td>'
                 f'<td class="py-2 pr-4">{esc(t.get("pricing_model") or "—")}</td>'
                 f'<td class="py-2">{esc(", ".join(flags))}</td></tr>')
    tp_name = esc(top["name"]) if top else "—"
    lead_ans = (f"Top pick by our maturity signal: <strong class=\"text-slate-200\">{tp_name}</strong>. "
                f"Below are all {n} {spec['crit']} tools we track, ranked by the same objective GitHub-derived score. "
                "Maturity measures adoption and upkeep, not subjective quality — pick by your own constraints.")
    body = f"""<main class="max-w-3xl mx-auto px-6 py-12">
<p class="text-sm text-slate-500 mb-2"><a href="../index.html" class="hover:text-slate-300">Home</a> / Best lists</p>
<h1 class="text-3xl font-bold text-white">{esc(spec['h1'])}</h1>
<div class="mt-4 bg-slate-900 border-l-4 border-emerald-500 rounded-r-lg px-5 py-4"><p class="text-sm font-semibold text-emerald-400">Quick answer</p><p class="text-slate-300 mt-1">{lead_ans}</p></div>
<p class="mt-4 text-slate-400">{esc(spec['lead'])} Ranking method is public — see <a class="text-emerald-400" href="../methodology.html">methodology</a>. Note: maturity reflects total GitHub adoption, so large general-purpose platforms (e.g. Grafana, Sentry, PostHog) can rank high on the strength of their parent project even where their LLM-specific features are newer — read the flags and pick by your constraints. Listings are free and editorially independent; sponsorship never changes facts or ranking.</p>
<table class="w-full text-sm mt-8"><thead><tr class="text-left text-slate-300 border-b border-slate-700"><th class="py-2 pr-4">#</th><th class="py-2 pr-4">Tool</th><th class="py-2 pr-4">Maturity</th><th class="py-2 pr-4">Pricing</th><th class="py-2">Flags</th></tr></thead><tbody>{rows}</tbody></table></main>"""
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
        cmp_links.append(f'<a href="compare/{slug(an)}-vs-{slug(bn)}.html" class="bg-slate-900 border border-slate-800 hover:border-slate-600 rounded-lg px-4 py-3 text-sm">{esc(an)} <span class="text-slate-500">vs</span> {esc(bn)}</a>')

    for spec in BEST_PAGES:
        paths.append(best_page(spec, tools))

    for ck,(cn,cd) in CATS.items():
        items = "".join(card(t, root="../") for t in by.get(ck, []))
        body = f"""<main class="max-w-5xl mx-auto px-6 py-12">
<p class="text-sm text-slate-500 mb-2"><a href="../index.html" class="hover:text-slate-300">Home</a> / {esc(cn)}</p>
<h1 class="text-3xl font-bold text-white">{esc(cn)}</h1><p class="mt-2 text-slate-400">{esc(cd)} {len(by.get(ck,[]))} tools tracked.</p>
<div class="grid md:grid-cols-2 gap-4 mt-8">{items}</div></main>"""
        jsonld = {"@context": "https://schema.org", "@graph": [
            {"@type": "CollectionPage", "name": cn, "description": cd, "url": f"{BASE}/categories/{ck}.html"},
            crumbs([("Home", "index.html"), (cn, f"categories/{ck}.html")])]}
        paths.append(page(f"{cn} tools (2026) — {len(by.get(ck,[]))} compared | {SITE}", cd, body, f"categories/{ck}.html", root="../", jsonld=jsonld))

    cat_chips = '<button data-f="all" class="fbtn bg-emerald-500 text-slate-950 px-3 py-1.5 rounded-lg text-sm font-semibold">All</button>' + "".join(
        f'<button data-f="{k}" class="fbtn border border-slate-700 px-3 py-1.5 rounded-lg text-sm hover:border-slate-500">{esc(v[0])} ({len(by.get(k,[]))})</button>' for k,v in CATS.items())
    best_chips = "".join(f'<a href="best/{esc(sp["slug"])}.html" class="bg-slate-900 border border-slate-800 hover:border-slate-600 rounded-lg px-4 py-3 text-sm">{esc(sp["h1"])}</a>' for sp in BEST_PAGES)
    cards = "".join(card(t) for t in tools)
    body = f"""<header class="max-w-5xl mx-auto px-6 pt-16 pb-10">
<h1 class="text-4xl md:text-5xl font-bold text-white leading-tight">The neutral index of<br><span class="text-emerald-400">AI agent observability</span> tooling</h1>
<p class="mt-5 text-lg text-slate-400 max-w-2xl">{esc(TAG)} {len(tools)} tools tracked across tracing, evals, guardrails, prompt management, cost and debugging — with licensing, self-hosting and pricing-model facts checked against primary sources. Built by an engineer who runs agent fleets in production, not by a vendor marketing team.</p>
<div class="mt-4 text-sm text-slate-500">Maintained by <span class="text-slate-300">Panshi</span> · updated {BUILD_DATE}</div></header>
<section id="compare" class="max-w-5xl mx-auto px-6 pb-4"><h2 class="text-xl font-semibold text-white mb-4">Popular comparisons</h2>
<div class="grid sm:grid-cols-2 md:grid-cols-3 gap-3">{''.join(cmp_links)}</div></section>
<section id="best" class="max-w-5xl mx-auto px-6 pb-4"><h2 class="text-xl font-semibold text-white mb-4">Best-of lists</h2>
<div class="grid sm:grid-cols-2 md:grid-cols-3 gap-3">{best_chips}</div></section>
<section id="tools" class="max-w-5xl mx-auto px-6 py-10">
<h2 class="text-xl font-semibold text-white mb-4">All tools</h2>
<div class="flex flex-col sm:flex-row gap-3 mb-5">
<input id="q" type="search" placeholder="Search {len(tools)} tools…" class="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-emerald-500 outline-none" aria-label="Search tools">
<div class="flex gap-2 text-sm"><span class="text-slate-500 py-2">Sort:</span>
<button data-s="name" class="sbtn border border-slate-700 px-3 py-1.5 rounded-lg hover:border-slate-500">A–Z</button>
<button data-s="stars" class="sbtn border border-slate-700 px-3 py-1.5 rounded-lg hover:border-slate-500">Stars</button>
<button data-s="maturity" class="sbtn border border-slate-700 px-3 py-1.5 rounded-lg hover:border-slate-500">Maturity</button></div></div>
<div class="flex flex-wrap gap-2 mb-6">{cat_chips}</div>
<p id="count" class="text-xs text-slate-500 mb-3"></p>
<div id="grid" class="grid md:grid-cols-2 gap-4">{cards}</div>
<p id="empty" class="hidden text-slate-500 py-8 text-center">No tools match your search.</p></section>
<script>
const grid=document.getElementById('grid'),q=document.getElementById('q'),countEl=document.getElementById('count'),emptyEl=document.getElementById('empty');
let curCat='all';
function apply(){{
 const term=(q.value||'').trim().toLowerCase();let shown=0;
 grid.querySelectorAll('[data-cat]').forEach(c=>{{
  const okCat=curCat==='all'||c.dataset.cat===curCat;
  const okTerm=!term||c.dataset.name.includes(term)||c.textContent.toLowerCase().includes(term);
  const vis=okCat&&okTerm;c.style.display=vis?'':'none';if(vis)shown++;}});
 countEl.textContent=shown+' tool'+(shown===1?'':'s')+' shown';
 emptyEl.classList.toggle('hidden',shown!==0);}}
q.addEventListener('input',apply);
document.querySelectorAll('.fbtn').forEach(b=>b.onclick=()=>{{
 document.querySelectorAll('.fbtn').forEach(x=>{{x.className='fbtn border border-slate-700 px-3 py-1.5 rounded-lg text-sm hover:border-slate-500';}});
 b.className='fbtn bg-emerald-500 text-slate-950 px-3 py-1.5 rounded-lg text-sm font-semibold';
 curCat=b.dataset.f;apply();}});
document.querySelectorAll('.sbtn').forEach(b=>b.onclick=()=>{{
 document.querySelectorAll('.sbtn').forEach(x=>x.classList.remove('border-emerald-500','text-emerald-400'));
 b.classList.add('border-emerald-500','text-emerald-400');
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
    meth_body = """<main class="max-w-3xl mx-auto px-6 py-12">
<p class="text-sm text-slate-500 mb-2"><a href="index.html" class="hover:text-slate-300">Home</a> / Methodology</p>
<h1 class="text-3xl font-bold text-white">Methodology</h1>
<p class="mt-4 text-slate-400">This index is editorially independent. Listings are free and sponsorship never changes facts, scores or rankings. Here is exactly how every data point is produced, so you can audit it.</p>
<h2 class="text-xl font-semibold text-white mt-8">Factual fields</h2>
<p class="mt-2 text-slate-400">Open-source status, self-hostability, pricing model, pricing notes, framework integrations, OpenTelemetry-native support and funding/ownership are read from each tool's primary sources (official site, pricing page, repository, docs). Every tool page links its source. Spotted something stale? Email <a class="text-emerald-400" href="mailto:hi@panshi.io">hi@panshi.io</a> and it is fixed within 24h.</p>
<h2 class="text-xl font-semibold text-white mt-8">GitHub signals</h2>
<p class="mt-2 text-slate-400">For tools with a public repository we read four objective signals directly from the GitHub API: star count, date of the last push, detected license, and open-issue count. These are facts, not opinions.</p>
<h2 class="text-xl font-semibold text-white mt-8">Maturity signal (0–100)</h2>
<p class="mt-2 text-slate-400">A reproducible composite of the public GitHub signals above. It measures adoption and upkeep — <em>not</em> product quality, and it is never sold. Tools without a public repo have no score. The formula:</p>
<pre class="bg-slate-900 border border-slate-800 rounded-lg p-4 text-sm text-slate-300 mt-3 overflow-x-auto">popularity   = min(55, round(13.7 &times; log10(stars + 1)))     # ~55 at 10k+ stars
maintenance  = 35 if pushed &le; 30d, 25 if &le; 90d, 14 if &le; 180d,
                6 if &le; 365d, else 0
openness     = 10 if an OSI license is detected, else 0
maturity     = min(100, popularity + maintenance + openness)</pre>
<p class="mt-3 text-slate-400">Bands: Mature &ge; 80, Established &ge; 60, Growing &ge; 40, Early below 40.</p>
<h2 class="text-xl font-semibold text-white mt-8">What we do not do</h2>
<p class="mt-2 text-slate-400">We do not inject vendor marketing copy, we do not rank by who pays, and we do not publish performance benchmarks we have not actually run. When hands-on test results are added, they will be labelled as tested and dated.</p>
</main>"""
    meth_ld = {"@context": "https://schema.org", "@graph": [crumbs([("Home", "index.html"), ("Methodology", "methodology.html")])]}
    paths.append(page(f"Methodology — how the data and scores are produced | {SITE}",
        "How the Agent Observability Index produces every factual field and the GitHub-based maturity signal. Fully reproducible, editorially independent.",
        meth_body, "methodology.html", jsonld=meth_ld))

    # advertise page
    body = f"""<main class="max-w-3xl mx-auto px-6 py-12">
<h1 class="text-3xl font-bold text-white">Get your tool featured</h1>
<p class="mt-4 text-slate-400">The index is read by engineers choosing their observability, evals and guardrails stack — transactional-intent traffic, not casual browsing.</p>
<div class="grid md:grid-cols-2 gap-6 mt-8">
<div class="bg-slate-900 rounded-2xl p-6 border border-emerald-700">
<h2 class="font-semibold text-white">Featured listing</h2>
<ul class="text-sm text-slate-400 mt-3 space-y-1 list-disc list-inside"><li>Pinned placement in your category + homepage</li><li>“Featured” badge and expanded card</li><li>Launch pricing, first 10 vendors</li></ul>
<p class="mt-4 text-emerald-400 font-mono">$99 / year (launch price)</p>
<a href="https://buy.stripe.com/eVqeV59sGapNcnLdCk5AQ00" class="inline-block mt-4 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold px-5 py-2.5 rounded-lg">Get featured — $99</a></div>
<div class="bg-slate-900 rounded-2xl p-6 border border-slate-800">
<h2 class="font-semibold text-white">Category sponsor</h2>
<ul class="text-sm text-slate-400 mt-3 space-y-1 list-disc list-inside"><li>Exclusive banner on one category page</li><li>Included in comparison-page footers of that category</li><li>One slot per category</li></ul>
<p class="mt-4 text-emerald-400 font-mono">$490 / year</p>
<a href="https://buy.stripe.com/eVq5kvcES8hF9bzbuc5AQ01" class="inline-block mt-4 border border-emerald-600 hover:border-emerald-400 text-emerald-400 font-semibold px-5 py-2.5 rounded-lg">Sponsor a category — $490</a></div></div>
<p class="mt-8 text-slate-400">Listings themselves are free and editorially controlled — sponsorship never changes facts or rankings.</p>
<p class="mt-6 text-sm text-slate-500">After payment, reply to the Stripe receipt (or email <a class="text-emerald-400" href="mailto:hi@panshi.io">hi@panshi.io</a>) with your tool name — placement goes live within 24h. Questions first? Just email.</p>
</main>"""
    paths.append(page(f"Advertise — featured listings & category sponsorship | {SITE}",
        "Reach engineers choosing their LLM observability and evals stack. Featured listings from $99/year.", body, "advertise.html"))

    # 404
    body404 = f"""<main class="max-w-3xl mx-auto px-6 py-24 text-center">
<h1 class="text-5xl font-bold text-white">404</h1>
<p class="mt-4 text-slate-400">That page is not in the index. The tool may have been renamed, or the link is out of date.</p>
<a href="/index.html" class="inline-block mt-8 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold px-5 py-2.5 rounded-lg">Browse all tools</a>
</main>"""
    page("Page not found | " + SITE, "Page not found.", body404, "404.html")  # not in sitemap

    # static assets
    open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write(FAVICON)
    if os.path.isdir("static"):
        for fn in os.listdir("static"):
            shutil.copy(os.path.join("static", fn), os.path.join(OUT, fn))

    # blog
    for post in POSTS:
        fhtml, fsch = faq(post.get("faq", []))
        pbody = f"""<main class="max-w-3xl mx-auto px-6 py-12">
<p class="text-sm text-slate-500 mb-2"><a href="../index.html" class="hover:text-slate-300">Home</a> / <a href="index.html" class="hover:text-slate-300">Blog</a></p>
<h1 class="text-3xl font-bold text-white leading-tight">{esc(post['title'])}</h1>
<p class="text-sm text-slate-500 mt-3">{esc(post['date'])} · {esc(', '.join(post.get('tags', [])))}</p>
<div class="mt-8">{post['body']}</div>
{fhtml}</main>"""
        art = {"@type": "Article", "headline": post["title"], "description": post["description"],
               "datePublished": post["date"], "author": {"@type": "Organization", "name": SITE},
               "publisher": {"@type": "Organization", "name": "Panshi"},
               "url": f"{BASE}/blog/{post['slug']}.html"}
        pld = {"@context": "https://schema.org", "@graph": [art, fsch,
               crumbs([("Home", "index.html"), ("Blog", "blog/index.html"), (post["title"], f"blog/{post['slug']}.html")])]}
        paths.append(page(f"{post['title']} | {SITE}", post["description"], pbody,
                          f"blog/{post['slug']}.html", root="../", jsonld=pld, og_type="article"))
    if POSTS:
        items = "".join(
            f'<article class="bg-slate-900 rounded-xl p-5 border border-slate-800 hover:border-slate-600">'
            f'<h2 class="font-semibold text-white"><a class="hover:text-emerald-400" href="{esc(po["slug"])}.html">{esc(po["title"])}</a></h2>'
            f'<p class="text-xs text-slate-500 mt-1">{esc(po["date"])}</p>'
            f'<p class="text-sm text-slate-400 mt-2">{esc(po["description"])}</p></article>'
            for po in POSTS)
        bbody = f"""<main class="max-w-3xl mx-auto px-6 py-12">
<h1 class="text-3xl font-bold text-white">Blog</h1>
<p class="mt-2 text-slate-400">Field notes on AI agent observability, GEO and choosing a neutral tooling stack.</p>
<div class="grid gap-4 mt-8">{items}</div></main>"""
        bld = {"@context": "https://schema.org", "@graph": [
            {"@type": "Blog", "name": f"{SITE} Blog", "url": f"{BASE}/blog/index.html"},
            crumbs([("Home", "index.html"), ("Blog", "blog/index.html")])]}
        paths.append(page(f"Blog | {SITE}", "Field notes on AI agent observability, GEO and neutral tooling selection.",
                          bbody, "blog/index.html", root="../", jsonld=bld))

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
