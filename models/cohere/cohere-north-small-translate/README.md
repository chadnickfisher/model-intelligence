# North Small Translate

**Creator:** Cohere · **Family:** North Translate · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-10

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Self hosted enterprise localization research (low confidence)

Purpose-built candidate, particularly listed tier-one languages. Hardware and noncommercial license substantially narrow free deployment usefulness.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: language.translation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-315d51f450cac0a4

Conditions: Not established in this pass

Failure modes / limitations: Not established in this pass

Supporting sources: [docs.cohere.com](https://docs.cohere.com/docs/north-small-translate-1.0)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Observation obs-516d65ed1c24: Purpose-built machine translation with listed tier-one languages and deployment formats.

### Language.translation (low confidence)

Vendor WMT26 evaluation supports a provisional translation candidate for its tested language set; the multi-pass agentic result is a separate workflow.

Scope: direct / conditional. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: language.translation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-0e77ffde181d61b9

Conditions: Vendor evaluation judged by GPT-5.6-Sol; reported all-language score, not an established human WMT competition rank.

Failure modes / limitations: Not established in this pass

Supporting sources: [North Small Translate](https://cohere.com/blog/north-small-translate) · [https://huggingface.co/CohereLabs/North-Small-Translate-1.0](https://huggingface.co/CohereLabs/North-Small-Translate-1.0)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence: limited exact-task evidence, vendor-heavy or unresolved configuration; scores are not confidence.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | decoder-only sparse MoE Transformer |
| parameters | total billion: 218; active billion: 25 |
| context window | 16000 |
| maximum output | 16000 |
| modalities | input: text; output: translated text |
| language support | 50 |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

2 recorded access route(s); 1 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: CC-BY-NC-4.0 for downloadable weights; commercial use requires separate authorization

Restrictions: Not established in this pass

Commercial use: Unknown / not established

Redistribution: Unknown / not established

Hosted service: Unknown / not established

Local weights/runtime availability: available

Hardware: Not established in this pass

Local conditions: Not established in this pass

## Gaps and caveats

- No independent translation-quality result verified in this pass.
- Commercial API/production pricing unknown.
- Name 'Small' does not mean laptop-size.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| cohere | Capped free evaluation / tier / current | input: 0 USD / per 1 million tokens; output: 0 USD / per 1 million tokens | Capped free evaluation; contact sales for production. | 2026-10-07 |

## Recorded access routes

- cohere / Creator Hugging Face Space: documented_not_execution_tested. Not established in this pass
- cohere / Cohere Chat V2 / V1 / Chat Completions: documented_not_execution_tested. Not established in this pass

## Sources

[docs.cohere.com](https://docs.cohere.com/docs/north-small-translate-1.0) · [North Small Translate](https://cohere.com/blog/north-small-translate) · [https://huggingface.co/CohereLabs/North-Small-Translate-1.0](https://huggingface.co/CohereLabs/North-Small-Translate-1.0)
