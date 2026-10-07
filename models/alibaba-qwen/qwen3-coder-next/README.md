# Qwen3-Coder-Next

**Creator:** Alibaba / Qwen · **Family:** Qwen3-Coder · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-02-03

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Local repository editing (medium confidence)

Useful coding-specialist candidate where non-thinking responses and permissive licensing matter.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: coding.repository_work

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-6c53b662d08a63d0

Conditions: Use its coding chat template and supported tool parser; do not add thinking tokens.

Failure modes / limitations: General knowledge/reasoning quality is not established by SWE performance; small quantization may degrade code correctness.

Supporting sources: [Qwen3-Coder-Next model card](https://huggingface.co/Qwen/Qwen3-Coder-Next) · [Qwen3-Coder-Next technical report](https://arxiv.org/abs/2603.00729)

Contradictory or limiting sources: [Qwen3-Coder-Next independently profiled](https://artificialanalysis.ai/models/qwen3-coder-next)

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Hybrid MoE Gated DeltaNet / gated attention |
| parameters | total billion: 80; active billion: 3; scope: creator-declared count; see notes; exact parameter count: Unknown / not established |
| context window | native tokens: 262144; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; output: text |
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

Hardware: Planning estimate: 48–64GB aggregate GPU/unified memory at 4-bit and moderate context; 24GB GPU can offload experts into 64GB+ RAM at a throughput cost.; 

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|

## Recorded access routes

- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Alibaba / Qwen

## Sources

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) · [Qwen3-Coder-Next model card](https://huggingface.co/Qwen/Qwen3-Coder-Next) · [Qwen3-Coder-Next technical report](https://arxiv.org/abs/2603.00729) · [Qwen3-Coder-Next independently profiled](https://artificialanalysis.ai/models/qwen3-coder-next)
