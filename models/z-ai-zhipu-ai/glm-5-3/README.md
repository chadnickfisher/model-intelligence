# GLM-5.3

**Creator:** Z.ai / Zhipu AI · **Family:** GLM5 · **Status:** active
**Verified:** 2026-10-06 · **Release:** Unknown

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Long horizon text coding (medium confidence)

Strong candidate for coding agents and text-based knowledge work with sufficient serving resources.

Conditions: Preserve reasoning/template semantics; compare max effort using complete-task budgets.

Failure modes / limitations: Creator evaluations alter some anti-cheat checks and harnesses; cyber/terminal strengths do not establish visual capability.

Supporting sources: [GLM-5.3 model card](https://huggingface.co/zai-org/GLM-5.3) · [GLM5.3 max independently profiled](https://artificialanalysis.ai/models/glm-5-3)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | MoE with DeepSeek-style sparse attention; same base model as GLM5.2, newer post-training |
| parameters | total billion: 753; active billion: 40; scope: 753B HF serialized artifact, 40B rounded active from independent catalog; runtime maintainer says ~743B/39B. Preserve discrepancy.; exact parameter count: Unknown / not established |
| context window | native tokens: 1000000; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

3 recorded access route(s); 2 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: GLM-5.3 License

Restrictions: Retain notices.; MaaS operator above $10B aggregate trailing-12-month revenue must pass Z.ai security review before commercial use.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: conditional

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Datacenter / high-memory multi-GPU: ideal 4-bit full weights around 377GB plus substantial headroom.; Runtime-maintainer count ~743B/39B differs from serialized HF 753B / AA 40B; neither equals required VRAM.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| zai-api | standard / current | input: 1.4 USD / per_1000000_tokens; output: 4.4 USD / per_1000000_tokens; cached_input: 0.26 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Cached-input storage currently labeled limited-time free; promotional expired rates are excluded. | 2026-10-06 |
| mistral-api | standard / current | input: 1.4 USD / per_1000000_tokens; output: 4.4 USD / per_1000000_tokens; cached_input: 0.14 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Default standard tier; regional inference, batch and priority may have different rates. | 2026-10-06 |

## Recorded access routes

- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Z.ai / Zhipu AI
- zai-api / hosted_api: documented route; account eligibility unverified. Not established in this pass
- mistral-api / hosted_api: documented route; account eligibility unverified. Not established in this pass

## Sources

[GLM5.3 License](https://huggingface.co/zai-org/GLM-5.3/blob/main/LICENSE) · [GLM-5.3 model card](https://huggingface.co/zai-org/GLM-5.3) · [GLM5.3 max independently profiled](https://artificialanalysis.ai/models/glm-5-3) · [vLLM GLM5.3 recipe](https://recipes.vllm.ai/zai-org/GLM-5.3) · [GLM5.3 endpoint guide](https://docs.z.ai/guides/llm/glm-5.3)
