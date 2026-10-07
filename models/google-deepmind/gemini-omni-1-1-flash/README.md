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

### Video.editing (low confidence)

Official 1.1 documentation describes scene extension and start/end-frame controls; their measured consistency and edit fidelity remain unknown for the exact 1.1 route.

Scope: direct / unknown. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: video.editing

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-af4ab0ba09892360

Conditions: Feature documentation is not an edit-quality evaluation. Generic Omni Flash comparator scores are version-gated.

Failure modes / limitations: Not established in this pass

Supporting sources: [Gemini Omni 1.1 Flash developer and subscriber access](https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-omni-1-1-flash/) · [Gemini Omni Flash API model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-omni-flash)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence: limited exact-task evidence, vendor-heavy or unresolved configuration; scores are not confidence.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

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

8 recorded access route(s); 1 model-specific price record(s).

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

- google-ai / Google Vids: Conditional consumer/client product; exact account entitlement unverified. Omni 1.1 HD generation documented at no cost for Google or Workspace account holders; precise quota not stated.
- google-ai / Google Flow: Conditional consumer/client product; exact account entitlement unverified. Omni 1.1 launch documents Plus/Pro/Ultra; Flow has its own generation-credit tariffs. Exact minor-version mapping for current generic Omni Flash credit rows remains unstated.
- google-developer-api / Gemini Developer API / Google AI Studio: officially_documented_not_execution_tested. Not established in this pass
- google-ai / Gemini app video: Conditional consumer/client product; exact account entitlement unverified. Paid Google AI plan or qualifying Workspace license, age 18+; scene extension explicitly announced for Plus/Pro/Ultra.
- google-cloud / Gemini Enterprise Agent Platform: official_preview. Not established in this pass
- google-developer-api / first-party-api: documented route; account eligibility unverified. Not established in this pass
- google-ai-studio / Google AI Studio: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass
- google-consumer / Gemini app / Google AI plans: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass

## Sources

[Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Gemini Omni Flash API model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-omni-flash) · [Gemini API release notes](https://ai.google.dev/gemini-api/docs/changelog) · [Gemini Omni 1.1 Flash developer and subscriber access](https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-omni-1-1-flash/)
