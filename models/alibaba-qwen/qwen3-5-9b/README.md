# Qwen3.5-9B

**Creator:** Alibaba / Qwen · **Family:** Qwen3.5 · **Status:** active
**Verified:** 2026-10-06 · **Release:** Unknown

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Small local visual assistant (medium confidence)

Reasonable low-memory candidate for short visual QA, extraction and bounded assistant work.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): vision.question_answering; knowledge.extraction

Judgment ID: judgment-89e9ac298c376d19

Conditions: Measure task accuracy at target image resolution and context.

Failure modes / limitations: Verbose reasoning can dominate latency; small-model factual and complex planning errors.

Supporting sources: [Qwen3.5-9B model card](https://huggingface.co/Qwen/Qwen3.5-9B) · [Qwen3.5 9B independently profiled](https://artificialanalysis.ai/models/qwen3-5-9b)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Dense hybrid Gated DeltaNet / gated attention with vision encoder |
| parameters | total billion: 9; active billion: 9; scope: 9B language model; approximately 9.7B in independent complete-model catalog.; exact parameter count: Unknown / not established |
| context window | native tokens: 262144; extended tokens: 1010000; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; video; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

1 recorded access route(s); 0 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Apache-2.0

Restrictions: Retain copyright/license notices; comply with the license.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: allowed

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Planning estimate: 8–12GB GPU or 16GB+ unified memory at 4-bit, modest context; 24GB-class memory is more comfortable for BF16.; 9B is LM count; independent catalog reports 9.7B complete parameters. Million-token mode does not fit these budgets automatically.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|

## Recorded access routes

- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Alibaba / Qwen

## Sources

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) · [Qwen3.5-9B model card](https://huggingface.co/Qwen/Qwen3.5-9B) · [Qwen3.5 9B independently profiled](https://artificialanalysis.ai/models/qwen3-5-9b)
