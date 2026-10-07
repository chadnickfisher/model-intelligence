# gpt-oss-120b

**Creator:** OpenAI · **Family:** gpt-oss · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2025-08-05

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Local private text reasoning and adaptation (medium confidence)

Consider for self-hosting and customization; modern frontier agent equivalence is unsupported.

Scope: unresolved / conditional. Scope needs review; the original claim does not establish a specific task ability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): reasoning.general; agent.long_horizon

Judgment ID: judgment-f8a05ea09b9472ae

Conditions: Harmony formatting required; hosted provider quantization/output caps may differ from native weights.

Failure modes / limitations: Cited high-effort service scores0% on Terminal-Bench4.0 and AutomationBench-AA.

Supporting sources: [OpenAI gpt-oss-120b model card](https://huggingface.co/openai/gpt-oss-120b) · [Introducing gpt-oss](https://openai.com/index/introducing-gpt-oss/) · [gpt-oss 120B versus20B high-effort comparison](https://artificialanalysis.ai/models/comparisons/gpt-oss-120b-vs-gpt-oss-20b)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: Open weights with disclosed MoE design and commercially permissive license; deployment guidance fits80GB memory.; contradictory evidence: AA high: Terminal-Bench4.0 and AutomationBench-AA both0%; AA-LCR52%. Older launch benchmarks target different capabilities.; Observation obs-c3ae88e5cf4d: Consider for self-hosting and customization; modern frontier agent equivalence is unsupported.; Potential risk (not a measured failure): Long-horizon failure, hallucination and language weakness; self-hosting does not add missing vision/audio.

### Coding.scoped_edit (low confidence)

Can solve some small editing exercises, but this older diff-based setup needs repair and format validation.

Scope: direct / warning. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.scoped_edit

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-5f82e79ab532e98f

Conditions: Aider0.85.3.dev; OpenRouter; high effort; diff format;225Polyglot exercises;2025-08-06.

Failure modes / limitations: Only31/225 passed initially;94/225 after second pass.; 79.1% well-formed cases;47 cases had malformed responses.

Supporting sources: [Aider Polyglot gpt-oss-120b result](https://aider.chat/docs/leaderboards/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Old immutable-checkpoint evidence; current provider/harness parity unverified.; Research provenance: history/research/2026-10-07/coding-input.json :: scoped_debugging:gpt-oss-120b-scoped-aider; Confidence concerns this bounded claim, not a capability score.

### Coding.debugging (low confidence)

Weak for autonomous whole-repository bug hunting in this measured route; other repair settings remain open.

Scope: direct / weak. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-3f23cd037accf1ae

Conditions: Groq pinned via OpenRouter with fallbacks disabled; effort field dropped, provider default unknown.; Harness: Claude Code / OpenRouter; effort: default; effort evidence: inert_default.; 105 planted defects across TypeScript VS Code extension (~28K lines) and React/Supabase LMS (~60K lines).; One agentic round per repository; native CLI/tools; same task prompt but nonidentical harnesses, contexts and budgets.; Blind diff-based answer-key grading; extra unplanted fixes excluded; private corpus/judgments prevent full external reproduction.

Failure modes / limitations: No planted defects fixed across three runs; early stopping/report-writing failures observed.; Missing route accounting prevents verified context-regime parity.

Supporting sources: [Bug Hunt Bench frozen measurements](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/data/benchmark.json) · [Bug Hunt Bench receipts and boundaries](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/README.md) · [Bug Hunt Bench individual configuration caveats](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/run-notes.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Result measures finding AND implementing fixes; do not relabel it as code-review recall or test-generation quality.; No matched independent contradiction located; partial successes and misses coexist.; Research provenance: history/research/2026-10-07/coding-input.json :: scoped_debugging:gpt-oss-120b-debug-bughunt; Confidence concerns this bounded claim, not a capability score.

### Coding.debugging (low confidence)

A viable candidate for constrained single-file repair with visible tests.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-e2b504d398235939

Conditions: ClosedCode/Ollama,high effort,ASUSGX10; exact quantization not stated.

Failure modes / limitations: Single synthetic CSV case cannot establish broad reliability.

Supporting sources: [Local ClosedCode editing and CSV repair study](https://zenn.dev/nicktominaga/articles/closedcode-local-llm-benchmark?locale=en)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: The zero-score whole-repository audit used a different host/effort/harness. It bounds transfer rather than disproving this local result.; Related caution source: bughunt-data. It is not a controlled contradiction because the task size, route, effort and harness differ.; Research provenance: history/research/2026-10-07/coding-input.json :: scoped_debugging:gpt-oss-120b-debug-local-csv; Confidence concerns this bounded claim, not a capability score.

### Coding.tests (medium confidence)

A viable backbone for mutation-guided Java test generation when the full feedback harness is retained.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.tests

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-38c7d3ecbd4a7108

Conditions: Five-action adversarial method; source metrics are method-level, not bare-model pass rates.; Named release matches; preserve source-specific provider, snapshot and precision limitations.

Failure modes / limitations: Much lower fault detection in simpler generation harnesses; coverage is incomplete.

Supporting sources: [Test vs Mutant: Adversarial LLM Agents for Robust Unit Test Generation](https://arxiv.org/html/2602.08146v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Research provenance: history/research/2026-10-07/coding-input.json :: review_tests_frontend:tests-oss120; Confidence concerns this bounded claim, not a capability score.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Mixture-of-experts Transformer; alternating dense/local sparse attention; grouped-query attention; RoPE |
| parameters | total: 117000000000; active: 5100000000 |
| context window | 131072 |
| maximum output | 131072 |
| modalities | input: text; output: text |
| language support | Mostly English training; multilingual quality varies |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

6 recorded access route(s); 8 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Apache-2.0

Restrictions: Not established in this pass

Commercial use: Unknown / not established

Redistribution: Unknown / not established

Hosted service: Unknown / not established

Local weights/runtime availability: available

Hardware: Published reference memory: 80 GB; runtime/context overhead and configuration must be checked.

Local conditions: Not established in this pass

## Gaps and caveats

- Deployment-specific latency, maximum usable context and total RAM depend on quantization/runtime/KV cache
- Exact supported-language inventory unverified

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| together | Standard / current | input: 0.15 USD / per 1 million tokens; output: 0.6 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |
| groq | Standard / current | input: 0.15 USD / per 1 million tokens; output: 0.6 USD / per 1 million tokens; cached_input: 0.075 USD / per 1 million tokens | Cached input is derived50% published discount on successful exact-prefix cache hits. | 2026-10-07 |
| groq | Capped free evaluation / tier / current | input: 0 USD / per 1 million tokens; output: 0 USD / per 1 million tokens | Free account quotas, not infinite free usage. | 2026-10-07 |
| groq | Developer / on-demand / historical | input: 0.15 USD / per 1 million tokens; output: 0.6 USD / per 1 million tokens | Tool charges; enterprise provisioned capacity | 2026-10-06 |
| groq | Cached input / historical | cached_input: 0.075 USD / per 1 million tokens | Not established in this pass | 2026-10-06 |
| cerebras | Developer PayGo / current | input: 0.35 USD / per 1M tokens; output: 0.75 USD / per 1M tokens | Not established in this pass | 2026-10-06 |
| groq | Developer / historical | input: 0.15 USD / per 1M tokens; output: 0.6 USD / per 1M tokens | Not established in this pass | 2026-10-06 |
| together | standard displayed serverless / current | input: 0.15 USD / per 1M tokens; output: 0.6 USD / per 1M tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- groq / hosted free tier api: documented_not_execution_tested. Not established in this pass
- groq / hosted metered api: documented_not_execution_tested. Not established in this pass
- together / hosted metered api: documented_not_execution_tested. Not established in this pass
- Local / self-hosted / Hugging Face weights / compatible runtimes: Downloadable; no runtime executed for this research. quota: Hardware/runtime dependent
- groq / GroqCloud: Production model. quota: {"actual_account_remaining": null, "developer": {"RPM": 1000, "TPM": 250000}, "free": {"RPD": 1000, "RPM": 30, "TPD": 200000, "TPM": 8000}}
- openai / ChatGPT / OpenAI hosted API: No first-party hosted entitlement established; OpenAI catalog entry is not evidence of API hosting. Not established in this pass

## Sources

[gpt-oss-120b model specifications](https://developers.openai.com/api/docs/models/gpt-oss-120b) · [OpenAI gpt-oss-120b model card](https://huggingface.co/openai/gpt-oss-120b) · [Introducing gpt-oss](https://openai.com/index/introducing-gpt-oss/) · [gpt-oss 120B versus20B high-effort comparison](https://artificialanalysis.ai/models/comparisons/gpt-oss-120b-vs-gpt-oss-20b)
