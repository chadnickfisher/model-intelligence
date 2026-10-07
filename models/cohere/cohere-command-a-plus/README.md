# Command A+

**Creator:** Cohere · **Family:** Command · **Status:** preview
**Verified:** 2026-10-06 · **Release:** 2026-05-20

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Private multilingual rag and enterprise agents (medium confidence)

Useful candidate where controllable deployment and abstention matter. Independent launch testing found 86% non-hallucination but only 9% knowledge accuracy; high abstention is not universal correctness.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): knowledge.rag; agent.tool_use

Judgment ID: judgment-d3d856d23e638edc

Conditions: Not established in this pass

Failure modes / limitations: Not established in this pass

Supporting sources: [artificialanalysis.ai](https://artificialanalysis.ai/articles/cohere-launches-open-weights-model-command-a-more-than-a-year-since-the-command-a-release)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Observation obs-4dd631a08c77: Public evidence observation

### Hard scientific reasoning agentic coding (medium confidence)

Launch testing showed gaps on hardest tasks; do not infer frontier quality from hardware efficiency.

Scope: compound / warning. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): reasoning.scientific; coding.repository_work

Judgment ID: judgment-9e8f4c9fa81f59ba

Conditions: Not established in this pass

Failure modes / limitations: Not established in this pass

Supporting sources: [artificialanalysis.ai](https://artificialanalysis.ai/articles/cohere-launches-open-weights-model-command-a-more-than-a-year-since-the-command-a-release)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Observation obs-4dd631a08c77: Public evidence observation

### Research.fact_check (low confidence)

Independent launch testing reports high abstention/non-hallucination alongside low factual accuracy. Abstaining safely does not establish reliable factual answers.

Scope: direct / warning. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: research.fact_check

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-f2ef16690b3303d9

Conditions: Pre-release AA-Omniscience evaluation; non-hallucination and accuracy are distinct metrics.

Failure modes / limitations: Low measured factual accuracy in this evaluation; do not interpret abstention as knowledge.

Supporting sources: [artificialanalysis.ai](https://artificialanalysis.ai/articles/cohere-launches-open-weights-model-command-a-more-than-a-year-since-the-command-a-release) · [docs.cohere.com](https://docs.cohere.com/docs/command-a-plus)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence in current generalization: one independent pre-release evaluation, uncertain later serving revision.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

### Measured generation behavior (medium confidence)

Public evidence observation Measurements: {"output_tokens_per_second": 281}. These describe the cited benchmark configuration only.

Scope: performance / conditional. Cost, deployment or throughput observation; not a task capability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-9404c729731567f2

Conditions: Not established in this pass

Failure modes / limitations: Not established in this pass

Supporting sources: [artificialanalysis.ai](https://artificialanalysis.ai/articles/cohere-launches-open-weights-model-command-a-more-than-a-year-since-the-command-a-release)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Launch/pre-release testing; older index revision and comparison set. Abstention can drive non-hallucination result.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | sparse Mixture-of-Experts |
| parameters | total billion: 218; active billion: 25 |
| context window | 128000 |
| maximum output | 64000 |
| modalities | input: text; image; output: text |
| language support | 48 |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

3 recorded access route(s); 1 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Apache-2.0

Restrictions: Not established in this pass

Commercial use: Unknown / not established

Redistribution: Unknown / not established

Hosted service: Unknown / not established

Local weights/runtime availability: available

Hardware: Not established in this pass

Local conditions: Not established in this pass

## Gaps and caveats

- API free-trial limits differ from paid production Model Vault.
- Launch benchmark scores are dated and not comparable with current index revisions without normalization.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| cohere | Capped free evaluation / tier / current | input: 0 USD / per 1 million tokens; output: 0 USD / per 1 million tokens | Free capped evaluation; production-key label alone does not remove newer-model restrictions. | 2026-10-07 |

## Recorded access routes

- azure-foundry / hosted deployment: creator_catalog_lists_partner_model; provider_price_unverified. Not established in this pass
- cohere / Model Vault: documented_not_execution_tested. Not established in this pass
- cohere / hosted evaluation api: documented_not_execution_tested. Not established in this pass

## Sources

[docs.cohere.com](https://docs.cohere.com/docs/command-a-plus) · [artificialanalysis.ai](https://artificialanalysis.ai/articles/cohere-launches-open-weights-model-command-a-more-than-a-year-since-the-command-a-release) · [Command A+ release notes](https://docs.cohere.com/v1/changelog/command-a-plus-05-2026)
