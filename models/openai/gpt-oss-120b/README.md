# gpt-oss-120b

**Creator:** OpenAI · **Family:** gpt-oss · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2025-08-05

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Local private text reasoning and adaptation (medium confidence)

Consider for self-hosting and customization; modern frontier agent equivalence is unsupported.

Conditions: Harmony formatting required; hosted provider quantization/output caps may differ from native weights.

Failure modes / limitations: Cited high-effort service scores0% on Terminal-Bench4.0 and AutomationBench-AA.

Supporting sources: [OpenAI gpt-oss-120b model card](https://huggingface.co/openai/gpt-oss-120b) · [Introducing gpt-oss](https://openai.com/index/introducing-gpt-oss/) · [gpt-oss 120B versus20B high-effort comparison](https://artificialanalysis.ai/models/comparisons/gpt-oss-120b-vs-gpt-oss-20b)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: Open weights with disclosed MoE design and commercially permissive license; deployment guidance fits80GB memory.; contradictory evidence: AA high: Terminal-Bench4.0 and AutomationBench-AA both0%; AA-LCR52%. Older launch benchmarks target different capabilities.; Observation obs-c3ae88e5cf4d: Consider for self-hosting and customization; modern frontier agent equivalence is unsupported.; Potential risk (not a measured failure): Long-horizon failure, hallucination and language weakness; self-hosting does not add missing vision/audio.

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

3 recorded access route(s); 5 model-specific price record(s).

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
| groq | Developer / on-demand / current | input: 0.15 USD / per 1 million tokens; output: 0.6 USD / per 1 million tokens | Tool charges; enterprise provisioned capacity | 2026-10-06 |
| groq | Cached input / current | cached_input: 0.075 USD / per 1 million tokens | Not established in this pass | 2026-10-06 |
| together | standard displayed serverless / current | input: 0.15 USD / per 1M tokens; output: 0.6 USD / per 1M tokens | Not established in this pass | 2026-10-06 |
| groq | Developer / current | input: 0.15 USD / per 1M tokens; output: 0.6 USD / per 1M tokens | Not established in this pass | 2026-10-06 |
| cerebras | Developer PayGo / current | input: 0.35 USD / per 1M tokens; output: 0.75 USD / per 1M tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- Local / self-hosted / Hugging Face weights / compatible runtimes: Downloadable; no runtime executed for this research. quota: Hardware/runtime dependent
- groq / GroqCloud: Production model. quota: {"actual_account_remaining": null, "developer": {"RPM": 1000, "TPM": 250000}, "free": {"RPD": 1000, "RPM": 30, "TPD": 200000, "TPM": 8000}}
- openai / ChatGPT / OpenAI hosted API: No first-party hosted entitlement established; OpenAI catalog entry is not evidence of API hosting. Not established in this pass

## Sources

[gpt-oss-120b model specifications](https://developers.openai.com/api/docs/models/gpt-oss-120b) · [OpenAI gpt-oss-120b model card](https://huggingface.co/openai/gpt-oss-120b) · [Introducing gpt-oss](https://openai.com/index/introducing-gpt-oss/) · [gpt-oss 120B versus20B high-effort comparison](https://artificialanalysis.ai/models/comparisons/gpt-oss-120b-vs-gpt-oss-20b)
