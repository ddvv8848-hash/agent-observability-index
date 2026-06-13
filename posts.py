# Blog posts for tools.panshi.io. Plain data; build.py renders them.
# Each post: slug, title, description, date (ISO), tags, body (HTML), faq [(q,a)].

POSTS = [
{
 "slug": "geo-case-study-ai-tools-directory",
 "title": "How we made a 116-tool directory citable by AI answer engines",
 "description": "A concrete GEO (Generative Engine Optimization) case study: the exact five changes we made to tools.panshi.io so ChatGPT, Perplexity and Google AI Overviews can cite it — with the research behind each.",
 "date": "2026-06-13",
 "tags": ["GEO", "case study", "AI search"],
 "body": """
<div class="bg-slate-900 border-l-4 border-emerald-500 rounded-r-lg px-5 py-4 mb-8">
<p class="text-sm font-semibold text-emerald-400">TL;DR</p>
<p class="text-slate-300 mt-1">We applied five evidence-backed GEO techniques to this directory: front-loaded verdicts, FAQ schema on 130 pages, structured comparison data, objective GitHub-derived maturity scores, and a published methodology. None of it is keyword tricks — it is making the facts an answer engine can lift directly. Here is exactly what we changed, and the research behind each.</p>
</div>

<p class="text-slate-400">Traditional SEO optimizes to rank as a blue link a human clicks. <strong class="text-slate-200">GEO (Generative Engine Optimization)</strong> optimizes so an AI answer engine — ChatGPT, Perplexity, Google AI Overviews, Claude — quotes your content inside its generated answer. Often there is no click: the citation <em>is</em> the win. The mechanics differ enough to be worth doing deliberately, and most of the winning moves are simply good, well-structured, well-sourced content.</p>

<p class="text-slate-400 mt-4">We rebuilt <a class="text-emerald-400" href="/index.html">this directory</a> with GEO in mind. Five concrete changes:</p>

<h2 class="text-xl font-semibold text-white mt-10">1. Front-load the verdict</h2>
<p class="text-slate-400 mt-2">The Princeton <em>GEO</em> paper (KDD 2024) found that adding clear statements, statistics and citations measurably lifts how often generative engines surface a page; separate citation studies find roughly 44% of LLM citations are pulled from the first 30% of a page. So every comparison page now opens with a one-sentence "Quick verdict" generated from verified data — the exact answer an engine can quote — before the detail table.</p>

<h2 class="text-xl font-semibold text-white mt-10">2. FAQ blocks with FAQPage schema</h2>
<p class="text-slate-400 mt-2">Answer engines lean heavily on Q&amp;A-shaped content. Every tool and comparison page now carries a short FAQ ("Is X open source?", "Can I self-host X?", "Is X OpenTelemetry-native?") rendered both for humans and as <code>FAQPage</code> JSON-LD — 130 pages of it. Every answer is generated from primary-source-verified fields, never invented.</p>

<h2 class="text-xl font-semibold text-white mt-10">3. Structured, comparable facts — not marketing copy</h2>
<p class="text-slate-400 mt-2">For all 116 tools we track open-source status, self-hostability, pricing model, framework integrations and licensing — each checked against the tool's own primary source. Tables and "best/vs" comparisons are cited by AI engines far more than prose, because the facts are unambiguous and liftable.</p>

<h2 class="text-xl font-semibold text-white mt-10">4. Objective, reproducible scores</h2>
<p class="text-slate-400 mt-2">We added a maturity signal computed only from public GitHub data (log of stars + last-commit recency + license) with the formula published openly. And we flagged which tools are genuinely OpenTelemetry-native — 29 of the 37 tracing/observability tools speak OTLP natively (no proprietary-SDK lock-in), 8 do not. That single fact changes a buyer's migration cost more than any feature list, and no vendor listicle will tell you.</p>

<h2 class="text-xl font-semibold text-white mt-10">5. A public methodology</h2>
<p class="text-slate-400 mt-2">Trust is the whole product for a neutral directory, so <a class="text-emerald-400" href="/methodology.html">the methodology</a> spells out exactly how every field and score is produced. Engines (and humans) reward auditable sources.</p>

<h2 class="text-xl font-semibold text-white mt-10">The honest part</h2>
<p class="text-slate-400 mt-2">GEO is real but over-hyped at the edges. The most credible independent benchmark (Conductor, 1,215 enterprise domains) puts AI-referral traffic at ~1% of total today — small, but high-intent (Ahrefs saw AI traffic convert to signups far above its share). And skip the fads: <code>llms.txt</code> is not consumed by search engines (Google compared it to the dead keywords meta tag), and keyword stuffing tests negative. GEO that lasts is just authority plus well-structured, well-sourced, comparison-shaped content.</p>

<div class="bg-slate-900 rounded-xl p-6 border border-slate-800 mt-10">
<p class="text-slate-200 font-semibold">We do this as a service.</p>
<p class="text-slate-400 mt-2">We applied this to our own directory first — it is the testbed and the reference case. If you want your content surfaced by AI answer engines with <em>measured</em> citation tracking (not vague "AI visibility"), email <a class="text-emerald-400" href="mailto:hi@panshi.io">hi@panshi.io</a>.</p>
</div>
""",
 "faq": [
   ("What is GEO (Generative Engine Optimization)?",
    "GEO is optimizing content so AI answer engines like ChatGPT, Perplexity and Google AI Overviews cite or surface it inside their generated answers, rather than ranking it as a link a human clicks."),
   ("Does llms.txt help with GEO?",
    "No. Major search/answer engines do not consume llms.txt; Google has compared it to the long-dead keywords meta tag. It is only useful for feeding coding assistants documentation."),
   ("How much traffic does AI search actually send?",
    "Today it is small — around 1% of total referral traffic per the most credible independent benchmark (Conductor, 1,215 domains) — but it converts at a much higher rate than its share, so it is high-intent rather than high-volume."),
   ("What is the single highest-ROI GEO action?",
    "Publish and keep fresh opinionated, benchmarked best/vs comparison pages with hard statistics, named sources and tables, with the conclusion front-loaded in the first paragraph."),
 ],
},
]
