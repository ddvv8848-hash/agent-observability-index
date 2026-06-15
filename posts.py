# Blog posts for tools.panshi.io. Plain data; build.py renders them.
# Each post: slug, title, description, date (ISO), tags, body (HTML), faq [(q,a)].

POSTS = [
{
 "slug": "geo-case-study-ai-tools-directory",
 "title": "How we made a 116-tool directory citable by AI answer engines",
 "description": "A concrete GEO (Generative Engine Optimization) case study: the exact five changes we made to panshi.io/tools so ChatGPT, Perplexity and Google AI Overviews can cite it — with the research behind each.",
 "date": "2026-06-13",
 "tags": ["GEO", "case study", "AI search"],
 "body": """
<div class="rounded-r-lg px-5 py-4 mb-8" style="background:#0F1011;border:1px solid rgba(255,255,255,0.08);border-left:3px solid #5E6AD2;">
<p class="text-sm font-semibold" style="color:#aab2ee;">TL;DR</p>
<p class="mt-1" style="color:#C8CCD2;">We applied five evidence-backed GEO techniques to this directory: front-loaded verdicts, FAQ schema on 130 pages, structured comparison data, objective GitHub-derived maturity scores, and a published methodology. None of it is keyword tricks — it is making the facts an answer engine can lift directly. Here is exactly what we changed, and the research behind each.</p>
</div>

<p class="text-slate-600">Traditional SEO optimizes to rank as a blue link a human clicks. <strong class="text-slate-900">GEO (Generative Engine Optimization)</strong> optimizes so an AI answer engine — ChatGPT, Perplexity, Google AI Overviews, Claude — quotes your content inside its generated answer. Often there is no click: the citation <em>is</em> the win. The mechanics differ enough to be worth doing deliberately, and most of the winning moves are simply good, well-structured, well-sourced content.</p>

<p class="text-slate-600 mt-4">We rebuilt <a class="text-blue-600 hover:text-blue-700" href="/index.html">this directory</a> with GEO in mind. Five concrete changes:</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">1. Front-load the verdict</h2>
<p class="text-slate-600 mt-2">The Princeton <em>GEO</em> paper (KDD 2024) found that adding clear statements, statistics and citations measurably lifts how often generative engines surface a page; separate citation studies find roughly 44% of LLM citations are pulled from the first 30% of a page. So every comparison page now opens with a one-sentence "Quick verdict" generated from verified data — the exact answer an engine can quote — before the detail table.</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">2. FAQ blocks with FAQPage schema</h2>
<p class="text-slate-600 mt-2">Answer engines lean heavily on Q&amp;A-shaped content. Every tool and comparison page now carries a short FAQ ("Is X open source?", "Can I self-host X?", "Is X OpenTelemetry-native?") rendered both for humans and as <code>FAQPage</code> JSON-LD — 130 pages of it. Every answer is generated from primary-source-verified fields, never invented.</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">3. Structured, comparable facts — not marketing copy</h2>
<p class="text-slate-600 mt-2">For all 116 tools we track open-source status, self-hostability, pricing model, framework integrations and licensing — each checked against the tool's own primary source. Tables and "best/vs" comparisons are cited by AI engines far more than prose, because the facts are unambiguous and liftable.</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">4. Objective, reproducible scores</h2>
<p class="text-slate-600 mt-2">We added a maturity signal computed only from public GitHub data (log of stars + last-commit recency + license) with the formula published openly. And we flagged which tools are genuinely OpenTelemetry-native — 29 of the 37 tracing/observability tools speak OTLP natively (no proprietary-SDK lock-in), 8 do not. That single fact changes a buyer's migration cost more than any feature list, and no vendor listicle will tell you.</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">5. A public methodology</h2>
<p class="text-slate-600 mt-2">Trust is the whole product for a neutral directory, so <a class="text-blue-600 hover:text-blue-700" href="/methodology.html">the methodology</a> spells out exactly how every field and score is produced. Engines (and humans) reward auditable sources.</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">The honest part</h2>
<p class="text-slate-600 mt-2">GEO is real but over-hyped at the edges. The most credible independent benchmark (Conductor, 1,215 enterprise domains) puts AI-referral traffic at ~1% of total today — small, but high-intent (Ahrefs saw AI traffic convert to signups far above its share). And skip the fads: <code>llms.txt</code> is not consumed by search engines (Google compared it to the dead keywords meta tag), and keyword stuffing tests negative. GEO that lasts is just authority plus well-structured, well-sourced, comparison-shaped content.</p>

<div class="rounded-xl p-6 mt-10" style="background:#0F1011;border:1px solid rgba(255,255,255,0.08);">
<p class="font-semibold" style="color:#F7F8F8;">We do this as a service.</p>
<p class="text-slate-600 mt-2">We applied this to our own directory first — it is the testbed and the reference case. If you want your content surfaced by AI answer engines with <em>measured</em> citation tracking (not vague "AI visibility"), email <a class="text-blue-600 hover:text-blue-700" href="mailto:hi@panshi.io">hi@panshi.io</a>.</p>
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
 "title_zh": "我们如何让一个 116 个工具的目录被 AI 答案引擎引用",
 "description_zh": "一个具体的 GEO(生成式引擎优化)案例:我们对 panshi.io/tools 做的五项改动,让 ChatGPT、Perplexity 和 Google AI Overviews 能够引用它 —— 并附上每项背后的研究依据。",
 "body_zh": """
<div class="rounded-r-lg px-5 py-4 mb-8" style="background:#0F1011;border:1px solid rgba(255,255,255,0.08);border-left:3px solid #5E6AD2;">
<p class="text-sm font-semibold" style="color:#aab2ee;">一句话总结</p>
<p class="mt-1" style="color:#C8CCD2;">我们对这个目录应用了五项有证据支撑的 GEO 手法:把结论前置、130 个页面的 FAQ 结构化数据、结构化对比数据、基于 GitHub 的客观成熟度评分,以及公开的方法论。这些都不是关键词花招 —— 而是把事实做成答案引擎可以直接引用的形式。下面是我们具体改了什么,以及每一项背后的研究依据。</p>
</div>

<p class="text-slate-600">传统 SEO 优化的目标,是在搜索结果里排到一个供人点击的蓝色链接。<strong class="text-slate-900">GEO(生成式引擎优化)</strong>优化的目标,是让 AI 答案引擎 —— ChatGPT、Perplexity、Google AI Overviews、Claude —— 在它生成的答案里引用你的内容。很多时候根本没有点击:被引用本身就是胜利。两者机制的差异大到值得专门去做,而大部分能赢的动作,其实就是把内容做得扎实、结构清晰、来源可靠。</p>

<p class="text-slate-600 mt-4">我们带着 GEO 思路重建了<a class="text-blue-600 hover:text-blue-700" href="/index.html">这个目录</a>。五项具体改动:</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">1. 把结论前置</h2>
<p class="text-slate-600 mt-2">普林斯顿的 <em>GEO</em> 论文(KDD 2024)发现,加入明确的论断、统计数字和引用,能显著提升生成式引擎收录页面的频率;另有引用研究发现,约 44% 的 LLM 引用取自页面前 30% 的内容。所以现在每个对比页都以一句基于已核实数据生成的"快速结论"开头 —— 也就是引擎可以直接引用的那句答案 —— 再展开细节表格。</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">2. 带 FAQPage 结构化数据的 FAQ 区块</h2>
<p class="text-slate-600 mt-2">答案引擎高度依赖问答形态的内容。现在每个工具页和对比页都带一段简短 FAQ("X 是开源的吗?""X 能自托管吗?""X 是 OpenTelemetry 原生的吗?"),既渲染给人看,也以 <code>FAQPage</code> JSON-LD 形式输出 —— 共 130 个页面。每个答案都由一手来源核实过的字段生成,绝不杜撰。</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">3. 结构化、可对比的事实 —— 而非营销文案</h2>
<p class="text-slate-600 mt-2">对全部 116 个工具,我们追踪其开源状态、可自托管性、定价模式、框架集成与授权协议 —— 每一项都对照该工具自己的一手来源核实。表格和"最佳/对比"类内容被 AI 引擎引用的频率远高于散文,因为事实清晰无歧义、可被直接摘取。</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">4. 客观、可复现的评分</h2>
<p class="text-slate-600 mt-2">我们加了一个仅由公开 GitHub 数据计算的成熟度信号(star 数的对数 + 最近提交时间 + 授权协议),公式完全公开。我们还标注了哪些工具是真正 OpenTelemetry 原生的 —— 37 个追踪/可观测性工具里有 29 个原生支持 OTLP(无私有 SDK 锁定),8 个不支持。这一个事实对买家迁移成本的影响,胜过任何功能清单,而厂商榜单不会告诉你。</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">5. 公开的方法论</h2>
<p class="text-slate-600 mt-2">对一个中立目录来说,信任就是产品的全部,所以<a class="text-blue-600 hover:text-blue-700" href="/methodology.html">方法论页面</a>把每个字段和评分的产生方式都讲清楚。引擎(和人)都奖励可审计的来源。</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">实话部分</h2>
<p class="text-slate-600 mt-2">GEO 是真实存在的,但在边缘地带被过度炒作。最可信的独立基准(Conductor,1215 个企业域名)显示,如今 AI 引荐流量约占总量的 1% —— 体量小,但意图强(Ahrefs 观察到 AI 流量转化为注册的比例远高于其流量占比)。也别追风口:<code>llms.txt</code> 并不被搜索引擎消费(Google 把它比作早已作废的 keywords meta 标签),关键词堆砌经测试是负面效果。能长久见效的 GEO,无非是权威性,加上结构清晰、来源可靠、对比形态的内容。</p>

<div class="rounded-xl p-6 mt-10" style="background:#0F1011;border:1px solid rgba(255,255,255,0.08);">
<p class="font-semibold" style="color:#F7F8F8;">我们也把这件事做成一项服务。</p>
<p class="text-slate-600 mt-2">我们先把它用在自己的目录上 —— 它既是试验场,也是参考案例。如果你希望自己的内容被 AI 答案引擎引用,并带<em>可测量</em>的引用追踪(而不是含糊的"AI 可见度"),请邮件联系 <a class="text-blue-600 hover:text-blue-700" href="mailto:hi@panshi.io">hi@panshi.io</a>。</p>
</div>
""",
 "faq_zh": [
   ("什么是 GEO(生成式引擎优化)?",
    "GEO 是指优化内容,使 ChatGPT、Perplexity、Google AI Overviews 等 AI 答案引擎在其生成的答案中引用或呈现你的内容,而不是把它排成一个供人点击的链接。"),
   ("llms.txt 对 GEO 有帮助吗?",
    "没有。主流搜索/答案引擎并不消费 llms.txt;Google 把它比作早已作废的 keywords meta 标签。它只对给编程助手喂文档有用。"),
   ("AI 搜索实际能带来多少流量?",
    "目前还很小 —— 按最可信的独立基准(Conductor,1215 个域名)约占引荐流量的 1% —— 但其转化率远高于流量占比,所以是高意图而非高流量。"),
   ("投入产出比最高的单项 GEO 动作是什么?",
    "发布并持续更新有观点、有基准数据的最佳/对比页面,配上硬统计数字、具名来源和表格,并把结论前置到第一段。"),
 ],
},
{
 "slug": "opentelemetry-native-llm-observability-lock-in",
 "title": "OpenTelemetry-native or not: the lock-in question in LLM observability",
 "description": "Of the 37 LLM tracing/observability tools we track, 29 are OpenTelemetry-native and 8 are not. Here is why that single fact decides your migration cost — and how to tell the difference.",
 "date": "2026-06-13",
 "tags": ["OpenTelemetry", "observability", "lock-in"],
 "body": """
<div class="rounded-r-lg px-5 py-4 mb-8" style="background:#0F1011;border:1px solid rgba(255,255,255,0.08);border-left:3px solid #5E6AD2;">
<p class="text-sm font-semibold" style="color:#aab2ee;">Quick answer</p>
<p class="mt-1" style="color:#C8CCD2;">If a tool is OpenTelemetry-native — it ingests or emits OTLP and follows the OTel GenAI semantic conventions — switching off it later costs you almost nothing, because your instrumentation stays the same and you just repoint the endpoint. If it relies on a proprietary SDK or trace format, every line of instrumentation is a switching cost. Of the 37 tracing/observability tools we track, <strong class="text-slate-900">29 are OpenTelemetry-native and 8 are not.</strong></p>
</div>

<p class="text-slate-600">"Does it integrate with X?" is the wrong first question when you pick an LLM observability tool. The question that actually decides your future migration bill is: <strong class="text-slate-900">is it OpenTelemetry-native, or does it lock you into a proprietary SDK?</strong></p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">Why it matters</h2>
<p class="text-slate-600 mt-2">OpenTelemetry (OTel) is the vendor-neutral standard for traces and metrics. When an observability tool speaks OTLP natively, your app emits standard OTel spans and you simply point them at that tool. Outgrow it, or want to send the same data to two backends? You change an endpoint, not your code. When a tool instead ships its own SDK and trace format, your instrumentation <em>is</em> the lock-in: leaving means re-instrumenting everything.</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">How to tell the difference</h2>
<p class="text-slate-600 mt-2">We checked each tool's own docs and repository, not its marketing. A tool counts as OTel-native only if OTLP / the OpenTelemetry SDK / GenAI semantic conventions are a first-class path — not a secondary "integration." Native examples include Arize Phoenix (built on OTel), SigNoz (OTel-first since day one), Pydantic Logfire (a thin wrapper over OTel), OpenLIT and Traceloop/OpenLLMetry (whose conventions were upstreamed into OTel itself), plus managed platforms that expose a native OTLP endpoint (Langfuse, Datadog, New Relic, Grafana, Dynatrace). Proprietary-first examples include tools whose primary path is their own decorator SDK or a logging proxy rather than OTLP.</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">The nuance</h2>
<p class="text-slate-600 mt-2">OTel-native is not automatically "better" — a proprietary SDK can offer richer, opinionated capture. And in our own instrumentation-overhead benchmark, the per-span cost of all tested SDKs was negligible against real LLM latency (well under 0.05% of a typical call), though it varied about 7x between the lightest OTel path and a richer proprietary one. So treat OTel-native as a <em>strategic</em> property — it caps your downside and keeps you portable — rather than a performance verdict.</p>

<p class="text-slate-600 mt-4">Every tool page in <a class="text-blue-600 hover:text-blue-700" href="/index.html">our index</a> flags OpenTelemetry-native status, and our <a class="text-blue-600 hover:text-blue-700" href="/methodology.html">methodology</a> explains how we verified it.</p>
""",
 "faq": [
   ("What does OpenTelemetry-native mean for an LLM observability tool?",
    "It means the tool ingests or emits OpenTelemetry (OTLP) and follows the OTel GenAI semantic conventions as a first-class path, so you instrument with standard OpenTelemetry rather than a proprietary SDK — and can repoint or dual-export without rewriting code."),
   ("How many LLM observability tools are OpenTelemetry-native?",
    "Of the 37 tracing/observability tools tracked on this index, 29 are OpenTelemetry-native and 8 rely on a proprietary SDK or trace format."),
   ("Is OpenTelemetry-native always the better choice?",
    "Not always. A proprietary SDK can capture richer, more opinionated data. OTel-native is best understood as a strategic property that minimizes lock-in and keeps you portable, not as a performance ranking."),
   ("Does instrumentation overhead differ much between tools?",
    "In our micro-benchmark the per-span overhead of all tested SDKs was negligible versus real LLM latency (under 0.05% of a typical 500ms call), though it varied roughly 7x between the lightest OpenTelemetry path and a richer proprietary one."),
 ],
 "title_zh": "OpenTelemetry 原生与否:LLM 可观测性里的锁定问题",
 "description_zh": "在我们追踪的 37 个 LLM 追踪/可观测性工具中,29 个是 OpenTelemetry 原生的,8 个不是。本文讲清这一个事实为何决定你的迁移成本 —— 以及如何分辨。",
 "body_zh": """
<div class="rounded-r-lg px-5 py-4 mb-8" style="background:#0F1011;border:1px solid rgba(255,255,255,0.08);border-left:3px solid #5E6AD2;">
<p class="text-sm font-semibold" style="color:#aab2ee;">快速答案</p>
<p class="mt-1" style="color:#C8CCD2;">如果一个工具是 OpenTelemetry 原生的 —— 它摄取或发出 OTLP,并遵循 OTel GenAI 语义约定 —— 那么以后切换离开它几乎不花成本,因为你的插桩代码不变,只需把端点改个指向。如果它依赖私有 SDK 或私有追踪格式,那么你写的每一行插桩都是切换成本。在我们追踪的 37 个追踪/可观测性工具里,<strong class="text-slate-900">29 个是 OpenTelemetry 原生的,8 个不是。</strong></p>
</div>

<p class="text-slate-600">挑选 LLM 可观测性工具时,"它和 X 集成吗?"是个错误的首要问题。真正决定你未来迁移账单的问题是:<strong class="text-slate-900">它是 OpenTelemetry 原生的,还是把你锁进一个私有 SDK?</strong></p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">为什么重要</h2>
<p class="text-slate-600 mt-2">OpenTelemetry(OTel)是追踪与指标的厂商中立标准。当一个可观测性工具原生支持 OTLP 时,你的应用发出标准的 OTel span,你只需把它们指向该工具即可。用不下去了,或者想把同一份数据同时送往两个后端?改个端点就行,不用改代码。而当一个工具改用自己的 SDK 和追踪格式时,你的插桩本身<em>就是</em>锁定:离开就意味着把一切重新插桩。</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">如何分辨</h2>
<p class="text-slate-600 mt-2">我们查的是每个工具自己的文档和代码仓库,而不是它的营销话术。只有当 OTLP / OpenTelemetry SDK / GenAI 语义约定是一等公民路径(而非次要的"集成")时,我们才算它 OTel 原生。原生的例子包括 Arize Phoenix(构建于 OTel 之上)、SigNoz(从第一天起就是 OTel 优先)、Pydantic Logfire(对 OTel 的薄封装)、OpenLIT,以及 Traceloop/OpenLLMetry(其约定已被上游合入 OTel 本身),还有提供原生 OTLP 端点的托管平台(Langfuse、Datadog、New Relic、Grafana、Dynatrace)。私有优先的例子,则是主路径为自家装饰器 SDK 或日志代理、而非 OTLP 的那些工具。</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">其中的微妙之处</h2>
<p class="text-slate-600 mt-2">OTel 原生并不自动等于"更好" —— 私有 SDK 可能提供更丰富、更有取舍的数据采集。而且在我们自己的插桩开销基准里,所有被测 SDK 的单 span 成本相对真实 LLM 延迟都可忽略不计(远低于一次典型调用的 0.05%),尽管最轻的 OTel 路径与较重的私有路径之间相差约 7 倍。所以应把 OTel 原生当作一个<em>战略</em>属性 —— 它封住了你的下行风险、保持可移植 —— 而非性能裁决。</p>

<p class="text-slate-600 mt-4">我们<a class="text-blue-600 hover:text-blue-700" href="/index.html">索引</a>里的每个工具页都标注了 OpenTelemetry 原生状态,我们的<a class="text-blue-600 hover:text-blue-700" href="/methodology.html">方法论</a>说明了我们如何核实它。</p>
""",
 "faq_zh": [
   ("对一个 LLM 可观测性工具来说,OpenTelemetry 原生意味着什么?",
    "意味着该工具把摄取或发出 OpenTelemetry(OTLP)、遵循 OTel GenAI 语义约定作为一等公民路径,因此你用标准 OpenTelemetry 而非私有 SDK 来插桩 —— 并且可以重新指向端点或双路导出而不必改写代码。"),
   ("有多少 LLM 可观测性工具是 OpenTelemetry 原生的?",
    "在本索引追踪的 37 个追踪/可观测性工具中,29 个是 OpenTelemetry 原生的,8 个依赖私有 SDK 或私有追踪格式。"),
   ("OpenTelemetry 原生总是更好的选择吗?",
    "不一定。私有 SDK 可能采集到更丰富、更有取舍的数据。OTel 原生最好理解为一个把锁定降到最低、保持可移植的战略属性,而非性能排名。"),
   ("不同工具的插桩开销差别大吗?",
    "在我们的微基准里,所有被测 SDK 的单 span 开销相对真实 LLM 延迟都可忽略不计(低于一次典型 500ms 调用的 0.05%),尽管最轻的 OpenTelemetry 路径与较重的私有路径之间相差约 7 倍。"),
 ],
},
{
 "slug": "self-hosting-llm-observability-what-we-measured",
 "title": "Self-hosting LLM observability: what we actually measured",
 "description": "We self-hosted open-source LLM observability tools and measured the two things that matter: how much instrumentation overhead they add, and how heavy they are to run. Real numbers, honest caveats.",
 "date": "2026-06-13",
 "tags": ["self-hosting", "benchmark", "observability"],
 "body": """
<div class="rounded-r-lg px-5 py-4 mb-8" style="background:#0F1011;border:1px solid rgba(255,255,255,0.08);border-left:3px solid #5E6AD2;">
<p class="text-sm font-semibold" style="color:#aab2ee;">What we found</p>
<p class="mt-1" style="color:#C8CCD2;">Instrumentation overhead is a non-issue: every SDK we tested added under 0.05% to a typical LLM call (though there's a ~7x spread between them). The real difference is operational weight. Arize Phoenix came up as a single container (1.35 GB image, ~400&nbsp;MB idle RAM, OTLP ingest verified end-to-end); Langfuse is a full platform that booted cleanly but runs as a 6-service stack costing ~2.1&nbsp;GB idle RAM. Match the footprint to the need. <span style="color:#62666D;">(tested @ 2026-06, WSL2 + Docker)</span></p>
</div>

<p class="text-slate-600">Most "best self-hosted observability" lists never actually run the tools. We did. Two questions matter when you self-host: <strong class="text-slate-900">how much does the SDK slow my app down</strong>, and <strong class="text-slate-900">how much does the backend cost me to operate</strong>. Here is what we measured.</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">1. Instrumentation overhead (client-side)</h2>
<p class="text-slate-600 mt-2">We timed 50,000 spans per SDK with in-memory exporters (no network), against an uninstrumented baseline. Per-span overhead, and what it is as a fraction of a typical 500&nbsp;ms LLM call:</p>
<table class="w-full text-sm mt-4">
<thead><tr class="text-left" style="color:#F7F8F8;border-bottom:1px solid rgba(255,255,255,0.14);"><th class="py-2 pr-4">SDK</th><th class="py-2 pr-4">overhead / span</th><th class="py-2">% of a 500ms call</th></tr></thead>
<tbody>
<tr style="border-bottom:1px solid rgba(255,255,255,0.08);"><td class="py-2 pr-4">OpenTelemetry (raw)</td><td class="py-2 pr-4">~34 µs</td><td class="py-2">0.007%</td></tr>
<tr style="border-bottom:1px solid rgba(255,255,255,0.08);"><td class="py-2 pr-4">Traceloop / OpenLLMetry</td><td class="py-2 pr-4">~37 µs</td><td class="py-2">0.007%</td></tr>
<tr style="border-bottom:1px solid rgba(255,255,255,0.08);"><td class="py-2 pr-4">Langfuse SDK</td><td class="py-2 pr-4">~243 µs</td><td class="py-2">0.049%</td></tr>
</tbody></table>
<p class="text-slate-600 mt-3">Takeaway: stop worrying about instrumentation overhead for LLM workloads — the model call dominates by 2,000x or more. The ~7x spread (a richer observation model costs more per span) only matters on very high-span, non-LLM hot paths.</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">2. Operational weight (self-host footprint)</h2>
<p class="text-slate-600 mt-2">We booted each backend from its official Docker setup and measured the footprint: how many containers it runs, the on-disk image size, idle RAM once healthy, time to a ready endpoint, and whether it ingests OpenTelemetry (OTLP) out of the box. <span class="text-sm" style="color:#62666D;">(tested @ 2026-06, WSL2 + Docker, measured)</span></p>
<table class="w-full text-sm mt-4">
<thead><tr class="text-left" style="color:#F7F8F8;border-bottom:1px solid rgba(255,255,255,0.14);"><th class="py-2 pr-4">Tool</th><th class="py-2 pr-4">Containers</th><th class="py-2 pr-4">Image size</th><th class="py-2 pr-4">Idle RAM</th><th class="py-2 pr-4">Time to ready</th><th class="py-2">OTLP ingest</th></tr></thead>
<tbody>
<tr style="border-bottom:1px solid rgba(255,255,255,0.08);"><td class="py-2 pr-4 font-medium" style="color:#F7F8F8;">Arize Phoenix</td><td class="py-2 pr-4">1</td><td class="py-2 pr-4">1.35 GB</td><td class="py-2 pr-4">~400&nbsp;MB</td><td class="py-2 pr-4">19&nbsp;s</td><td class="py-2">yes (verified end-to-end)</td></tr>
<tr style="border-bottom:1px solid rgba(255,255,255,0.08);"><td class="py-2 pr-4 font-medium" style="color:#F7F8F8;">Langfuse</td><td class="py-2 pr-4">6</td><td class="py-2 pr-4">1.16&nbsp;GB</td><td class="py-2 pr-4">~2.1&nbsp;GB <span style="color:#62666D;">(web container alone ~1.1&nbsp;GB)</span></td><td class="py-2 pr-4">~10&nbsp;s <span style="color:#62666D;">(images cached)</span></td><td class="py-2">n/a (own SDK, not OTLP-native)</td></tr>
<tr style="border-bottom:1px solid rgba(255,255,255,0.08);"><td class="py-2 pr-4 font-medium" style="color:#F7F8F8;">SigNoz</td><td class="py-2 pr-4">multi-service</td><td class="py-2 pr-4">—</td><td class="py-2 pr-4">—</td><td class="py-2 pr-4">not measured</td><td class="py-2">not measured in our env*</td></tr>
</tbody></table>
<p class="text-slate-600 mt-3"><strong class="text-slate-900">Arize Phoenix</strong> is the lightweight end: one drop-in container, ~400&nbsp;MB idle RAM, ready in under 20&nbsp;seconds, and it accepted standard OTLP traces immediately. If you want self-hosted tracing running in five minutes, this is the shape to look for.</p>
<p class="text-slate-600 mt-2"><strong class="text-slate-900">Langfuse</strong> booted cleanly this time — with images cached the stack came up in about 10&nbsp;seconds. But it is a full platform, not a one-container drop-in: a 6-service stack (web, worker, Postgres, ClickHouse, cache, object store) costing ~2.1&nbsp;GB idle RAM, with the web container alone at ~1.1&nbsp;GB. It also ingests via its own SDK rather than OTLP natively. One host-port note worth knowing up front: its bundled MinIO object store defaults to <code class="text-slate-900">:9090</code>, which collides with Prometheus on a lot of dev boxes — remap it before you start. Far more capable for prompt management, evals and retention; just budget for the operational weight.</p>
<p class="text-slate-600 mt-2"><strong class="text-slate-900">SigNoz</strong> we could not measure cleanly in our environment: its first-boot init container blocked downloading a GitHub release asset on our test network, so the stack never reached a healthy state. We are flagging this honestly as <em>not measured in our env</em> — it is an environmental/network issue on our side, not a SigNoz defect — rather than publishing a number we did not actually observe.</p>
<p class="text-sm mt-2" style="color:#62666D;">* SigNoz: init container blocked downloading a GitHub release asset on our test network (environmental, not a SigNoz defect).</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">How to read this</h2>
<p class="text-slate-600 mt-2">Match the footprint to the job. Need lightweight, OpenTelemetry-native tracing you can stand up fast? A single-container tool wins. Need prompt management, evals, datasets and long retention for a team? A full platform earns its operational weight. Don't pay multi-service ops cost for a single-container need, or vice versa.</p>

<p class="text-slate-600 mt-4">Caveats, stated plainly: the overhead test is client-side span cost with in-memory export, not end-to-end backend latency; the self-host numbers are from one test environment (WSL2, Docker, tested @ 2026-06) and are footprint snapshots, not a load test. Langfuse times benefit from cached images; cold pulls take longer. SigNoz is reported as not-measured-in-our-env rather than estimated. We are extending the matrix to more tools and will keep every row labelled "tested" and dated. See <a class="text-blue-600 hover:text-blue-700" href="/methodology.html">our methodology</a>.</p>
""",
 "faq": [
   ("Does LLM observability instrumentation slow down my app?",
    "Negligibly. In our test every SDK added under 0.05% to a typical 500ms LLM call; the model call dominates by thousands of times. Instrumentation overhead should not drive your tool choice for LLM workloads."),
   ("Which self-hosted LLM observability tool is lightest to run?",
    "In our test Arize Phoenix was the lightweight end: a single container, ~1.35GB image and ~400MB idle RAM, accepting OTLP traces immediately. Full platforms like Langfuse are far more capable but ship multi-service stacks that are a larger operational commitment."),
   ("Is Langfuse hard to self-host?",
    "It booted cleanly in our 2026-06 test (about 10 seconds with images cached), but it is a full platform, not a one-container drop-in: a 6-service stack (web, worker, Postgres, ClickHouse, cache, object store) costing ~2.1GB idle RAM, with the web container alone around 1.1GB. It uses its own SDK rather than OTLP natively, and its bundled MinIO defaults to host port :9090 (which collides with Prometheus on many dev boxes). Plenty capable for prompt management, evals and retention — just budget for the operational weight."),
 ],
 "title_zh": "自托管 LLM 可观测性:我们实测了什么",
 "description_zh": "我们自托管了多个开源 LLM 可观测性工具,实测了两件真正重要的事:它们增加多少插桩开销,以及运行起来有多重。真实数字,诚实说明。",
 "body_zh": """
<div class="rounded-r-lg px-5 py-4 mb-8" style="background:#0F1011;border:1px solid rgba(255,255,255,0.08);border-left:3px solid #5E6AD2;">
<p class="text-sm font-semibold" style="color:#aab2ee;">我们的发现</p>
<p class="mt-1" style="color:#C8CCD2;">插桩开销是个伪问题:我们测的每个 SDK 给一次典型 LLM 调用增加的开销都低于 0.05%(尽管彼此相差约 7 倍)。真正的差别在于运维重量。Arize Phoenix 以单个容器起来(1.35 GB 镜像、约 400&nbsp;MB 空闲内存,OTLP 摄取端到端验证通过);Langfuse 是一个完整平台,启动顺利,但作为 6 服务栈运行,空闲内存约 2.1&nbsp;GB。按需求匹配占用。<span style="color:#62666D;">(测试环境 @ 2026-06,WSL2 + Docker)</span></p>
</div>

<p class="text-slate-600">大多数"最佳自托管可观测性"清单从没真正跑过这些工具。我们跑了。自托管时有两个问题最关键:<strong class="text-slate-900">SDK 把我的应用拖慢多少</strong>,以及<strong class="text-slate-900">后端运维起来要花我多少</strong>。下面是我们的实测。</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">1. 插桩开销(客户端)</h2>
<p class="text-slate-600 mt-2">我们对每个 SDK 用内存导出器(无网络)计时 50,000 个 span,并与未插桩的基线对比。单 span 开销,以及它占一次典型 500&nbsp;ms LLM 调用的比例:</p>
<table class="w-full text-sm mt-4">
<thead><tr class="text-left" style="color:#F7F8F8;border-bottom:1px solid rgba(255,255,255,0.14);"><th class="py-2 pr-4">SDK</th><th class="py-2 pr-4">每 span 开销</th><th class="py-2">占 500ms 调用比例</th></tr></thead>
<tbody>
<tr style="border-bottom:1px solid rgba(255,255,255,0.08);"><td class="py-2 pr-4">OpenTelemetry(原始)</td><td class="py-2 pr-4">~34 µs</td><td class="py-2">0.007%</td></tr>
<tr style="border-bottom:1px solid rgba(255,255,255,0.08);"><td class="py-2 pr-4">Traceloop / OpenLLMetry</td><td class="py-2 pr-4">~37 µs</td><td class="py-2">0.007%</td></tr>
<tr style="border-bottom:1px solid rgba(255,255,255,0.08);"><td class="py-2 pr-4">Langfuse SDK</td><td class="py-2 pr-4">~243 µs</td><td class="py-2">0.049%</td></tr>
</tbody></table>
<p class="text-slate-600 mt-3">结论:对 LLM 工作负载别再纠结插桩开销 —— 模型调用本身要主导 2000 倍以上。那约 7 倍的差距(更丰富的观测模型每 span 成本更高)只在 span 量极大的非 LLM 热路径上才有意义。</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">2. 运维重量(自托管占用)</h2>
<p class="text-slate-600 mt-2">我们用每个后端的官方 Docker 配置启动它,并测量其占用:跑多少个容器、磁盘镜像大小、健康后的空闲内存、到就绪端点的时间,以及是否开箱即支持 OpenTelemetry(OTLP)摄取。<span class="text-sm" style="color:#62666D;">(测试环境 @ 2026-06,WSL2 + Docker,实测)</span></p>
<table class="w-full text-sm mt-4">
<thead><tr class="text-left" style="color:#F7F8F8;border-bottom:1px solid rgba(255,255,255,0.14);"><th class="py-2 pr-4">工具</th><th class="py-2 pr-4">容器数</th><th class="py-2 pr-4">镜像大小</th><th class="py-2 pr-4">空闲内存</th><th class="py-2 pr-4">就绪时间</th><th class="py-2">OTLP 摄取</th></tr></thead>
<tbody>
<tr style="border-bottom:1px solid rgba(255,255,255,0.08);"><td class="py-2 pr-4 font-medium" style="color:#F7F8F8;">Arize Phoenix</td><td class="py-2 pr-4">1</td><td class="py-2 pr-4">1.35 GB</td><td class="py-2 pr-4">~400&nbsp;MB</td><td class="py-2 pr-4">19&nbsp;秒</td><td class="py-2">是(端到端验证)</td></tr>
<tr style="border-bottom:1px solid rgba(255,255,255,0.08);"><td class="py-2 pr-4 font-medium" style="color:#F7F8F8;">Langfuse</td><td class="py-2 pr-4">6</td><td class="py-2 pr-4">1.16&nbsp;GB</td><td class="py-2 pr-4">~2.1&nbsp;GB <span style="color:#62666D;">(仅 web 容器约 1.1&nbsp;GB)</span></td><td class="py-2 pr-4">~10&nbsp;秒 <span style="color:#62666D;">(镜像已缓存)</span></td><td class="py-2">不适用(自家 SDK,非 OTLP 原生)</td></tr>
<tr style="border-bottom:1px solid rgba(255,255,255,0.08);"><td class="py-2 pr-4 font-medium" style="color:#F7F8F8;">SigNoz</td><td class="py-2 pr-4">多服务</td><td class="py-2 pr-4">—</td><td class="py-2 pr-4">—</td><td class="py-2 pr-4">未测</td><td class="py-2">本环境未测*</td></tr>
</tbody></table>
<p class="text-slate-600 mt-3"><strong class="text-slate-900">Arize Phoenix</strong> 处在轻量这一端:一个即插即用容器、约 400&nbsp;MB 空闲内存、20&nbsp;秒内就绪,并且立即接受标准 OTLP 追踪。如果你想五分钟内跑起自托管追踪,就该找这种形态。</p>
<p class="text-slate-600 mt-2"><strong class="text-slate-900">Langfuse</strong> 这次启动顺利 —— 在镜像已缓存的情况下整个栈约 10&nbsp;秒起来。但它是一个完整平台,而非单容器即插即用:一个 6 服务栈(web、worker、Postgres、ClickHouse、缓存、对象存储),空闲内存约 2.1&nbsp;GB,仅 web 容器就约 1.1&nbsp;GB。它也是通过自家 SDK 而非原生 OTLP 摄取。有一个值得提前知道的主机端口坑:它自带的 MinIO 对象存储默认用 <code class="text-slate-900">:9090</code>,在很多开发机上会与 Prometheus 冲突 —— 启动前先改掉。它在提示词管理、评测和留存方面强得多;只是要为运维重量做好预算。</p>
<p class="text-slate-600 mt-2"><strong class="text-slate-900">SigNoz</strong> 我们在自己的环境里没能干净地测出来:它首次启动的 init 容器在我们的测试网络上下载一个 GitHub release 资产时被卡住,导致整个栈始终未达健康状态。我们如实把它标为<em>本环境未测</em> —— 这是我们这边的环境/网络问题,不是 SigNoz 的缺陷 —— 而不是发布一个我们并未真正观测到的数字。</p>
<p class="text-sm mt-2" style="color:#62666D;">* SigNoz:init 容器在我们的测试网络上下载 GitHub release 资产时被卡住(环境问题,非 SigNoz 缺陷)。</p>

<h2 class="text-xl font-semibold text-slate-900 mt-10">怎么读这些数据</h2>
<p class="text-slate-600 mt-2">按任务匹配占用。需要能快速起来的轻量、OpenTelemetry 原生追踪?单容器工具胜出。需要给团队用的提示词管理、评测、数据集和长留存?完整平台值它的运维重量。别为单容器的需求付多服务的运维成本,反之亦然。</p>

<p class="text-slate-600 mt-4">把话说明白的几点保留意见:开销测试测的是客户端 span 成本、内存导出,不是端到端后端延迟;自托管数字来自单一测试环境(WSL2、Docker,测试 @ 2026-06),是占用快照而非压测。Langfuse 的时间受益于已缓存镜像;冷拉取会更久。SigNoz 标为本环境未测而非估算。我们正在把这张矩阵扩展到更多工具,并会给每一行都标注"已测试"和日期。详见<a class="text-blue-600 hover:text-blue-700" href="/methodology.html">我们的方法论</a>。</p>
""",
 "faq_zh": [
   ("LLM 可观测性插桩会拖慢我的应用吗?",
    "可忽略。在我们的测试里,每个 SDK 给一次典型 500ms LLM 调用增加的开销都低于 0.05%;模型调用要主导数千倍。对 LLM 工作负载,插桩开销不应成为选型依据。"),
   ("哪个自托管 LLM 可观测性工具运行起来最轻?",
    "在我们的测试里 Arize Phoenix 处在轻量这一端:单个容器、约 1.35GB 镜像、约 400MB 空闲内存,并立即接受 OTLP 追踪。像 Langfuse 这样的完整平台强大得多,但是多服务栈,运维投入更大。"),
   ("Langfuse 自托管难吗?",
    "在我们 2026-06 的测试里它启动顺利(镜像已缓存约 10 秒),但它是完整平台而非单容器即插即用:一个 6 服务栈(web、worker、Postgres、ClickHouse、缓存、对象存储),空闲内存约 2.1GB,仅 web 容器约 1.1GB。它用自家 SDK 而非原生 OTLP,且自带 MinIO 默认占用主机端口 :9090(在很多开发机上会与 Prometheus 冲突)。在提示词管理、评测和留存方面相当强 —— 只是要为运维重量做好预算。"),
 ],
},
]
