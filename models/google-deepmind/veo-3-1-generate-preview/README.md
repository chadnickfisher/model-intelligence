# Veo 3.1

**Creator:** Google DeepMind · **Family:** Veo · **Status:** preview
**Verified:** 2026-10-06 · **Release:** 2025-10-15

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Directed short shots requiring first last frame or extensions (low confidence)

Useful specialist option; test Omni too for new general video workflows.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: video.generation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-f36c958097d5b875

Conditions: Not established in this pass

Failure modes / limitations: Not established in this pass

Supporting sources: [Generate videos with Veo 3.1 in Gemini API](https://ai.google.dev/gemini-api/docs/veo) · [Veo 3.1 API model documentation](https://ai.google.dev/gemini-api/docs/models/veo-3.1-generate-preview)

Contradictory or limiting sources: [Generate videos with Veo 3.1 in Gemini API](https://ai.google.dev/gemini-api/docs/veo) · [Video generation in the Gemini API](https://ai.google.dev/gemini-api/docs/video)

Evidence notes: task-conditioned synthesis; no inference runs performed; Observation obs-a1dcd03b9809: Native audio, frame controls, reference images and extension fit directed short cinematic shots.; Observation obs-7d1f6921bea0: Multi-video reasoning unsupported; non-English unevaluated; audio processing/safety blocks and variable latency occur.; Observation obs-6dfa41ffcfec: Google now recommends Omni as default video option, reserving Veo for particular controls/legacy integration.; Confidence limited by vendor-heavy task evidence and missing exact-task independent replication; documented interface support alone is not task quality.

### Video.generation (low confidence)

The preview route documents video generation, but exact-route measured detail accuracy remains unresolved. Located Fast-model distortion reports do not establish failure of the standard model.

Scope: direct / unknown. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: video.generation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-a39ac31ce68709f0

Conditions: Standard generate-preview identity; Fast sibling tests and unpinned consumer-surface comparisons excluded.

Failure modes / limitations: Not established in this pass

Supporting sources: [Veo 3.1 API model documentation](https://ai.google.dev/gemini-api/docs/models/veo-3.1-generate-preview) · [Veo detail-accuracy question and support reply](https://discuss.ai.google.dev/t/query-differences-in-details-of-decoration-between-veo-3-1-generate-preview-and-veo-3-1-fast-preview/108272)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence: limited exact-task evidence, vendor-heavy or unresolved configuration; scores are not confidence.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

### Measured generation behavior (medium confidence)

Multi-video reasoning unsupported; non-English unevaluated; audio processing/safety blocks and variable latency occur. Measurements: {"published_latency_min_seconds": 11, "published_latency_max_seconds": 360}. These describe the cited benchmark configuration only.

Scope: performance / conditional. Cost, deployment or throughput observation; not a task capability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-8e62e348ffe18201

Conditions: Not established in this pass

Failure modes / limitations: Not established in this pass

Supporting sources: [Generate videos with Veo 3.1 in Gemini API](https://ai.google.dev/gemini-api/docs/veo)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Published range during peak periods, not independently measured or guaranteed.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 1024 |
| maximum output | videos per request: 1 |
| modalities | input: text; image; prior_generated_video_for_extension; output: video; synchronized_audio |
| language support | fully supported: English; other languages: not evaluated; may work with variable results; evidence ids: src-6fab7b07e4f3 |

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


## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| google-developer-api | paid_standard / current | 720p_or_1080p_audio_video: 0.4 USD / per_successful_output_second; 4K_audio_video: 0.6 USD / per_successful_output_second | Not established in this pass | 2026-10-06 |

## Recorded access routes

- google-cloud / Gemini Enterprise Agent Platform Veo 3.1: related_GA_route_exact_preview_identity_not_equivalent. Not established in this pass
- google-ai / Google Flow Veo 3.1 Quality: Conditional consumer/client product; exact account entitlement unverified. Veo 3.1 Quality: 100 credits/generation for 8s videos or Extend, all users; Fast/Lite have separate costs.
- google-ai / Gemini app video: Conditional consumer/client product; exact account entitlement unverified. Current help names Gemini Omni, so a present Veo 3.1 entitlement in this app is not established.
- google-developer-api / Gemini Developer API / Google AI Studio: officially_documented_not_execution_tested. Not established in this pass
- google-developer-api / first-party-api: documented route; account eligibility unverified. Not established in this pass
- google-ai-studio / Google AI Studio: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass

## Sources

[Generate videos with Veo 3.1 in Gemini API](https://ai.google.dev/gemini-api/docs/veo) · [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Veo 3.1 API model documentation](https://ai.google.dev/gemini-api/docs/models/veo-3.1-generate-preview) · [Gemini API release notes](https://ai.google.dev/gemini-api/docs/changelog) · [Veo detail-accuracy question and support reply](https://discuss.ai.google.dev/t/query-differences-in-details-of-decoration-between-veo-3-1-generate-preview-and-veo-3-1-fast-preview/108272)
