# Lyria 3.5

**Creator:** Google DeepMind · **Family:** Lyria · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-03

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Prompted full song concept drafts (low confidence)

Promising from official feature evidence; comparative quality confidence remains low.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: music.generation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-81c45f869d24d386

Conditions: Not established in this pass

Failure modes / limitations: Not established in this pass

Supporting sources: [Generate music with Lyria 3.5](https://ai.google.dev/gemini-api/docs/music-generation) · [Lyria 3.5 model card](https://deepmind.google/models/model-cards/lyria-3-5/)

Contradictory or limiting sources: [Generate music with Lyria 3.5](https://ai.google.dev/gemini-api/docs/music-generation)

Evidence notes: task-conditioned synthesis; no inference runs performed; Observation obs-d42491a5f0c8: Full songs include prompted verses, choruses, bridges and lyrics; developer guidance supports structural prompts.; Observation obs-62a4e6b29fd2: Google reports improved audio fidelity and lyric-prompt adherence versus Lyria 2.; Observation obs-4bde1c37710c: Single-turn generation, variable duration/output, blocked artist-voice/copyrighted-lyric prompts and SynthID watermark constrain workflows.

### Music.generation (low confidence)

Vendor music-expert evaluations report improved fidelity and lyric prompt adherence over Lyria 2; this is qualitative evidence, without an independently established error rate.

Scope: direct / conditional. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: music.generation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-d0a9599027c859f7

Conditions: July 2026 model card; curated in/out-of-distribution music prompts and music experts.

Failure modes / limitations: Not established in this pass

Supporting sources: [Lyria 3.5 model card](https://deepmind.google/models/model-cards/lyria-3-5/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence: limited exact-task evidence, vendor-heavy or unresolved configuration; scores are not confidence.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Latent diffusion over temporal audio latents |
| parameters | Unknown / not established |
| context window | 131072 |
| maximum output | Unknown / not established |
| modalities | input: text; image; output: audio_MP3; lyrics_text |
| language support | Unknown / not established |

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

- Hard maximum duration
- Complete lyric language list
- Independent current-version quality benchmark
- Earliest product release: card predates API GA

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| google-developer-api | paid_standard / current | full_song: 0.08 USD / per_song_request | Not established in this pass | 2026-10-06 |

## Recorded access routes

- google-cloud / Gemini Enterprise Agent Platform: exact_model_route_unverified. Not established in this pass
- google-developer-api / Gemini Developer API / Google AI Studio: officially_documented_not_execution_tested. Not established in this pass
- google-ai / Gemini app / Flow Music / Google Vids: Conditional consumer/client product; exact account entitlement unverified. Lyria 3.5 explicitly documented for all users globally in Gemini web/mobile; Flow Music, AI Studio and Vids also named. No fixed generation count verified.
- google-developer-api / first-party-api: documented route; account eligibility unverified. Not established in this pass
- google-ai-studio / Google AI Studio: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass
- google-consumer / Gemini app / Google AI plans: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass

## Sources

[Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Lyria 3.5 API model documentation](https://ai.google.dev/gemini-api/docs/models/lyria-3.5) · [Gemini API release notes](https://ai.google.dev/gemini-api/docs/changelog) · [Lyria 3.5 model card](https://deepmind.google/models/model-cards/lyria-3-5/) · [Generate music with Lyria 3.5](https://ai.google.dev/gemini-api/docs/music-generation)
