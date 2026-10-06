# Gemma 4 family (31B IT representative)

**Creator:** Google DeepMind · **Family:** Gemma · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-03-31

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Locally controlled multimodal coding assistant (medium confidence)

Useful open-weight candidate when deployment control matters; select variant against memory and quality requirements.

Conditions: instruction-tuned; provider evaluation; reasoning; different weights and reasoning configurations

Failure modes / limitations: Not established in this pass

Supporting sources: [Google Gemma 4 31B instruction-tuned weights](https://huggingface.co/google/gemma-4-31B-it) · [Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4)

Contradictory or limiting sources: [Artificial Analysis gemma-4-31b](https://artificialanalysis.ai/models/gemma-4-31b) · [Gemma 4 configuration comparison](https://artificialanalysis.ai/models/comparisons/gemma-4-26b-a4b-vs-gemma-4-31b-non-reasoning)

Evidence notes: task-conditioned synthesis; no inference runs performed; Observation obs-277108d396be: Open downloadable weights and Apache 2.0 allow controlled deployment and tuning.; Observation obs-984e3b3ac410: Provider evaluates 31B IT as capable in coding and visual reasoning; smaller variants trade quality for resources.; Observation obs-fcfd1534c8b5: Independent hosted 31B reasoning throughput is substantially lower than the Flash services measured here.; Observation obs-cdfc4938876f: Independent configuration-specific results show model size and thinking mode do not create a simple ranking.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Dense decoder transformer with alternating local/global attention |
| parameters | total: 30700000000; active: Unknown / not established |
| context window | 262144 |
| maximum output | Unknown / not established |
| modalities | input: text; image; video_frames; output: text |
| language support | out of box: 35+; pretraining: 140+; evidence ids: src-fc87bfb1eae7 |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

2 recorded access route(s); 1 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Apache-2.0

Restrictions: Not established in this pass

Commercial use: Unknown / not established

Redistribution: Unknown / not established

Hosted service: Unknown / not established

Local weights/runtime availability: available

Hardware: Not established in this pass

Local conditions: Not established in this pass

## Gaps and caveats

- Host-specific maximum output limit
- Actual self-hosting RAM/VRAM, quantization effects and total cost
- Exact local workload performance

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| google-developer-api | free / current | input: 0 USD / per_1M_tokens; output: 0 USD / per_1M_tokens | Gemma 4 pricing section; paid tier unavailable. Quota limited, data-use terms differ from paid Gemini API. | 2026-10-06 |

## Recorded access routes

- google-developer-api / first-party-api: documented route; account eligibility unverified. Not established in this pass
- google-ai-studio / Google AI Studio: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass

## Sources

[Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4) · [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Gemma releases](https://ai.google.dev/gemma/docs/releases) · [Gemini API release notes](https://ai.google.dev/gemini-api/docs/changelog) · [Google Gemma 4 31B instruction-tuned weights](https://huggingface.co/google/gemma-4-31B-it) · [Gemma 4 31B IT config.json](https://huggingface.co/google/gemma-4-31B-it/raw/main/config.json)
