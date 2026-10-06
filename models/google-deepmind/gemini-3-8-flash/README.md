# Gemini 3.8 Flash

**Creator:** Google DeepMind · **Family:** Gemini · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-02

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Fast multimodal assistant and bounded coding tasks (medium confidence)

Strong candidate when throughput matters and outputs can be tested.

Conditions: high reasoning; Google API; high; temperature 1; Google API; max output 65,536; high; Google API

Failure modes / limitations: Not established in this pass

Supporting sources: [Artificial Analysis gemini-3-8-flash](https://artificialanalysis.ai/models/gemini-3-8-flash) · [Vals AI gemini-3.8-flash](https://www.vals.ai/models/google_gemini-3.8-flash)

Contradictory or limiting sources: [Gemini 3.8 Flash model card](https://deepmind.google/models/model-cards/gemini-3-8-flash/) · [Vals AI gemini-3.8-flash](https://www.vals.ai/models/google_gemini-3.8-flash)

Evidence notes: task-conditioned synthesis; no inference runs performed; Observation obs-62d94da56cdb: Fast streamed decoding in the observed benchmark service.; Observation obs-7445edb36893: Competitive contained coding tasks, with much weaker results on harder general terminal work.; Observation obs-a6b7a76a516c: Supports demanding visual/scientific question answering in independent evaluation.; Observation obs-623d3b669e5c: Provider discloses hallucinations, occasional timeouts, and increased tokens at higher effort; multilingual safety regressed versus 3.7.

### Unsupervised long horizon terminal execution (medium confidence)

Conditional; use tests and checkpointing rather than assuming benchmark coding strength transfers.

Conditions: high; temperature 1; Google API; max output 65,536

Failure modes / limitations: Not established in this pass

Supporting sources: [Vals AI gemini-3.8-flash](https://www.vals.ai/models/google_gemini-3.8-flash)

Contradictory or limiting sources: [Vals AI gemini-3.8-flash](https://www.vals.ai/models/google_gemini-3.8-flash) · [Gemini 3.8 Flash model card](https://deepmind.google/models/model-cards/gemini-3-8-flash/)

Evidence notes: task-conditioned synthesis; no inference runs performed; Observation obs-7445edb36893: Competitive contained coding tasks, with much weaker results on harder general terminal work.; Observation obs-623d3b669e5c: Provider discloses hallucinations, occasional timeouts, and increased tokens at higher effort; multilingual safety regressed versus 3.7.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 1048576 |
| maximum output | 65536 |
| modalities | input: text; image; video; audio; PDF; output: text |
| language support | Unknown / not established |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

4 recorded access route(s); 3 model-specific price record(s).

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

- Full language coverage list
- Architecture beyond published dependency
- Private production latency/SLAs

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| google-developer-api | paid_standard / current | input: 0.75 USD / per_1M_tokens; output_including_thinking: 3.75 USD / per_1M_tokens; cache_read: 0.075 USD / per_1M_tokens | Not established in this pass | 2026-10-06 |
| google-developer-api | paid_standard / current | input: 1.5 USD / per_1M_tokens; output_including_thinking: 7.5 USD / per_1M_tokens; cache_read: 0.15 USD / per_1M_tokens | Not established in this pass | 2026-10-06 |
| google-developer-api | paid_batch / current | input: 0.375 USD / per_1M_tokens; output_including_thinking: 1.875 USD / per_1M_tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- google-developer-api / first-party-api: documented route; account eligibility unverified. Not established in this pass
- google-ai-studio / Google AI Studio: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass
- google-consumer / Gemini app / Google AI plans: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass
- google-antigravity / Google Antigravity: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass

## Sources

[Gemini 3.8 Flash model card](https://deepmind.google/models/model-cards/gemini-3-8-flash/) · [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Gemini 3.8 Flash API model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash) · [Gemini API release notes](https://ai.google.dev/gemini-api/docs/changelog)
