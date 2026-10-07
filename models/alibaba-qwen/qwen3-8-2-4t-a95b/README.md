# Qwen3.8-2.4T-A95B

**Creator:** Alibaba / Qwen · **Family:** Qwen3.8 · **Status:** active
**Verified:** 2026-10-06 · **Release:** Unknown

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Large scale text agents (low confidence)

A candidate for capable self-hosted text coding and work agents if infrastructure justifies it.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.repository_work; agent.tool_use

Judgment ID: judgment-5b2db26e97cc525c

Conditions: Creator benchmarks use differing harnesses; hosted Qwen3.8 Max 0902 is a separate identity until mapped.

Failure modes / limitations: Substantial infrastructure burden; no image input in this checkpoint; official comparisons include modified benchmark tasks.

Supporting sources: [Qwen3.8-2.4T-A95B model card](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Coding.repository_work (low confidence)

Exact open-weight repository-work ability remains unresolved: the card labels its coding benchmark column Qwen3.8-Max, a hosted model with additional capabilities.

Scope: direct / unknown. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: coding.repository_work

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-fba9d11fe50c103d

Conditions: Hosted Qwen3.8-Max scores and its Claude Code harness are excluded from this checkpoint.

Failure modes / limitations: Not established in this pass

Supporting sources: [Qwen3.8-2.4T-A95B model card](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B) · [Qwen3.8 2.4T A95B analysis](https://artificialanalysis.ai/models/qwen3-8-2-4t-a95b)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence: limited exact-task evidence, vendor-heavy or unresolved configuration; scores are not confidence.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Hybrid MoE Gated DeltaNet / gated attention; 512 experts, 10 routed plus one shared active |
| parameters | total billion: 2400; active billion: 95; scope: creator-declared count; see notes; exact parameter count: Unknown / not established |
| context window | native tokens: 262144; extended tokens: 1010000; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

3 recorded access route(s); 2 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Qwen3.8-Max License

Restrictions: Retain notices.; MaaS/AI Work Assistant businesses above $50M aggregate trailing-12-month revenue need separate commercial license; internal-only exemption.; UI branding above 100M MAU or $20M monthly product/service revenue.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: conditional

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Datacenter scale: ideal 4-bit weights alone are 1.2TB; plan a multi-node accelerator cluster with additional headroom.; 95B active is compute, not 95B total storage; no tested minimum configuration verified.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.
- Exact release day and independent checkpoint-matched evaluation not verified.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| novita | Standard / current | input: 2 USD / per 1 million tokens; output: 6 USD / per 1 million tokens; cached_input: 0.25 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |
| together | Standard / current | input: 2 USD / per 1 million tokens; output: 6 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |

## Recorded access routes

- novita / Serverless inference: officially_documented_not_execution_tested. Not established in this pass
- together / Serverless inference: officially_documented_not_execution_tested. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Alibaba / Qwen

## Sources

[Qwen3.8-Max License](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B/blob/main/LICENSE) · [Qwen3.8-2.4T-A95B model card](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B) · [Qwen3.8 2.4T A95B analysis](https://artificialanalysis.ai/models/qwen3-8-2-4t-a95b)
