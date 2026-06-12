#!/usr/bin/env python3
"""Static site generator for the Agent Observability Index (by Panshi)."""
import json, os, re, shutil, html

BASE = "https://akige.github.io/agent-observability-index"  # switch to https://tools.panshi.io when DNS lands
SITE = "Agent Observability Index"
TAG = "Every AI agent observability, evals, guardrails & cost tool — compared by a neutral third party."
OUT = "site"

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
 ("Helicone","Portkey"),("Guardrails AI","NVIDIA NeMo Guardrails"),("Lakera Guard","LLM Guard (Protect AI)"),
]

def slug(s):
    return re.sub(r"-+","-",re.sub(r"[^a-z0-9]+","-",s.lower())).strip("-")

def esc(s):
    return html.escape(s or "")

def page(title, desc, body, path, root=""):
    h = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{BASE}/{path}">
<script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-slate-950 text-slate-200 antialiased">
<nav class="border-b border-slate-800"><div class="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
<a href="{root}index.html" class="font-bold text-white">Agent<span class="text-emerald-400">Obs</span> Index</a>
<div class="flex gap-5 text-sm">
<a href="{root}index.html#tools" class="hover:text-white">Tools</a>
<a href="{root}index.html#compare" class="hover:text-white">Comparisons</a>
<a href="{root}advertise.html" class="text-emerald-400 hover:text-emerald-300">Get featured</a>
</div></div></nav>
{body}
<footer class="border-t border-slate-800 mt-16"><div class="max-w-5xl mx-auto px-6 py-8 text-sm text-slate-500">
<p>{SITE} — independent directory, no vendor affiliation. Data manually verified; corrections welcome via <a class="text-emerald-400" href="mailto:sysetc@gmail.com">email</a>.</p>
<p class="mt-2">© 2026 Panshi · <a class="hover:text-slate-300" href="{root}index.html">Home</a> · <a class="hover:text-slate-300" href="{root}advertise.html">Advertise</a></p>
</div></footer></body></html>"""
    fp = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(h)
    return path

def badge(txt, color="slate"):
    return f'<span class="text-xs px-2 py-0.5 rounded bg-{color}-800/60 border border-{color}-700 text-{color}-200">{esc(txt)}</span>'

def card(t, root=""):
    badges = [badge(CATS[t["category"]][0], "emerald")]
    if t.get("open_source"): badges.append(badge("open source","sky"))
    if t.get("self_hostable"): badges.append(badge("self-hostable","violet"))
    pm = t.get("pricing_model")
    if pm: badges.append(badge(pm,"amber"))
    note = t.get("funding_note") or ""
    status = ""
    low = (note + (t.get("pricing_note") or "")).lower()
    if "shut down" in low or "maintenance mode" in low: status = badge("⚠ sunset/maintenance","red")
    elif "acquired" in low: status = badge("acquired","rose")
    return f"""<article class="bg-slate-900 rounded-xl p-5 border border-slate-800 hover:border-slate-600" data-cat="{t['category']}">
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
    tr = "".join(f'<tr class="border-b border-slate-800"><td class="py-2 pr-6 text-slate-400 align-top whitespace-nowrap">{esc(k)}</td><td class="py-2">{esc(v)}</td></tr>' for k,v in rows)
    links = f'<a href="{esc(t["url"])}" rel="nofollow" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold px-5 py-2.5 rounded-lg">Website ↗</a>'
    if t.get("github"):
        links += f' <a href="{esc(t["github"])}" rel="nofollow" class="border border-slate-700 hover:border-slate-500 px-5 py-2.5 rounded-lg ml-2">GitHub ↗</a>'
    ev = t.get("evidence_url")
    evp = f'<p class="text-xs text-slate-600 mt-6">Pricing/feature source: <a class="underline" rel="nofollow" href="{esc(ev)}">{esc(ev)}</a></p>' if ev else ""
    body = f"""<main class="max-w-3xl mx-auto px-6 py-12">
<p class="text-sm text-slate-500 mb-2"><a href="../categories/{t['category']}.html" class="text-emerald-400">{esc(c[0])}</a></p>
<h1 class="text-3xl font-bold text-white">{esc(t['name'])}</h1>
<p class="mt-3 text-lg text-slate-400">{esc(t['one_liner'])}</p>
<div class="mt-6">{links}</div>
<table class="w-full text-sm mt-8">{tr}</table>{evp}</main>"""
    return page(f"{t['name']} — pricing, self-hosting & alternatives | {SITE}",
        f"{t['name']}: {t['one_liner'][:140]}", body, f"tools/{slug(t['name'])}.html", root="../")

