# Embed 5 Pro

**Creator:** Cohere · **Family:** Embed · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-30

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Complex document retrieval offline indexing (low confidence)

Promising quality-focused retrieval option based on vendor tests; independent reproduction not verified.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: knowledge.retrieval

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-0e6e2979fb965898

Conditions: Not established in this pass

Failure modes / limitations: Not established in this pass

Supporting sources: [Introducing Embed 5](https://cohere.com/blog/embed-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Observation obs-752ea46df2f7: Public evidence observation; Vendor evidence concerns ranking external candidates. Exact first-stage recall and independent reproduction remain unresolved; vendor-heavy evidence limits confidence.

### Knowledge.retrieval (low confidence)

Vendor ViDoRe V3 results support ranking a fixed candidate set of parsed documents; first-stage retrieval recall over a full index remains unknown.

Scope: direct / conditional. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: knowledge.retrieval

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-d02c0c4f21657798

Conditions: RCP-nDCG@10 reranks fixed candidates; parsed text from eight ViDoRe V3 domains, not full-index recall.

Failure modes / limitations: This candidate-ranking result cannot establish full-index recall or all-language superiority.

Supporting sources: [Introducing Embed 5](https://cohere.com/blog/embed-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence: limited exact-task evidence, vendor-heavy or unresolved configuration; scores are not confidence.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.; Vendor evidence concerns ranking external candidates. Exact first-stage recall and independent reproduction remain unresolved; vendor-heavy evidence limits confidence.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 128000 |
| maximum output | embedding dimensions: 256; 512; 768; 1024; 1536; 2048; default dimensions: 2048 |
| modalities | input: text; image; fused text+image; output: embedding |
| language support | 100+ |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

4 recorded access route(s); 4 model-specific price record(s).

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

- Retrieval ranking quality is corpus-dependent.
- API alias not confirmed.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| cohere | Standard / current | input: 0.12 USD / per 1 million tokens; image_input: 0.4 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |
| cohere | GA / current | input: 0.12 USD / per 1M tokens | Not established in this pass | 2026-10-06 |
| cohere | Small / current | capacity_hour: 3 USD / per instance hour; capacity_month: 2000 USD / per instance month | Cohere-managed dedicated capacity; Fixed/Flex agreements and instance sizing apply. Annual quotes not extracted. No per-token equivalence. | 2026-10-07 |
| cohere | Medium / current | capacity_hour: 5 USD / per instance hour; capacity_month: 3250 USD / per instance month | Cohere-managed dedicated capacity; Fixed/Flex agreements and instance sizing apply. Annual quotes not extracted. No per-token equivalence. | 2026-10-07 |

## Recorded access routes

- aws-sagemaker / dedicated compute: creator_documented; deployment-specific ID. Not established in this pass
- azure-foundry / hosted deployment: exact_partner_catalog_listing; regional_price_unverified. Not established in this pass
- cohere / Model Vault: documented_not_execution_tested. Not established in this pass
- cohere / Cohere Embed API: documented_not_execution_tested. Not established in this pass

## Sources

[Introducing Embed 5](https://cohere.com/blog/embed-5) · [https://docs.cohere.com/docs/cohere-embed](https://docs.cohere.com/docs/cohere-embed)
