# MiniMax M3

**Creator:** MiniMax · **Family:** MiniMax M · **Status:** active
**Verified:** 2026-10-06 · **Release:** Unknown

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Multimodal long context work (medium confidence)

A candidate for cost-sensitive image/video coding and work agents; compare using the >512k price band when relevant.

Conditions: Thinking can be enabled, adaptive or disabled; paid hosting terms are separate from weight license.

Failure modes / limitations: Long-context requests cost more; reported attention speedups are creator comparisons against M2, not universal application speedups.

Supporting sources: [MiniMax M3 model card](https://huggingface.co/MiniMaxAI/MiniMax-M3) · [MiniMax M3 independently profiled](https://artificialanalysis.ai/models/minimax-m3) · [MiniMax API pricing](https://platform.minimax.io/docs/pricing/overview)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Native multimodal MoE with MiniMax Sparse Attention |
| parameters | total billion: 428; active billion: 23; scope: creator-declared count; see notes; exact parameter count: Unknown / not established |
| context window | native tokens: 1000000; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; video; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

2 recorded access route(s); 5 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: MiniMax Community License

Restrictions: Retain copyright and permission notices.; Commercial use: branding plus one-time notice; >$20M yearly product/service revenue requires prior written authorization.; Prohibited-use appendix applies, including any military use.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: conditional

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Datacenter / high-memory workstation: ideal 4-bit roughly 214GB; plan >=256GB aggregate memory plus workload headroom.; Card ~428B versus HF serialized 427B and alternate MXFP8 artifact ~440B; scope/rounding differs. Supported quantized backend required.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| minimax-api | standard_short / current | input: 0.3 USD / per_1000000_tokens; output: 1.2 USD / per_1000000_tokens; cached_input: 0.06 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Input length <=512k. Current displayed effective rates, not struck-through list prices. | 2026-10-06 |
| minimax-api | standard_long / current | input: 0.6 USD / per_1000000_tokens; output: 2.4 USD / per_1000000_tokens; cached_input: 0.12 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Input length >512k. Current displayed effective rates, not struck-through list prices. | 2026-10-06 |
| minimax-api | priority_short / current | input: 0.44999999999999996 USD / per_1000000_tokens; output: 1.7999999999999998 USD / per_1000000_tokens; cached_input: 0.09 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Input length <=512k. Current displayed effective rates, not struck-through list prices. | 2026-10-06 |
| minimax-api | priority_long / current | input: 0.8999999999999999 USD / per_1000000_tokens; output: 3.5999999999999996 USD / per_1000000_tokens; cached_input: 0.18 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Input length >512k. Current displayed effective rates, not struck-through list prices. | 2026-10-06 |
| together | standard displayed serverless / current | input: 0.3 USD / per 1M tokens; cached_input: 0.06 USD / per 1M tokens; output: 1.2 USD / per 1M tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is MiniMax
- minimax-api / hosted_api: documented route; account eligibility unverified. Not established in this pass

## Sources

[MiniMax M3 Community License](https://huggingface.co/MiniMaxAI/MiniMax-M3/blob/main/LICENSE) · [MiniMax M3 model card](https://huggingface.co/MiniMaxAI/MiniMax-M3) · [MiniMax M3 independently profiled](https://artificialanalysis.ai/models/minimax-m3) · [MiniMax API pricing](https://platform.minimax.io/docs/pricing/overview)
