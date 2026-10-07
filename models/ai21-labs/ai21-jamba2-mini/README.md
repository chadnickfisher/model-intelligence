# Jamba2 Mini

**Creator:** AI21 Labs · **Family:** Jamba · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-01-08

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Grounded extraction constrained enterprise question answering (low confidence)

Reasonable efficiency/steerability candidate from design and vendor evaluations; no current independent result established.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): knowledge.extraction; knowledge.rag

Judgment ID: judgment-fbc9e2719df53c93

Conditions: Not established in this pass

Failure modes / limitations: Not established in this pass

Supporting sources: [www.ai21.com](https://www.ai21.com/blog/introducing-jamba2/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Observation obs-15662c63b9d6: Enterprise grounding/instruction-following focus and efficient non-reasoning architecture.

### Language.instruction_following (low confidence)

Vendor instruction-heavy enterprise comparisons make Jamba2 Mini a provisional instruction-following candidate; this pass does not establish an independent success rate.

Scope: direct / conditional. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: language.instruction_following

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-d1c98668b2402aca

Conditions: Vendor blind enterprise comparisons and named IFBench/IFEval evaluations; numerical chart values were not extracted.

Failure modes / limitations: Not established in this pass

Supporting sources: [www.ai21.com](https://www.ai21.com/blog/introducing-jamba2/) · [https://huggingface.co/ai21labs/AI21-Jamba2-Mini](https://huggingface.co/ai21labs/AI21-Jamba2-Mini)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence: limited exact-task evidence, vendor-heavy or unresolved configuration; scores are not confidence.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | hybrid SSM-Transformer MoE |
| parameters | total billion: 52; active billion: 12 |
| context window | 256K tokens |
| maximum output | Unknown / not established |
| modalities | input: text; output: text |
| language support | Unknown / not established |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

2 recorded access route(s); 1 model-specific price record(s).

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

- Do not inherit context size, pricing or license from Jamba1.5/1.6.
- Not evaluated here against newer open models.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| ai21 | Standard / current | input: 0.2 USD / per 1 million tokens; output: 0.4 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |

## Recorded access routes

- ai21 / AI21 Studio Playground: documented_not_execution_tested. Not established in this pass
- ai21 / AI21 Studio: documented_not_execution_tested. Not established in this pass

## Sources

[www.ai21.com](https://www.ai21.com/blog/introducing-jamba2/) · [www.ai21.com](https://www.ai21.com/jamba/) · [https://huggingface.co/ai21labs/AI21-Jamba2-Mini](https://huggingface.co/ai21labs/AI21-Jamba2-Mini) · [https://docs.ai21.com/docs/jamba-foundation-models](https://docs.ai21.com/docs/jamba-foundation-models)
