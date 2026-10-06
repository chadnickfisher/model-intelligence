# DeepSeek-V4-Pro-0813

**Creator:** DeepSeek · **Family:** DeepSeek V4 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-08-13

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Text coding and reasoning (medium confidence)

Officially supersedes Preview and remains a capable text-agent option.

Conditions: Use 0813 evidence, not April preview scores; reasoning low/high/max changes behavior.

Failure modes / limitations: Text-only; system-level results depend on DeepSeek Harness; no independent checkpoint-matched test established here.

Supporting sources: [DeepSeek-V4-Pro-0813 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813) · [DeepSeek live pricing and alias mapping](https://api-docs.deepseek.com/quick_start/pricing/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Sparse-attention MoE V4 backbone plus DSpark speculative decoder |
| parameters | total billion: 1600; active billion: 49; scope: 1.6T backbone; HF full artifact rounds to 1.7T; exact all-component total not verified.; exact parameter count: Unknown / not established |
| context window | native tokens: 1000000; extended tokens: Unknown / not established; max output tokens: 384000; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | 384000 |
| modalities | input: text; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

2 recorded access route(s); 2 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: MIT

Restrictions: Retain copyright/license notices; comply with the license.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: allowed

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Datacenter-scale multi-GPU/multi-node; ideal 4-bit backbone alone roughly 800GB.; HF serialized artifact rounds to 1.7T due to auxiliary modules; real storage floor is higher than the headline-backbone calculation.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.
- Independent 0813-only reproducible comparison not verified.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| deepseek-api | peak / current | input: 1.32 USD / per_1000000_tokens; output: 3.96 USD / per_1000000_tokens; cached_input: 0.044 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Peak weekdays 01:00–04:00 and 06:00–10:00 UTC, excluding Chinese public holidays. Off-peak all other times. Reasoning and final tokens contribute to output billing. | 2026-10-06 |
| deepseek-api | off_peak / current | input: 0.66 USD / per_1000000_tokens; output: 1.98 USD / per_1000000_tokens; cached_input: 0.022 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Peak weekdays 01:00–04:00 and 06:00–10:00 UTC, excluding Chinese public holidays. Off-peak all other times. Reasoning and final tokens contribute to output billing. | 2026-10-06 |

## Recorded access routes

- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is DeepSeek
- deepseek-api / hosted_api: documented route; account eligibility unverified. Not established in this pass

## Sources

[huggingface.co](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813/blob/main/LICENSE) · [DeepSeek-V4-Pro-0813 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813) · [DeepSeek live pricing and alias mapping](https://api-docs.deepseek.com/quick_start/pricing/) · [DeepSeek V4 architecture introduction](https://deepseek.com/en/news/v4-preview/)
