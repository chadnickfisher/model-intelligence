# Gemini Omni 1.1 Flash

**Creator:** Google DeepMind · **Family:** Gemini · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-08-27

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Iterative short video editing (low confidence)

Current first-party default worth evaluating, but independent quality evidence is missing in this pass.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: video.editing

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-173b944a1d1a6c4c

Conditions: Not established in this pass

Failure modes / limitations: Not established in this pass

Supporting sources: [Gemini Omni Flash API model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-omni-flash) · [Omni video guide](https://ai.google.dev/gemini-api/docs/omni)

Contradictory or limiting sources: [Omni video guide](https://ai.google.dev/gemini-api/docs/omni) · [Gemini API release notes](https://ai.google.dev/gemini-api/docs/changelog)

Evidence notes: task-conditioned synthesis; no inference runs performed; Observation obs-3386dd991c55: Conversational short-video editing and mixed inputs support an iterative workflow.; Observation obs-b46d11e01909: Some edits of uploaded videos/recognizable people are regionally restricted; 1080p/4K are upscaled.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 1048576 |
| maximum output | Unknown / not established |
| modalities | input: text; image; video; output: video; native_audio |
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

- Audio input support differs between overview/pricing and model table; not certified here
- Independent 1.1 benchmark
- Architecture/parameter counts

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| google-developer-api | paid_standard / current | input: 1.5 USD / per_1M_tokens; text_output: 9 USD / per_1M_tokens; video_output: 17.5 USD / per_1M_tokens | 720p outputs billed at 5,792 tokens/second, approximately $0.10/second; not a flat quote for every resolution. | 2026-10-06 |

## Recorded access routes

- google-developer-api / first-party-api: documented route; account eligibility unverified. Not established in this pass
- google-ai-studio / Google AI Studio: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass
- google-consumer / Gemini app / Google AI plans: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass

## Sources

[Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Gemini Omni Flash API model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-omni-flash) · [Gemini API release notes](https://ai.google.dev/gemini-api/docs/changelog)
