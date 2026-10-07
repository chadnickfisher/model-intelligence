# Gemini 3.5 Flash-Lite

**Creator:** Google DeepMind · **Family:** Gemini · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-07-21

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### High volume parsing classification and bounded subagent work (medium confidence)

Reasonable economical starting point, with validation and escalation for difficult cases.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): knowledge.extraction; knowledge.classification; agent.tool_use

Judgment ID: judgment-06ddf2c86085a946

Conditions: high; temperature 1; output 65,536

Failure modes / limitations: Not established in this pass

Supporting sources: [Artificial Analysis gemini-3-5-flash-lite](https://artificialanalysis.ai/models/gemini-3-5-flash-lite) · [Vals AI gemini-3.5-flash-lite](https://www.vals.ai/models/google_gemini-3.5-flash-lite)

Contradictory or limiting sources: [Gemini 3.5 Flash-Lite model card](https://deepmind.google/models/model-cards/gemini-3-5-flash-lite/) · [Vals AI gemini-3.5-flash-lite](https://www.vals.ai/models/google_gemini-3.5-flash-lite)

Evidence notes: task-conditioned synthesis; no inference runs performed; Observation obs-16516ab6f54e: Measured decode speed supports throughput-sensitive experimentation.; Observation obs-8b65b1136da3: Useful bounded coding capability with weaker difficult agent performance.; Observation obs-04efb4d01f02: Large context is not equal to reliable exhaustive retrieval.

### Measured generation behavior (medium confidence)

Measured decode speed supports throughput-sensitive experimentation. Measurements: {"output_tokens_per_second": 341.5}. These describe the cited benchmark configuration only.

Scope: performance / conditional. Cost, deployment or throughput observation; not a task capability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-f7f4e9d19bb0fd4e

Conditions: Not established in this pass

Failure modes / limitations: Not established in this pass

Supporting sources: [Artificial Analysis gemini-3-5-flash-lite](https://artificialanalysis.ai/models/gemini-3-5-flash-lite)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: API snapshot; no end-to-end latency or local execution claim.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Gemini 3.1 Flash-Lite-derived; published lineage points to Gemini 3 Pro sparse MoE transformer |
| parameters | Unknown / not established |
| context window | 1048576 |
| maximum output | 65536 |
| modalities | input: text; image; video; audio; PDF; output: text |
| language support | Unknown / not established |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

3 recorded access route(s); 1 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Not established / proprietary terms must be checked

Restrictions: Not established in this pass

Commercial use: Unknown / not established

Redistribution: Unknown / not established

Hosted service: Unknown / not established

Local weights/runtime availability: unavailable

Hardware: Not established in this pass

Local conditions: Not established in this pass

## Gaps and caveats


## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| google-developer-api | paid_standard / current | input_all_supported_modalities: 0.3 USD / per_1M_tokens; output_including_thinking: 2.5 USD / per_1M_tokens; cache_read: 0.03 USD / per_1M_tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- google-developer-api / first-party-api: documented route; account eligibility unverified. Not established in this pass
- google-ai-studio / Google AI Studio: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass
- google-consumer / Gemini app / Google AI plans: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass

## Sources

[Gemini 3.5 Flash-Lite model card](https://deepmind.google/models/model-cards/gemini-3-5-flash-lite/) · [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Gemini 3.5 Flash-Lite API model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite) · [Gemini API release notes](https://ai.google.dev/gemini-api/docs/changelog) · [Gemini 3.1 Flash-Lite model card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-1-Flash-Lite-Model-Card.pdf) · [Gemini 3 Pro base model card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf)