def vs_row(label, a, b):
    return f'<tr class="border-b border-slate-800"><td class="py-2 pr-4 text-slate-400 whitespace-nowrap align-top">{esc(label)}</td><td class="py-2 pr-4 align-top">{esc(a)}</td><td class="py-2 align-top">{esc(b)}</td></tr>'

def compare_page(a, b):
    def f(t,k,d="—"): return t.get(k) or d
    yn = lambda v: "Yes" if v else "No"
    rows = "".join([
        vs_row("One-liner", a["one_liner"], b["one_liner"]),
        vs_row("Category", CATS[a["category"]][0], CATS[b["category"]][0]),
        vs_row("Open source", yn(a.get("open_source")), yn(b.get("open_source"))),
        vs_row("Self-hostable", yn(a.get("self_hostable")), yn(b.get("self_hostable"))),
        vs_row("Pricing model", f(a,"pricing_model"), f(b,"pricing_model")),
        vs_row("Pricing notes", f(a,"pricing_note"), f(b,"pricing_note")),
        vs_row("Frameworks", ", ".join(a.get("frameworks") or []), ", ".join(b.get("frameworks") or [])),
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
    body = f"""<main class="max-w-3xl mx-auto px-6 py-12">
<h1 class="text-3xl font-bold text-white">{esc(a['name'])} vs {esc(b['name'])}</h1>
<p class="mt-3 text-slate-400">Side-by-side comparison from the {SITE}: licensing, self-hosting, pricing model and integrations — no vendor copy, primary sources linked.</p>
<table class="w-full text-sm mt-8"><thead><tr class="text-left text-slate-300 border-b border-slate-700">
<th class="py-2 pr-4"></th><th class="py-2 pr-4"><a class="text-emerald-400" href="../tools/{sa}.html">{esc(a['name'])}</a></th><th class="py-2"><a class="text-emerald-400" href="../tools/{sb}.html">{esc(b['name'])}</a></th></tr></thead>
<tbody>{rows}</tbody></table>
<h2 class="text-xl font-semibold text-white mt-10">How to choose</h2>
<ul class="list-disc list-inside text-slate-400 mt-3 space-y-1">{picks}</ul>
<p class="text-xs text-slate-600 mt-8">Sources: <a class="underline" rel="nofollow" href="{esc(a.get('evidence_url') or a['url'])}">{esc(a['name'])}</a> · <a class="underline" rel="nofollow" href="{esc(b.get('evidence_url') or b['url'])}">{esc(b['name'])}</a></p>
</main>"""
    return page(f"{a['name']} vs {b['name']} (2026) — pricing, self-hosting, integrations | {SITE}",
        f"Neutral {a['name']} vs {b['name']} comparison: licensing, self-hosting, pricing and framework integrations, with primary sources.",
        body, f"compare/{sa}-vs-{sb}.html", root="../")

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

    for ck,(cn,cd) in CATS.items():
        items = "".join(card(t, root="../") for t in by.get(ck, []))
        body = f"""<main class="max-w-5xl mx-auto px-6 py-12">
<h1 class="text-3xl font-bold text-white">{esc(cn)}</h1><p class="mt-2 text-slate-400">{esc(cd)} {len(by.get(ck,[]))} tools tracked.</p>
<div class="grid md:grid-cols-2 gap-4 mt-8">{items}</div></main>"""
        paths.append(page(f"{cn} tools (2026) — {len(by.get(ck,[]))} compared | {SITE}", cd, body, f"categories/{ck}.html", root="../"))

    cat_chips = '<button data-f="all" class="fbtn bg-emerald-500 text-slate-950 px-3 py-1.5 rounded-lg text-sm font-semibold">All</button>' + "".join(
        f'<button data-f="{k}" class="fbtn border border-slate-700 px-3 py-1.5 rounded-lg text-sm hover:border-slate-500">{esc(v[0])} ({len(by.get(k,[]))})</button>' for k,v in CATS.items())
    cards = "".join(card(t) for t in tools)
    body = f"""<header class="max-w-5xl mx-auto px-6 pt-16 pb-10">
<h1 class="text-4xl md:text-5xl font-bold text-white leading-tight">The neutral index of<br><span class="text-emerald-400">AI agent observability</span> tooling</h1>
<p class="mt-5 text-lg text-slate-400 max-w-2xl">{esc(TAG)} {len(tools)} tools tracked across tracing, evals, guardrails, prompt management, cost and debugging — with licensing, self-hosting and pricing-model facts checked against primary sources. Built by an engineer who runs agent fleets in production, not by a vendor marketing team.</p>
<div class="mt-4 text-sm text-slate-500">Maintained by <span class="text-slate-300">Panshi</span> · updated June 2026</div></header>
<section id="compare" class="max-w-5xl mx-auto px-6 pb-4"><h2 class="text-xl font-semibold text-white mb-4">Popular comparisons</h2>
<div class="grid sm:grid-cols-2 md:grid-cols-3 gap-3">{''.join(cmp_links)}</div></section>
<section id="tools" class="max-w-5xl mx-auto px-6 py-10">
<h2 class="text-xl font-semibold text-white mb-4">All tools</h2>
<div class="flex flex-wrap gap-2 mb-6">{cat_chips}</div>
<div id="grid" class="grid md:grid-cols-2 gap-4">{cards}</div></section>
<script>
document.querySelectorAll('.fbtn').forEach(b=>b.onclick=()=>{{
 document.querySelectorAll('.fbtn').forEach(x=>x.className=x.className.replace('bg-emerald-500 text-slate-950 font-semibold','').trim()+' border border-slate-700');
 b.className=b.className.replace('border border-slate-700','').trim()+' bg-emerald-500 text-slate-950 font-semibold';
 const f=b.dataset.f;document.querySelectorAll('#grid [data-cat]').forEach(c=>c.style.display=(f==='all'||c.dataset.cat===f)?'':'none');}});
</script>"""
    paths.append(page(f"{SITE} (2026) — {len(tools)} LLM observability, evals & guardrails tools compared", TAG, body, "index.html"))

    body = f"""<main class="max-w-3xl mx-auto px-6 py-12">
<h1 class="text-3xl font-bold text-white">Get your tool featured</h1>
<p class="mt-4 text-slate-400">The index is read by engineers choosing their observability, evals and guardrails stack — transactional-intent traffic, not casual browsing.</p>
<div class="grid md:grid-cols-2 gap-6 mt-8">
<div class="bg-slate-900 rounded-2xl p-6 border border-emerald-700">
<h2 class="font-semibold text-white">Featured listing</h2>
<ul class="text-sm text-slate-400 mt-3 space-y-1 list-disc list-inside"><li>Pinned placement in your category + homepage</li><li>“Featured” badge and expanded card</li><li>Launch pricing, first 10 vendors</li></ul>
<p class="mt-4 text-emerald-400 font-mono">$99 / year (launch price)</p></div>
<div class="bg-slate-900 rounded-2xl p-6 border border-slate-800">
<h2 class="font-semibold text-white">Category sponsor</h2>
<ul class="text-sm text-slate-400 mt-3 space-y-1 list-disc list-inside"><li>Exclusive banner on one category page</li><li>Included in comparison-page footers of that category</li><li>One slot per category</li></ul>
<p class="mt-4 text-emerald-400 font-mono">$490 / year</p></div></div>
<p class="mt-8 text-slate-400">Listings themselves are free and editorially controlled — sponsorship never changes facts or rankings.</p>
<a href="mailto:sysetc@gmail.com?subject=Featured%20listing%20—%20Agent%20Observability%20Index" class="inline-block mt-6 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold px-6 py-3 rounded-lg">Email to get featured</a>
</main>"""
    paths.append(page(f"Advertise — featured listings & category sponsorship | {SITE}",
        "Reach engineers choosing their LLM observability and evals stack. Featured listings from $99/year.", body, "advertise.html"))

    sm = "".join(f"<url><loc>{BASE}/{p}</loc></url>" for p in sorted(set(paths)))
    open(os.path.join(OUT,"sitemap.xml"),"w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    print(f"built {len(paths)} pages + sitemap ({len(tools)} tools)")

if __name__ == "__main__":
    main()
