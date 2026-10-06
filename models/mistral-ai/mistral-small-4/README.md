# Mistral Small 4 119B

**Creator:** Mistral AI · **Family:** Mistral Small · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-03-16

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Latency sensitive enterprise assistant (medium confidence)

Useful candidate for concise multilingual extraction, tool use and mixed chat/reasoning.

Conditions: Toggle none/high reasoning per request and compare end-to-end success.

Failure modes / limitations: Creator broad best-in-class claims are not established by independent task-matched evidence; quantization and cache memory matter.

Supporting sources: [Mistral Small 4 119B model card](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) · [Mistral Small4 reasoning independently profiled](https://artificialanalysis.ai/models/mistral-small-4)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

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

2 recorded access route(s); 1 model-specific price record(s).

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
| mistral-api | standard / current | input: 0.15 USD / per_1000000_tokens; output: 0.6 USD / per_1000000_tokens; cached_input: 0.015 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Default standard tier; regional inference, batch and priority may have different rates. | 2026-10-06 |

## Recorded access routes

- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Mistral AI
- mistral-api / hosted_api: documented route; account eligibility unverified. Not established in this pass

## Sources

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) · [Mistral Small 4 119B model card](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) · [Mistral Small4 reasoning independently profiled](https://artificialanalysis.ai/models/mistral-small-4)
