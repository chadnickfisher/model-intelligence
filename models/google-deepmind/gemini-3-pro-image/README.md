# Nano Banana Pro / Gemini 3 Pro Image

**Creator:** Google DeepMind · **Family:** Gemini · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-05-28

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Visual concepts mockups and text heavy image drafts (medium confidence)

Good candidate for reviewed design work; do not use output as faithful forensic restoration.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: image.generation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-a8b91a879079b15e

Conditions: December 2025 Nano Banana Pro version

Failure modes / limitations: Not established in this pass

Supporting sources: [Nano Banana Pro API model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image) · [Gemini image generation guide](https://ai.google.dev/gemini-api/docs/image-generation) · [Is Nano Banana Pro a Low-Level Vision All-Rounder?](https://arxiv.org/abs/2512.15110)

Contradictory or limiting sources: [Is Nano Banana Pro a Low-Level Vision All-Rounder?](https://arxiv.org/abs/2512.15110)

Evidence notes: task-conditioned synthesis; no inference runs performed; Observation obs-bbe38314fda9: Grounded image creation and text/layout control are supported; results require review.; Observation obs-c3991e29aaff: Independent low-level vision study found attractive reconstructed detail but lower reference-based fidelity than specialists.

### Image.editing (low confidence)

Vendor human comparisons support an editing candidate with Search On. Search-assisted preference scores do not guarantee faithful text edits or factual images.

Scope: direct / conditional. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: image.editing

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-231a8488cc54a31b

Conditions: Gemini 3 Pro Image with Search On; curated human pairwise preference evaluation.

Failure modes / limitations: Not established in this pass

Supporting sources: [Gemini 3 Pro Image model card](https://deepmind.google/models/model-cards/gemini-3-pro-image/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence: limited exact-task evidence, vendor-heavy or unresolved configuration; scores are not confidence.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 65536 |
| maximum output | 32768 |
| modalities | input: text; image; output: text; image |
| language support | recommended: EN; ar-EG; de-DE; es-MX; fr-FR; hi-IN; id-ID; it-IT; ja-JP; ko-KR; pt-BR; ru-RU; ua-UA; vi-VN; zh-CN; note: Locale strings copied as documented; recommendation is not an exhaustive support guarantee.; evidence ids: src-5d0514efd100 |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

6 recorded access route(s); 2 model-specific price record(s).

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

- Flex/Priority availability: pricing page lists rates but model capability page says unsupported.
- Current model-card token-limit reconciliation

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| google-developer-api | paid_standard / current | input_text_image: 2 USD / per_1M_tokens; output_text_thinking: 12 USD / per_1M_tokens; output_image: 120 USD / per_1M_tokens | Not established in this pass | 2026-10-06 |
| google-developer-api | paid_standard / current | 1K_or_2K: 0.134 USD / per_output_image; 4K: 0.24 USD / per_output_image | Published rounded equivalents; input and thinking/text charges additional. | 2026-10-06 |

## Recorded access routes

- google-ai / Gemini app Nano Banana Pro redo: Conditional consumer/client product; exact account entitlement unverified. Nano Banana Pro redo is listed for AI Plus/Pro/Ultra, not without an AI plan. App quotas differ from API; no free API tier.
- google-cloud / Gemini Enterprise Agent Platform: officially_documented_not_execution_tested. Not established in this pass
- google-developer-api / Gemini Developer API / Google AI Studio: officially_documented_not_execution_tested. Not established in this pass
- google-developer-api / first-party-api: documented route; account eligibility unverified. Not established in this pass
- google-ai-studio / Google AI Studio: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass
- google-consumer / Gemini app / Google AI plans: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass

## Sources

[Gemini image generation guide](https://ai.google.dev/gemini-api/docs/image-generation) · [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Nano Banana Pro API model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image) · [Gemini API release notes](https://ai.google.dev/gemini-api/docs/changelog) · [Gemini 3 Pro Image model card](https://deepmind.google/models/model-cards/gemini-3-pro-image/) · [Gemini 3 Pro base model card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf) · [Gemini Developer API pricing](https://ai.google.dev/gemini-api/docs/pricing)
