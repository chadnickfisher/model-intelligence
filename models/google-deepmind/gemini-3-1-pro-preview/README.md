# Gemini 3.1 Pro Preview

**Creator:** Google DeepMind · **Family:** Gemini · **Status:** preview
**Verified:** 2026-10-06 · **Release:** 2026-02-19

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Difficult science visual qa and long documents (medium confidence)

Strong QA candidate; selectively retrieve evidence rather than fill the entire context indiscriminately.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): reasoning.scientific; vision.question_answering; context.reasoning

Judgment ID: judgment-6272f2a3a37dd45c

Conditions: high; temperature 1; Google API; output 65,536; high; Google API

Failure modes / limitations: Not established in this pass

Supporting sources: [Vals AI gemini-3.1-pro-preview](https://www.vals.ai/models/google_gemini-3.1-pro-preview)

Contradictory or limiting sources: [Gemini 3.1 Pro model card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [Vals AI gemini-3.1-pro-preview](https://www.vals.ai/models/google_gemini-3.1-pro-preview)

Evidence notes: task-conditioned synthesis; no inference runs performed; Observation obs-2ee68e334fde: Strong closed-form science and multimodal QA in current Vals snapshot.; Observation obs-dc03c35a1b80: Effective long-context retrieval degrades near the advertised maximum.; Observation obs-e8f1075592de: Strong QA does not transfer uniformly to open-ended agents.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Gemini 3 Pro-derived sparse mixture-of-experts transformer; exact 3.1 modifications undisclosed |
| parameters | Unknown / not established |
| context window | 1048576 |
| maximum output | 65536 |
| modalities | input: text; image; video; audio; PDF; output: text |
| language support | Unknown / not established |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

5 recorded access route(s); 2 model-specific price record(s).

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

- Parameter counts
- Complete language list
- Exact 3.1-specific knowledge cutoff

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| google-developer-api | paid_standard / current | input: 2 USD / per_1M_tokens; output_including_thinking: 12 USD / per_1M_tokens; cache_read: 0.2 USD / per_1M_tokens | prompt <= 200,000 tokens | 2026-10-06 |
| google-developer-api | paid_standard / current | input: 4 USD / per_1M_tokens; output_including_thinking: 18 USD / per_1M_tokens; cache_read: 0.4 USD / per_1M_tokens | prompt > 200,000 tokens | 2026-10-06 |

## Recorded access routes

- google-developer-api / first-party-api: documented route; account eligibility unverified. Not established in this pass
- google-ai-studio / Google AI Studio: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass
- google-consumer / Gemini app / Google AI plans: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass
- google-antigravity / Google Antigravity: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass
- google-cli / Gemini CLI: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass

## Sources

[Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Gemini 3.1 Pro Preview API model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview) · [Gemini API release notes](https://ai.google.dev/gemini-api/docs/changelog) · [Gemini 3.1 Pro model card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [Gemini 3 Pro base model card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf)
