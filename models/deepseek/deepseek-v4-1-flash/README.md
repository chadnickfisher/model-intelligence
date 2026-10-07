# DeepSeek-V4.1-Flash

**Creator:** DeepSeek · **Family:** DeepSeek V4.1 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-10

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Input heavy tool agents (medium confidence)

Promising cost-oriented candidate for long-context coding/review and image-grounded tool tasks.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.repository_work; coding.review; agent.tool_use

Judgment ID: judgment-c78023ee7891bfab

Conditions: Check maximum reasoning effort versus task cost; preserve correct prompt encoding.

Failure modes / limitations: Creator DeepSWE results vary materially by harness; long traces, tool mistakes and invalid edits remain possible.

Supporting sources: [DeepSeek-V4.1-Flash model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) · [DeepSeek V4.1 Flash max independently profiled](https://artificialanalysis.ai/models/deepseek-v4-1-flash) · [DeepSeek live pricing and alias mapping](https://api-docs.deepseek.com/quick_start/pricing/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Self host cost savings (low confidence)

No automatic savings from open weights; utilization and infrastructure dominate.

Scope: performance / warning. Cost, deployment or throughput observation; not a task capability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-71e1895294a2759d

Conditions: Compare full GPU/RAM/operator cost with actual cached API token mix.

Failure modes / limitations: Underutilized hardware can cost more than API access.

Supporting sources: [DeepSeek-V4.1-Flash model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Causal encoder-decoder MoE with CSA2, sparse indexing, mHC, Engram lookup memory and DSpark draft module |
| parameters | total billion: 763; active billion: 16; scope: 763B serialized HF artifact; creator headline is 552B backbone, plus conditional memory and auxiliaries.; exact parameter count: Unknown / not established; backbone billion: 552; conditional memory billion: 196; active prefill billion: 8; active decode billion: 16 |
| context window | native tokens: 1000000; extended tokens: Unknown / not established; max output tokens: 384000; notes: 384K is first-party API limit; weight-card generation example recommends >=256K budget, not a separate model hard limit. |
| maximum output | 384000 |
| modalities | input: text; image; output: text |
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

Hardware: Datacenter or specialized workstation: 4-bit floor about 382GB for all serialized parameters; reserve substantially more RAM/HBM and confirm support.; 552B backbone + 196B Engram conditional memory; HF artifact reports 763B including auxiliary components. 8B active prefill / 16B decode excludes a simple universal active-count interpretation. Engram can be placed separately; no minimum verified.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| deepseek-api | peak / current | input: 0.3 USD / per_1000000_tokens; output: 1.2 USD / per_1000000_tokens; cached_input: 0.006 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Peak weekdays 01:00–04:00 and 06:00–10:00 UTC, excluding Chinese public holidays. Off-peak all other times. Reasoning and final tokens contribute to output billing. | 2026-10-06 |
| deepseek-api | off_peak / current | input: 0.15 USD / per_1000000_tokens; output: 0.6 USD / per_1000000_tokens; cached_input: 0.003 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Peak weekdays 01:00–04:00 and 06:00–10:00 UTC, excluding Chinese public holidays. Off-peak all other times. Reasoning and final tokens contribute to output billing. | 2026-10-06 |

## Recorded access routes

- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is DeepSeek
- deepseek-api / hosted_api: documented route; account eligibility unverified. Not established in this pass

## Sources

[huggingface.co](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/LICENSE) · [DeepSeek-V4.1-Flash model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) · [DeepSeek V4.1 Flash max independently profiled](https://artificialanalysis.ai/models/deepseek-v4-1-flash) · [DeepSeek live pricing and alias mapping](https://api-docs.deepseek.com/quick_start/pricing/)
