# GLM-5.3-Flash

**Creator:** Z.ai / Zhipu AI · **Family:** GLM5 · **Status:** active
**Verified:** 2026-10-06 · **Release:** Unknown

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Cost constrained multimodal agents (medium confidence)

Useful candidate where image-capable agents, MIT terms and lower token prices matter.

Conditions: Exact hosted vs local runtime multimodal adapters differ; profile full task latency.

Failure modes / limitations: Verbose reasoning and measured 53 tokens/sec can dominate latency; no guarantee of flagship GLM5.3 task parity.

Supporting sources: [GLM-5.3-Flash model card](https://huggingface.co/zai-org/GLM-5.3-Flash) · [GLM5.3 Flash independently profiled](https://artificialanalysis.ai/models/glm-5-3-flash) · [Z.ai pricing](https://docs.z.ai/guides/overview/pricing)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Native multimodal MoE combining sparse and linear attention with mHC |
| parameters | total billion: 320; active billion: 18; scope: creator-declared count; see notes; exact parameter count: Unknown / not established |
| context window | native tokens: 1000000; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

2 recorded access route(s); 1 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: MIT

Restrictions: Retain copyright/license notices; comply with the license.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: allowed

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Planning estimate: 192–256GB aggregate memory for supported 4-bit with modest batching; FP8 requires over 320GB weights plus headroom.; HF serialized metadata rounds to 321B; official model-card declaration is 320B.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| zai-api | standard / current | input: 0.15 USD / per_1000000_tokens; output: 0.5 USD / per_1000000_tokens; cached_input: 0.03 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Cached-input storage currently labeled limited-time free; promotional expired rates are excluded. | 2026-10-06 |

## Recorded access routes

- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Z.ai / Zhipu AI
- zai-api / hosted_api: documented route; account eligibility unverified. Not established in this pass

## Sources

[GLM5.3 Flash MIT license](https://huggingface.co/zai-org/GLM-5.3-Flash/blob/main/LICENSE) · [GLM-5.3-Flash model card](https://huggingface.co/zai-org/GLM-5.3-Flash) · [GLM5.3 Flash independently profiled](https://artificialanalysis.ai/models/glm-5-3-flash) · [Z.ai pricing](https://docs.z.ai/guides/overview/pricing) · [GLM5.3 Flash endpoint guide](https://docs.z.ai/guides/vlm/glm-5.3-flash)
