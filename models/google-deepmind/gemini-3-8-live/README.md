# Gemini 3.8 Live

**Creator:** Google DeepMind · **Family:** Gemini · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-15

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Tool connected real time voice conversation (medium confidence)

Well-matched interface; actual speech quality, turn taking and latency need task-specific verification.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: audio.conversation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-6eac9d7c589429f2

Conditions: Not established in this pass

Failure modes / limitations: Not established in this pass

Supporting sources: [Gemini 3.8 Live API model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-live) · [Live API overview](https://ai.google.dev/gemini-api/docs/live-api)

Contradictory or limiting sources: [Gemini 3.8 Audio model card](https://deepmind.google/models/model-cards/gemini-3-8-audio/) · [Gemini 3.8 Live API model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-live)

Evidence notes: task-conditioned synthesis; no inference runs performed; Observation obs-c0b11ad9d793: Streaming voice with interleaved reasoning and default non-blocking tool calls is a suitable interface design for conversational agents.; Observation obs-d67386e9f0d6: Hallucinations/timeouts remain; migration fails if unsupported thinking_level or proactive_audio:false is sent.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Gemini 3 Pro-derived sparse MoE transformer; audio-specific changes undisclosed |
| parameters | Unknown / not established |
| context window | 131072 |
| maximum output | 65536 |
| modalities | input: text; image; audio; video; output: text; audio |
| language support | supported count: 70; scope: Live API overview; full list not transcribed; evidence ids: src-25e1e7c2305d |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

6 recorded access route(s); 1 model-specific price record(s).

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

- Independent 3.8 Live task quality and latency measurements
- Full per-language performance
- Live Avatar product-specific limits/prices not included

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| google-developer-api | paid_standard / current | text_input: 0.75 USD / per_1M_tokens; audio_input: 3 USD / per_1M_tokens; image_video_input: 1 USD / per_1M_tokens; text_output: 4.5 USD / per_1M_tokens; audio_output: 12 USD / per_1M_tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- google-ai / Gemini Live / Search Live / Workspace: Conditional consumer/client product; exact account entitlement unverified. Model family rollout documented across consumer voice surfaces. Exact base versus Extended Thinking assignment and account limits not verified.
- google-developer-api / Gemini Developer API / Google AI Studio: officially_documented_not_execution_tested. Not established in this pass
- google-cloud / Gemini Enterprise Agent Platform Live API: officially_documented_not_execution_tested. Not established in this pass
- google-developer-api / first-party-api: documented route; account eligibility unverified. Not established in this pass
- google-ai-studio / Google AI Studio: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass
- google-consumer / Gemini app / Google AI plans: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass

## Sources

[Live API overview](https://ai.google.dev/gemini-api/docs/live-api) · [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Gemini 3.8 Live API model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-live) · [Gemini API release notes](https://ai.google.dev/gemini-api/docs/changelog) · [Gemini 3.8 Audio model card](https://deepmind.google/models/model-cards/gemini-3-8-audio/) · [Gemini 3 Pro base model card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf)
