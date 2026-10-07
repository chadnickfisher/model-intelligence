# Mistral Small 4 119B

**Creator:** Mistral AI · **Family:** Mistral Small · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-03-16

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Latency sensitive enterprise assistant (medium confidence)

Useful candidate for concise multilingual extraction, tool use and mixed chat/reasoning.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): knowledge.extraction; agent.tool_use; language.multilingual_chat

Judgment ID: judgment-c17556d4544c4c48

Conditions: Toggle none/high reasoning per request and compare end-to-end success.

Failure modes / limitations: Creator broad best-in-class claims are not established by independent task-matched evidence; quantization and cache memory matter.

Supporting sources: [Mistral Small 4 119B model card](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) · [Mistral Small4 reasoning independently profiled](https://artificialanalysis.ai/models/mistral-small-4)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Context.reasoning (low confidence)

Vendor AA-LCR evidence supports a provisional long-context reasoning candidate when reasoning is enabled; the result does not transfer automatically to reasoning off.

Scope: direct / conditional. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: context.reasoning

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-9a65dee264bffeda

Conditions: Reasoning enabled; recommended reasoning_effort high does not establish the exact measured setting.

Failure modes / limitations: Not established in this pass

Supporting sources: [Mistral Small 4 119B model card](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence: limited exact-task evidence, vendor-heavy or unresolved configuration; scores are not confidence.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | MoE 128 experts, four active; integrated instruction/reasoning/code modes |
| parameters | total billion: 119; active billion: 6.5; scope: creator-declared count; see notes; exact parameter count: Unknown / not established |
| context window | native tokens: 262144; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

5 recorded access route(s); 3 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Apache-2.0

Restrictions: Retain copyright/license notices; comply with the license.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: allowed

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Planning estimate: 80GB-class aggregate memory with 4-bit/NVFP4, moderate context; FP8 approximately 119GB weights before overhead.; Vendor supplies FP8, NVFP4 and EAGLE acceleration options.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| openrouter | Standard / current | input: 0.15 USD / per 1 million tokens; output: 0.6 USD / per 1 million tokens | Gateway-listed base rate; provider routing/regional variants and credit-purchase fees separate. | 2026-10-07 |
| mistral-api | Standard / current | input: 0.15 USD / per 1 million tokens; output: 0.6 USD / per 1 million tokens; cached_input: 0.015 USD / per 1 million tokens | Rates are standard. Batch/priority/regional tiers distinct; do not infer a default account tier. | 2026-10-07 |
| mistral-api | standard / historical | input: 0.15 USD / per_1000000_tokens; output: 0.6 USD / per_1000000_tokens; cached_input: 0.015 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Default standard tier; regional inference, batch and priority may have different rates. | 2026-10-06 |

## Recorded access routes

- mistral-api / Mistral plan included API usage: documented_not_execution_tested. Not established in this pass
- mistral-api / Mistral API Standard: documented_not_execution_tested. Not established in this pass
- openrouter / gateway metered api: documented_not_execution_tested. Not established in this pass
- mistral-api / hosted_api: documented route; account eligibility unverified. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Mistral AI

## Sources

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) · [Mistral Small 4 119B model card](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) · [Mistral Small4 reasoning independently profiled](https://artificialanalysis.ai/models/mistral-small-4)
