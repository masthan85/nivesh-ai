# Building a trustworthy, grounded AI investment-research assistant ("Nia") and the retail-investor UX around it (as of Nov 2026)

Research note scope: web research only (repository not accessed). Roughly 15 tool calls. robinhood.com could not be fetched from this session (blocked by the network allowlist), so Robinhood findings come from search snippets and secondary coverage. Where only a search-result summary was available (not the full primary page), that is flagged.

---

## 1. Architecture: tools over deterministic services, RAG, citations, structured outputs, caching, routing; what finance builders publish

### Takeaway
The current Anthropic API gives Nia everything it needs to move from "holdings pasted into a prompt" to a grounded assistant. Deterministic services can sit behind strict tool use (schema-validated tool inputs). Retrieved filings and news can go in as `search_result` blocks so citations are native. Final answers can be constrained to a JSON schema. Prompt caching and the Haiku/Sonnet/Opus price spread make routing cheap. Published fintech builds (Morgan Stanley, Robinhood Cortex) stress two things: eval-first rollout, and a simple model-in-a-loop design over shared tools rather than many narrow agents.

### Cited Findings
**Current Claude models and pricing (Anthropic docs, fetched Nov 2026)**
- Current lineup: Claude Fable 5.2 (`claude-fable-5-2`, $8/$40 per MTok input/output), Claude Opus 5.5 (`claude-opus-5-5`, $4/$20), Claude Sonnet 5.5 (`claude-sonnet-5-5`, $2/$10) and Claude Haiku 5.5 (`claude-haiku-5-5`, "from $0.10 / from $0.50"). All have 1M-token context, 128K max output, tool use, multilingual and vision support. Anthropic describes Haiku 5.5 as "for high-volume, latency-sensitive tasks such as classification, extraction, and routing", and recommends starting with Opus 5.5 for most workloads — [Anthropic Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- The Batch API is 50% off. Prompt-cache reads cost 10% of the base input price, 5% on Opus 5.5 and Sonnet 5.5, and 2.5% on Fable 5.2/5.1 — [Anthropic Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- Thinking is "adaptive" on current models and is steered by an `effort` parameter (default `medium` on Opus 5.5 and Haiku 5.5, `high` on Sonnet 5.5 and Fable 5.2). The manual `budget_tokens` extended-thinking mode is not accepted on models after the 4.6 generation — [Anthropic Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- Model IDs from the 4.6 generation onward are dateless pinned snapshots. Retirement is no sooner than Sep–Nov 2027 for the current models — [Anthropic Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)

**Citations and search-result blocks**
- `search_result` content blocks let Claude cite your own retrieved content the way it cites web search. Each block has `type`, `source` (any stable string, such as a URL or internal document ID), `title`, a `content` array of text blocks, and an optional `citations: {enabled: true}`. Blocks can be sent inside a tool result or directly in a user message. Citations appear on the response text blocks that draw on the content, with no special prompting. All active models except Claude Haiku 3 support this, and no beta header is required — [Anthropic docs: Search results](https://platform.claude.com/docs/en/build-with-claude/search-results) (search-result summary of the docs page; an older Japanese page still mentions the `search-results-2025-01-01` beta header, which suggests the feature has since become generally available)

**Structured outputs and strict tool use**
- Structured outputs come in two parts: (a) JSON outputs via `output_config.format` with `type: "json_schema"`, and (b) strict tool use via `strict: true` on a tool definition, which validates tool names and inputs against `input_schema`. The two can be combined in one request. Constrained decoding guarantees valid JSON, required fields and correct types, with "no retries needed". Python `client.messages.parse(output_format=PydanticModel)` returns `parsed_output` — [Anthropic docs: Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- Limits: no recursive schemas, `oneOf` or `not`. No numeric `minimum`/`maximum` and no string-length constraints (400 error), so these must be validated in your own code. The first use of a schema adds grammar-compilation latency (cached for 24h). Changing `output_config.format` invalidates the prompt cache for that conversation. Supported on Opus 5.5/5/4.x, Sonnet 5.5/5/4.6/4.5, Haiku 5.5/4.5 and Fable/Mythos 5.x. Current API version header example: `anthropic-version: 2026-10-21` — [Anthropic docs: Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- I could not confirm from the portion of the page I read whether JSON outputs can be combined with citations in the same response. See Gaps.

**What finance builders publish**
- **Morgan Stanley (OpenAI case study):** built "an evaluation framework to test each AI use case before it went live", starting with three evals (translation first, then summarization), with expert feedback at every step. Later added translation evals for multilingual clients and worked with OpenAI to "fine-tune retrieval methods" as the document library grew. Reports that 98% of advisor teams use it, and cites zero data retention as important. This is vendor-published, so it is promotional — [OpenAI: Morgan Stanley](https://openai.com/index/morgan-stanley/); see also [ZenML LLMOps database write-up](https://www.zenml.io/llmops-database/enterprise-knowledge-management-with-llms-morgan-stanley-s-gpt-4-implementation)
- **Robinhood Cortex:** "Cortex Digests" are AI-generated, plain-language explanations of what *may* be moving a stock's price. They appear on stock detail pages, and "Portfolio Digests" extend them to the user's own holdings. Launched in the UK on 19 Aug 2025. The Cortex assistant is described as a conversational copilot "based on your overall portfolio" and is limited to Gold subscribers. A next-generation version was announced for Q1 2026 — [Robinhood support: Cortex Digests](https://robinhood.com/us/en/support/articles/cortex-digests); [Robinhood newsroom UK Digests](https://robinhood.com/newsroom/digests-by-robinhood-cortex-uk); [Finextra](https://www.finextra.com/newsarticle/46465/robinhood-uk-rolls-out-ai-investing-assistant-to-decode-market-movements) (Robinhood pages known only through search snippets; fetch blocked)
- **Robinhood engineering, Aug 2026 ("Loop stays dumb so the model can be smart"):** search-snippet summary says Robinhood moved from narrow per-agent scopes to "one capable model in a loop". One reason: holdings and recent trades lived with the account agent, but the research agent needed them too. The post recommends keeping the system simple and maintaining a good eval set — [Robinhood careers blog](https://robinhood.com/us/en/careers/blog/loop-stays-dumb-so-the-model-can-be-smart/) (could not fetch; snippet only, so verify before quoting)
- **Public:** Axios (Dec 2025) reports Public launched an AI-powered brokerage feature that lets users build their own ETFs. I could not verify details of a "Public Alpha" product — [Axios](https://www.axios.com/2025/12/17/ai-robinhood-stock-market)

### Inferences
- **Recommended Nia pattern:** a single model in a tool loop, with a server-side tool registry that calls Nivara's deterministic services. Examples: `get_portfolio_valuation`, `compute_xirr`, `get_capital_gains_estimate`, `project_goal`, `get_price_history`, `search_filings`, `search_news`. All use `strict: true`. The model chooses tools and writes the explanation. Every number comes from a tool result. Robinhood's published lesson argues against splitting this into many sub-agents early.
- **Retrieval:** chunk annual reports, concall transcripts, exchange filings (NSE/BSE corporate announcements) and licensed news into a vector or hybrid index. Return hits as `search_result` blocks, using `source` = canonical document URL plus page/section and `title` = "Company — Doc type — Date". This gives native, clickable citations without having to prompt-engineer a citation format.
- **Output contract:** for UI cards (e.g. "Portfolio health summary"), use `output_config.format` with a schema whose fields reference tool-output IDs (e.g. `{"metric_id": "xirr_portfolio", "explanation": "..."}`). The frontend then renders the actual number from the tool output, not from model text. Keep free-form chat answers separate, using citations.
- **Cost and routing:** use Haiku 5.5 for intent classification, guardrail classification and query rewriting. Use Sonnet 5.5 as the default answerer. Escalate to Opus 5.5 only for long multi-document research. Cache the static system prompt, tool definitions and disclaimers (cache reads at 5–10% of input price). Avoid toggling `output_config.format` mid-conversation, because it breaks the cache. Use the Batch API (50% off) for overnight "portfolio digest" generation.
- MCP: exposing Nivara's services as an MCP server is optional. In-process tool definitions are simpler for a single FastAPI backend. MCP becomes useful if the same tools are later reused by internal agents or by partner clients.

### Gaps
- I did not fetch the Anthropic prompt-caching page (cache-write multipliers, TTL options) or the pricing page. Only the cache-read percentages above are verified.
- I did not confirm whether citations and `output_config.format` can be used together.
- There were no primary sources for Bloomberg (BloombergGPT / Terminal AI features), Perplexity Finance architecture or Public's AI in this pass. I found no reliable architecture details for those within the call budget.
- The Robinhood engineering post was not readable (robinhood.com has to be allowed in the session's network settings).

---

## 2. Safety and compliance guardrails

### Takeaway
For an Indian product the binding constraint is regulatory. SEBI restricts unregistered investment advice and (via its Jan 2025 finfluencer clarifications) the use of recent price data in "education". SEBI has also consulted on a five-pillar AI/ML governance framework. Technically, frontier LLMs still make 10–20% errors on multi-step numerical reasoning over financial tables, and remain highly vulnerable to injected "news", so arithmetic must live in code and retrieved text must be treated as untrusted data.

### Cited Findings
**Regulatory (India)**
- SEBI's 29 Jan 2025 circular (building on Aug and Oct 2024 actions) bars regulated entities from associating with persons who give unregistered investment advice or make unsubstantiated return claims. Investor education is permitted, but educators "cannot use stock names, codes, or price data from the past three months in any form that could imply investment advice" — [Business Standard](https://www.business-standard.com/markets/news/sebi-finfluencer-circular-live-stock-data-market-education-rules-125013000571_1.html); [Inc42](https://inc42.com/buzz/sebi-issues-clarifications-on-finfluencer-guidelines); [Legal500](https://www.legal500.com/developments/thought-leadership/securities-law-update-sebi-imposes-restrictions-on-intermediaries-and-finfluencers/) (secondary law-firm and news summaries; full circular text not read)
- SEBI consultation paper "Guidelines for Responsible Usage of AI/ML in Indian Securities Markets" (20 Jun 2025; comments closed 11 Jul 2025). It covers regulated entities whose AI use directly affects clients, including advisory services, with a lighter regime for internal-only use. It sets out five pillars, starting with model governance, and stresses data governance (ownership, access controls, encryption). It builds on the Feb 2025 Regulation 16C amendment to the intermediaries regulations, which makes regulated entities responsible for the AI tools they use, and on IOSCO's Mar 2025 AI report — [Business Standard](https://www.business-standard.com/markets/news/sebi-proposes-ai-ml-guidelines-for-market-participants-125062001137_1.html); [Mondaq](https://www.mondaq.com/india/new-technology/1642480/sebis-consultation-paper-on-aiml-guidelines-reconciling-innovation-with-investor-protection); [Taxmann](https://www.taxmann.com/post/blog/sebi-proposes-ai-ml-governance-framework-for-securities-markets). I found no confirmation that the guidelines have been finalized. A Digital Policy Alert entry titled "finalised consultations" exists but was not read — [Digital Policy Alert](https://digitalpolicyalert.org/event/32090-securities-and-exchange-board-of-india-finalised-consultations-on-guidelines-for-responsible-usage-of-aiml-usage-in-security-markets)

**Numeric hallucination evidence**
- FinanceBench (Patronus AI, Nov 2023, older): GPT-4 Turbo with a retrieval system "incorrectly answered or refused to answer 81%" of a 150-question sample of questions over public-company filings. Long-context setup reached about 79% correct. "Oracle" setup (the correct passage supplied) reached about 85% — [Patronus announcement](https://patronus.ai/announcements/patronus-ai-launches-financebench-the-industrys-first-benchmark-for-llm-performance-on-financial-questions); [arXiv 2311.11944](https://web3.arxiv.org/abs/2311.11944). Secondary sources disagree on which retrieval configuration produced the 81% figure; one gives about 50% correct and 39% refused for per-document vector stores. Old (2023) models; the lesson is that retrieval quality dominates.
- FAITH (arXiv 2508.05201, 2025): built on S&P 500 annual reports. Frontier models (Claude Sonnet 4, Gemini 2.5 Pro) achieve high overall accuracy but "still exhibit 10–20% error rates on multi-step numerical reasoning" — [FAITH](https://arxiv.org/abs/2508.05201v1)
- A 2026 paper ("Confidently Wrong") proposes detecting hallucinations in financial QA from LLM internal states. Not read in full — [arXiv 2607.11414](https://arxiv.org/pdf/2607.11414)

**Prompt injection via news and documents**
- "Fake News, Real Crashes: Information Injection Attacks on LLM Financial Trading Agents" (arXiv 2610.26438, 2026) found GPT-5 "remains vulnerable at 45%, on par with GPT-4o". A bullish injected item forces buying, and a bearish one ("CEO arrested") forces selling — [arXiv 2610.26438](https://arxiv.org/pdf/2610.26438) (snippet-level; paper not read in full)
- A 2026 fintech trustworthy-AI survey flags financial RAG pipelines as an injection vector because the model "ingest[s] malicious payloads from external reports or web content" — [arXiv 2605.30650](https://arxiv.org/pdf/2605.30650)
- Forcepoint documented 10 in-the-wild indirect prompt-injection payloads aimed at AI agents, one of which contained a PayPal.me link and full payment instructions — [Infosecurity Magazine](https://infosecurity-magazine.com/news/researchers-10-wild-indirect)

### Inferences
- **Explain-not-advise policy, enforced in layers:**
  1. The system prompt defines allowed acts: explain, compare factual attributes, describe risk, educate. It also defines disallowed acts: buy/sell/hold calls on a security, price targets, "should I", allocation percentages for this user, and return guarantees.
  2. A pre-classifier (Haiku 5.5, structured output `{intent: "advice_request" | "education" | "portfolio_fact" | ...}`) routes "should I buy X?" to a templated reframe. The reframe explains the factors a person would weigh, links to a SEBI-registered RIA/RA directory, and does not refuse coldly.
  3. A post-generation checker (Haiku plus regex) catches imperative trading verbs, target prices and future-return claims, and regenerates or blocks.
- Given SEBI's 3-month price-data rule for unregistered educators, have Nivara's legal counsel decide whether Nia discussing a named stock's recent price moves counts as education or advice. Nivara's own registration status (RA/IA or neither) determines this; it is not a technical choice.
- **Numeric grounding:** the model never computes. Every figure displayed must trace to a tool output ID. Run a post-check that extracts all numbers from the response and verifies each appears in (or is a formatted version of) a tool result or a cited document span. Unmatched numbers trigger regeneration. This directly targets the FAITH-style 10–20% multi-step error rate.
- **Injection defences:** pass news and filings only as `search_result` or tool-result content, never in the system prompt. Strip HTML and hidden text. Have no tools with side effects (no order placement), so injection can at worst mislead the explanation. Add an eval set of poisoned news items. Show source and date next to every news-based claim.
- **PII minimisation:** send holdings as ISIN, quantity and cost (no PAN, name, folio or demat IDs). Hash user IDs in logs. Use a zero-data-retention arrangement if available (Morgan Stanley cites ZDR as important; structured outputs are ZDR-eligible with qualifications per Anthropic docs).
- **Audit log:** per turn, persist the prompt version, model ID (pinned snapshot), tool calls and outputs, retrieved source IDs, guardrail verdicts and the final text. This aligns with SEBI's draft emphasis on model governance and Regulation 16C accountability.

### Gaps
- I did not read the full SEBI circular text, the final status of the AI/ML guidelines, or the specific RA/IA regulation definitions of "investment advice". Legal review is needed.
- I did not fetch Anthropic's own guidance on mitigating prompt injection or jailbreaks, or any guardrail-library documentation (e.g. NeMo Guardrails, Llama Guard).
- I found no published refusal or disclaimer A/B-test evidence specific to finance chatbots.

---

## 3. Evaluation and observability

### Takeaway
Public financial benchmarks (FinanceBench, FinQA, TAT-QA, FinBen) are useful for smoke-testing retrieval and numerical reasoning, but they are US-centric and partly saturated. Nia needs its own India-specific eval set (Indian filings, XIRR/LTCG questions, advice-bait prompts, poisoned news) run in CI. For tracing, OpenTelemetry GenAI semantic conventions are the emerging interoperability layer, still in "Development" status, and Langfuse and Datadog ingest them.

### Cited Findings
- FinBen (NeurIPS 2024 datasets track, older) covers 36 datasets and 24 tasks across seven aspects, with FinQA, ConvFinQA and TAT-QA in the quantitative-reasoning tier. Instruction tuning helped textual analysis but gave "limited benefits for complex tasks such as QA" — [FinBen arXiv 2402.12659](https://arxiv.org/abs/2402.12659v2); [NeurIPS slides](https://nips.cc/media/neurips-2024/Slides/97525.pdf)
- Critique: in FinBen, 8 of 36 datasets are textual-analysis tasks, 7 of them easy enough for zero-shot LLMs to exceed 60%, which inflates aggregate scores — [arXiv 2506.14028](https://arxiv.org/pdf/2506.14028v2.pdf) (per search summary)
- FinanceBench: 10,231 questions over public filings, with a 150-question open sample. Results above — [Patronus docs](https://docs.patronus.ai/docs/research_and_differentiators/financebench)
- Morgan Stanley's eval-before-launch process (summarization and translation evals, with expert graders) — [OpenAI](https://openai.com/index/morgan-stanley/)
- OpenTelemetry GenAI semantic conventions remain in "Development" (not stable) status as of mid-2026. Sources report a June 2026 move to a dedicated repository around semconv v1.42.0, though version numbers conflict across sources — [OpenTelemetry blog 2026](https://opentelemetry.io/blog/2026/genai-observability/); [Greptime](https://greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions); [dev.to (azena-ai)](https://dev.to/azena-ai/opentelemetrys-genai-semantic-conventions-are-not-stable-yet-heres-what-actually-shipped-in-2026-3mke)
- Datadog LLM Observability ingests OTel traces following GenAI semconv 1.37+ or OpenInference — [Datadog docs](https://docs.datadoghq.com/llm_observability/instrumentation/otel_instrumentation/)
- Langfuse accepts OTLP/OTel GenAI traces. One blog reports ClickHouse acquired Langfuse in Jan 2026, which I did not verify against a primary source — [Medium on Langfuse OTel](https://medium.com/@sharanharsoor/opentelemetry-for-llmops-how-langfuse-achieved-universal-multi-language-support-without-building-782d843adf3c); [GenAI observability comparison](https://mlunadia.github.io/observing-ai/genai-observability-compared.html)
- Citation-trust research (Ding et al., AAAI 2025): the presence of citations raised user trust even when the citations were random, and trust fell when users actually checked them. This is an argument for evaluating citation *accuracy*, not just whether citations are present — [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/34550)

### Inferences
- **Nia eval set (version-controlled JSONL, run in CI on every prompt or model change):**
  - (a) Grounded portfolio QA: synthetic portfolios with known XIRR, gains and concentration. Score exact numbers.
  - (b) Filing QA on 20–30 Nifty companies' annual reports and concall transcripts, in a FinanceBench style, with gold answers and gold page citations.
  - (c) Advice-bait and red-team prompts in English, Hindi and Hinglish ("kaunsa stock 2x karega?", "target price batao"). Score refusal-plus-helpful-reframe.
  - (d) Poisoned-news injection cases.
  - (e) Tone and readability for low-literacy users.
- **Scoring:** deterministic checks first (numbers match tool outputs; each cited `source` exists and contains the quoted span). Then an LLM-as-judge (a different or larger model, with a rubric) for helpfulness and compliance. Calibrate the judge against about 100 human-labelled items.
- **Observability:** instrument FastAPI with OTel GenAI attributes (model, tokens, cache hits, tool calls) and export to self-hosted Langfuse (helps data residency) or Datadog. Track cost per conversation, cache-hit rate, guardrail-trigger rate, citation-click rate and thumbs-down rate.

### Gaps
- I did not retrieve exact current FinQA or TAT-QA scores for 2026 models, or details of Braintrust or Helicone features.
- I found no India-specific financial QA benchmark (over BSE/NSE filings) within budget.

---

## 4. Indian context: languages, voice, literacy, investor-behaviour evidence

### Takeaway
Financial literacy in India is low (about 24–27% in NCFE's last national survey, from 2019), and derivatives losses are severe and persistent (about 91% of individual F&O traders lost money in FY25, with net losses of about ₹1.06 lakh crore). Nia's highest-value role is therefore education and behavioural guardrails, not "alpha". Sarvam's 2026 speech stack (Saaras v3 speech-to-text; Bulbul v3/v4 Flash text-to-speech) makes vernacular voice practical.

### Cited Findings
- SEBI FY25 F&O study: about 91% of individual equity-derivatives traders made net losses (91.1% the prior year). Net losses rose about 41% to ₹1,05,603 crore in FY25 from ₹74,812 crore in FY24, after transaction costs. Sample: top 13 brokers, about 96 lakh unique traders. Losses eased in Q4 FY25 after SEBI's curbs — [Business Standard](https://www.business-standard.com/markets/news/net-losses-of-traders-in-fo-widens-in-fy25-sebi-study-125070701221_1.html); [Moneylife](https://moneylife.in/article/91-percentage-of-retail-traders-lost-money-in-derivatives-losses-in-fo-surged-41-percentage-to-rs105-lakh-crore-in-fy25-sebi-study/77613.html). 5paisa reports ₹1.02 lakh crore instead (conflict) — [5paisa](https://www.5paisa.com/news/sebi-study-reveals-retail-traders-lost-over-rs1-lakh-crore-in-fy25-from-derivatives-trading)
- Average loss is about ₹1.1 lakh per trader in FY25 — [Value Research](https://www.valueresearchonline.com/stories/225398/average-trader-lost-rs-1-1-lakh-fo-fy25/)
- A later SEBI FY26 study reportedly found about 9 in 10 still losing, with aggregate losses of ₹91,685 crore, and active individual derivatives traders falling from 98.1 lakh (FY25) to 78.6 lakh (FY26). Methodology differs from earlier counts — [Open Magazine](https://openthemagazine.com/business/sebi-fo-loss-study-explained-why-9-in-10-retail-traders-lost-91685-crore-in-fy26) (secondary; verify against SEBI)
- Financial literacy: NCFE's NFLIS 2019 put literacy at about 24–27%. NCAER cites 27% for men versus 21% for women. I found no newer NCFE national survey — [NCAER](https://ncaer.org/?p=28914); [Punekar News / VP Research report](https://www.punekarnews.in/?p=214882)
- Sarvam AI (2026): Saaras v3 became the default speech-to-text model (replacing Saarika v2.5) in June 2026. Bulbul v3 text-to-speech covers 22 Indian languages plus English with streaming latency under 250ms. Bulbul v4 Flash covers 11 languages at ₹20 per 10k characters (versus ₹30 for v3). LLMs: Sarvam-30B and Sarvam-105B; `sarvam-m` deprecated. Mayura handles translation — [Sarvam changelog](https://docs.sarvam.ai/api/changelog); [Analytics India Mag](https://analyticsindiamag.com/ai-news/sarvam-ai-launches-bulbul-v4-flash-for-real-time-speech-in-11-indian-languages); [Business Standard on Saaras v3](https://business-standard.com/technology/tech-news/saaras-v3-beats-gemini-gpt-4o-on-indian-speech-benchmarks-says-sarvam-ai-126021200384_1.html) (benchmark claims are vendor-reported)
- All current Claude models list multilingual capability — [Anthropic Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)

### Inferences
- **Language architecture:** let Claude reason and answer directly in Hindi or Hinglish, mirroring the user's script and register. Use Sarvam Saaras for speech-to-text and Bulbul for text-to-speech in a voice mode. Keep numbers formatted in the Indian system (lakh/crore) by deterministic code, not by the LLM. Add Hinglish and regional-language items to the eval set.
- **F&O guardrail:** if the user's holdings or questions show derivatives activity, Nia should surface SEBI's own loss statistics neutrally ("SEBI found ~91% of individual F&O traders lost money in FY25"), with a citation. This is education grounded in regulator data.
- **Plain-language defaults:** given about 24–27% literacy, default to short answers with a "what this means for you" line, glossary pop-ups for XIRR, CAGR, expense ratio and LTCG, and progressive disclosure.

### Gaps
- I did not research AI4Bharat (IndicTrans2, IndicWhisper), Bhashini APIs or Krutrim in this pass.
- I found no NCFE 2025/2026 survey data or SEBI investor-survey findings on specific misconceptions (e.g. confusing XIRR with absolute return, or understanding of expense ratios).
- I found no measured comparison of Claude versus Sarvam LLMs on Hinglish financial QA.

---

## 5. UX for retail investors: nudges, explainability, trust, ethical engagement

### Takeaway
The evidence says frequent trading harms retail returns and that citations raise trust even when they are wrong. Nia's UX should therefore (a) make sources verifiable and visible rather than decorative, (b) nudge toward diversification and SIP discipline, and (c) avoid alerts and gamification that increase trading frequency. Robinhood's "Digests" pattern ("what *may* be moving this stock", attached to the holding) is a useful explanatory template.

### Cited Findings
- Barber & Odean (Journal of Finance, 2000; older but foundational): 66,465 US households, 1991–96. Households trading most earned 11.4% a year versus the market's 17.9%, which the authors attribute to overconfidence. Critics note the period and sample limits — [EconPapers](https://econpapers.repec.org/RePEc:bla:jfinan:v:55:y:2000:i:2:p:773-806); [Odean page](https://faculty.haas.berkeley.edu/odean/papers/returns/returns.html); critique: [NBER w25838 (Bonaparte & Cooper)](https://www.nber.org/system/files/working_papers/w25838/revisions/w25838.rev0.pdf)
- NN/g: users rarely click citation links in AI answers, may not notice inaccurate or fabricated citations, and "can easily overtrust AI outputs just because they look well-cited". UX teams can shape how sources are presented — [NN/g Explainable AI](https://nngroup.com/articles/explainable-ai/)
- Ding et al. (AAAI 2025): trust rose with any citations, even random ones, and fell when users checked them — [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/34550)
- Robinhood frames Digests as plain-language explanations of what "may be" moving a price, placed on the stock and portfolio pages — [Robinhood support](https://robinhood.com/us/en/support/articles/cortex-digests)
- A UXmatters article (Jul 2026) argues that first-session trust in AI products depends on onboarding that shows capabilities and limits. Not read in full — [UXmatters](https://www.uxmatters.com/mt/archives/2026/07/first-session-trust-in-ai-products-why-code-editors-onboard-users-better-than-chatbots.php)

### Inferences
- **Trust patterns:**
  - Inline citation chips showing source, document type and date, which open the exact page or span.
  - An "as of" timestamp on every number.
  - A "How Nia got this" expander listing the tool calls made (e.g. "Computed from your 14 holdings using NAV as of 24 Nov").
  - A persistent but unobtrusive "Nia explains; it doesn't advise" badge, rather than long disclaimers on every message.
  - An onboarding card that states what Nia can and can't do.
- **Behavioural nudges (all computed deterministically, explained by the LLM):**
  - Concentration alerts (single stock or sector above a threshold).
  - Overlap between mutual funds.
  - SIP-streak or continuity encouragement, and "stay the course" messaging during drawdowns, showing historical drawdown context.
  - Cooling-off copy before high-risk actions (e.g. F&O), quoting SEBI loss data.
  - A cost drag explainer (expense ratio, turnover).
- **Ethical engagement:**
  - Favour weekly or monthly portfolio digests (batch-generated, cheaper) over real-time price pushes.
  - Use goal-progress notifications rather than "stock moved 5%" pushes.
  - Avoid confetti and streak mechanics tied to trades, though it is fine to tie them to learning or SIP continuity.
  - Measure success by retained understanding (quiz or "did this help?") and SIP persistence, not trade count.
- **Metric explainability:** pair each metric (XIRR, max drawdown, volatility) with a one-line plain-language meaning, a personalised example from the user's own data, and a "compare with benchmark" toggle (Nifty 50 TRI). Make the layout mobile-first, with large tap targets, vernacular toggles and voice input.

### Gaps
- I did not retrieve primary evidence on gamification or push notifications and trading frequency (e.g. studies on app-based trading or the Robinhood "digital engagement practices" literature), or Baymard/NN/g fintech-specific mobile usability findings, within budget.
- I found no published retention or ethical-engagement metrics from Indian platforms (Zerodha, Groww, INDmoney).
