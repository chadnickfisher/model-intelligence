# Embed 5 Fast

**Creator:** Cohere · **Family:** Embed · **Status:** unknown
**Verified:** 2026-10-06 · **Release:** 2026-09-30

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### High volume interactive retrieval (medium confidence)

Candidate for query-time cost/latency savings, including Pro-index/Fast-query pairing; current comparative evidence is vendor-generated.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: context.retrieval

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-afbdc8473c5cc5bd

Conditions: Not established in this pass

Failure modes / limitations: Not established in this pass

Supporting sources: [cohere.com](https://cohere.com/blog/embed-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Observation obs-752ea46df2f7: Public evidence observation

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 128000 |
| maximum output | Unknown / not established |
| modalities | input: text; image; fused text+image; output: embedding |
| language support | 100+ |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

4 recorded access route(s); 2 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: commercial terms

Restrictions: Not established in this pass

Commercial use: Unknown / not established

Redistribution: Unknown / not established

Hosted service: Unknown / not established

Local weights/runtime availability: unknown

Hardware: Not established in this pass

Local conditions: Not established in this pass

## Gaps and caveats

- No independent latency measurements established here.
- Do not treat retrieval benchmarks as generation or reasoning scores.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| cohere | Standard / current | input: 0.08 USD / per 1 million tokens; image_input: 0.4 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |
| cohere | GA / current | input: 0.08 USD / per 1M tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- cohere / Model Vault: documented_not_execution_tested. Not established in this pass
- aws-sagemaker / dedicated compute: creator_documented; deployment-specific ID. Not established in this pass
- azure-foundry / hosted deployment: exact_partner_catalog_listing; regional_price_unverified. Not established in this pass
- cohere / Cohere Embed API: documented_not_execution_tested. Not established in this pass

## Sources

[cohere.com](https://cohere.com/blog/embed-5)
