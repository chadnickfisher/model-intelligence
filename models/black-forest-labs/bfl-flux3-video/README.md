# FLUX 3 Video

**Creator:** Black Forest Labs · **Family:** FLUX · **Status:** preview
**Verified:** 2026-10-06 · **Release:** 2026-07-23

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Short audiovisual generation and keyframed continuation (low confidence)

Feature-rich candidate where synchronized sound and pinned frames matter; quality judgment remains low confidence without independent testing.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): video.generation; audio.speech_generation

Judgment ID: judgment-da95efcb747baa7e

Conditions: Not established in this pass

Failure modes / limitations: Not established in this pass

Supporting sources: [docs.bfl.ai](https://docs.bfl.ai/flux_3/flux3_overview)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Observation obs-aa0038a13410: Short audiovisual generation, pinned keyframes and continuation capabilities publicly documented.

### Video.generation (low confidence)

Vendor preferences concern a development candidate and evolving harness; quality of an exact current FLUX.3 Video production checkpoint remains unknown.

Scope: direct / unknown. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: video.generation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-bf07973843af6a72

Conditions: Preliminary 10-second 720p text-to-video with audio; vendor-run human preferences.

Failure modes / limitations: Not established in this pass

Supporting sources: [Introducing FLUX.3](https://bfl.ai/blog/flux-3)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence: limited exact-task evidence, vendor-heavy or unresolved configuration; scores are not confidence.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | Unknown / not established |
| maximum output | Unknown / not established |
| modalities | input: text; image keyframes; video continuation; output: video; synchronized audio |
| language support | Unknown / not established |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

2 recorded access route(s); 2 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: API service terms; no blanket open-source claim

Restrictions: Not established in this pass

Commercial use: Unknown / not established

Redistribution: Unknown / not established

Hosted service: Unknown / not established

Local weights/runtime availability: unknown

Hardware: Not established in this pass

Local conditions: Not established in this pass

## Gaps and caveats

- Preview can change.
- 4K classes are finished with video upsampler, not an established native-resolution quality guarantee.
- Omni Reference still marked forthcoming in reviewed docs.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| bfl | t2v/i2v full render HD / current | generation: 0.17 USD / per output second | Not established in this pass | 2026-10-06 |
| bfl | t2v/i2v full render UHD / current | generation: 0.8 USD / per output second | Not established in this pass | 2026-10-06 |

## Recorded access routes

- bfl / BFL API and Playground: documented_not_execution_tested. Not established in this pass
- together / hosted metered api: provider_listed; billing_unit_conflict_requires_verification. Not established in this pass

## Sources

[docs.bfl.ai](https://docs.bfl.ai/flux_3/flux3_overview) · [docs.bfl.ai](https://docs.bfl.ai/quick_start/pricing) · [Introducing FLUX.3](https://bfl.ai/blog/flux-3)
