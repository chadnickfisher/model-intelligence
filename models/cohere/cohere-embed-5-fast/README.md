# Embed 5 Fast

**Creator:** Cohere · **Family:** Embed · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-30

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### High volume interactive retrieval (low confidence)

Candidate for query-time cost/latency savings, including Pro-index/Fast-query pairing; current comparative evidence is vendor-generated.

Scope: direct / conditional. Rubric 1.1 maps corpus retrieval to knowledge.retrieval. The stable ID, original conclusion and evidence remain; confidence is lowered because cost/latency transfer still relies on vendor evidence.

Direct task IDs: knowledge.retrieval

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-afbdc8473c5cc5bd

Conditions: Not established in this pass

Failure modes / limitations: Not established in this pass

Supporting sources: [Introducing Embed 5](https://cohere.com/blog/embed-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Observation obs-752ea46df2f7: Public evidence observation; Pilot reassessment: no independent exact-setup latency evidence inspected; the independent corpus study measures retrieval quality, not query-time savings. Earlier confidence remains in history.

### Knowledge.retrieval (low confidence)

Vendor ViDoRe V3 results support ranking a fixed candidate set of parsed documents; first-stage retrieval recall over a full index remains unknown.

Scope: direct / conditional. Rubric 1.1 maps external-corpus retrieval and candidate ranking to knowledge.retrieval. Stable judgment ID, original conclusion, confidence and evidence are preserved.

Direct task IDs: knowledge.retrieval

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-7e21faf82ca7635e

Conditions: RCP-nDCG@10 reranks fixed candidates; parsed text from eight ViDoRe V3 domains, not full-index recall.

Failure modes / limitations: This candidate-ranking result cannot establish full-index recall or all-language superiority.

Supporting sources: [Introducing Embed 5](https://cohere.com/blog/embed-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence: limited exact-task evidence, vendor-heavy or unresolved configuration; scores are not confidence.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

### Knowledge.retrieval (low confidence)

An independent short-passage corpus study supports retrieval under its recorded query/document configuration; incomplete labels and unpinned hosted weights limit transfer.

Scope: direct / conditional. The measured workload fits this task; conclusion is limited to the recorded setup.

Direct task IDs: knowledge.retrieval

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-cbfb9b59385271d6

Conditions: Cosine retrieval; search_query/search_document roles; 2048 dimensions; no reranking or generated answers.

Failure modes / limitations: Long-document, multilingual, multimodal and full RAG quality are not established by this setup.

Supporting sources: [AIMultiple original embedding retrieval evaluation](https://aimultiple.com/embedding-models)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence reflects setup breadth, identity uncertainty and source limitations, not the score. No contradictory result located in this bounded pass does not establish agreement.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 128000 |
| maximum output | embedding dimensions: 256; 512; 768; 1024; 1536; 2048 |
| modalities | input: text; image; fused text+image; output: embedding |
| language support | 100+ |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

4 recorded access route(s); 6 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: commercial terms

Restrictions: Trial keys cannot be used for production/commercial workloads. Production and private deployment rights depend on the applicable agreement.; Marketplace terms permit customer applications subject to restrictions; no unrestricted redistribution or modification right established.

Commercial use: Unknown / not established

Redistribution: Unknown / not established

Hosted service: Unknown / not established

Local weights/runtime availability: available

Hardware: Not established in this pass

Local conditions: Licensed private infrastructure/self-hosting described by creator; public weights, minimum VRAM and fine-tuning rights not established.

## Gaps and caveats

- No independent latency measurements established here.
- Do not treat retrieval benchmarks as generation or reasoning scores.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| cohere | Standard / current | input: 0.08 USD / per 1 million tokens; image_input: 0.4 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |
| cohere | GA / current | input: 0.08 USD / per 1M tokens | Not established in this pass | 2026-10-06 |
| aws-sagemaker | ml.g5.xlarge / current | software_host: 2.39 USD / per instance hour | AWS Marketplace listing; exact selected instance; software plus separately billed infrastructure. | 2026-10-07 |
| aws-sagemaker | ml.p5.4xlarge / current | software_host: 3.36 USD / per instance hour | AWS Marketplace listing; exact selected instance; software plus separately billed infrastructure. | 2026-10-07 |
| cohere | Small / current | capacity_hour: 3 USD / per instance hour; capacity_month: 2000 USD / per instance month; capacity_year: 20000 USD / per instance year | Cohere-managed dedicated capacity; Fixed/Flex agreement and sizing apply; no per-token equivalence. | 2026-10-07 |
| cohere | Medium / current | capacity_hour: 5 USD / per instance hour; capacity_month: 3250 USD / per instance month; capacity_year: 32500 USD / per instance year | Cohere-managed dedicated capacity; Fixed/Flex agreement and sizing apply; no per-token equivalence. | 2026-10-07 |

## Recorded access routes

- cohere / Model Vault: documented_not_execution_tested. Not established in this pass
- aws-sagemaker / Cohere Embed v5 Fast on Amazon SageMaker: exact_fast_marketplace_listing; deployment-specific endpoint. Not established in this pass
- azure-foundry / hosted deployment: exact_partner_catalog_listing; regional_price_unverified. Not established in this pass
- cohere / Cohere Embed API: documented_not_execution_tested. Trial keys are not for production/commercial use; production access requires organization-owner approval application.

## Sources

[Introducing Embed 5](https://cohere.com/blog/embed-5)
