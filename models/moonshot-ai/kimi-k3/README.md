# Kimi K3

**Creator:** Moonshot AI · **Family:** Kimi · **Status:** active
**Verified:** 2026-10-06 · **Release:** Unknown

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Long horizon multimodal agents (medium confidence)

Strong candidate for large-scale visual coding and tool-based knowledge work if cost and license are acceptable.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): agent.long_horizon; coding.repository_work; research.synthesis

Judgment ID: judgment-ce599538fb19f653

Conditions: Thinking is always on; preserve complete returned assistant messages including reasoning and tool fields.

Failure modes / limitations: Harness-dependent benchmark results; visual tasks still fail; preserving long histories increases costs.

Supporting sources: [Kimi K3 model card](https://huggingface.co/moonshotai/Kimi-K3) · [Kimi K3 max independently profiled](https://artificialanalysis.ai/models/kimi-k3)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | MoE with Kimi Delta Attention, gated MLA, Attention Residuals, Stable LatentMoE; MoonViT-V2 vision encoder |
| parameters | total billion: 2800; active billion: 104; scope: creator-declared count; see notes; exact parameter count: Unknown / not established; components billion: vision encoder: 0.401 |
| context window | native tokens: 1048576; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; video; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

2 recorded access route(s); 3 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Kimi K3 License

Restrictions: Retain notices.; MaaS business above $20M aggregate trailing-12-month revenue requires agreement.; UI branding above 100M MAU or $20M monthly revenue.; Internal-only use and official products/certified inference partners exempt from preceding commercial/branding conditions.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: conditional

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Datacenter scale: native MXFP4 weights alone roughly 1.4TB plus quantization/runtime/cache; multi-node high-memory deployment.; Quantization-aware trained MXFP4 weights / MXFP8 activations; do not substitute a 104B-active memory estimate.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| together | standard displayed serverless / current | input: 2.7 USD / per 1M tokens; cached_input: 0.27 USD / per 1M tokens; output: 13.5 USD / per 1M tokens | Not established in this pass | 2026-10-06 |
| fireworks | Standard / current | input: 3 USD / per 1M tokens; cached_input: 0.3 USD / per 1M tokens; output: 15 USD / per 1M tokens | Not established in this pass | 2026-10-06 |
| fireworks | Priority / current | input: 3.75 USD / per 1M tokens; cached_input: 0.375 USD / per 1M tokens; output: 18.75 USD / per 1M tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Moonshot AI
- kimi-api / hosted_api: documented route; account eligibility unverified. Not established in this pass

## Sources

[Kimi K3 License](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE) · [Kimi K3 model card](https://huggingface.co/moonshotai/Kimi-K3) · [Kimi K3 max independently profiled](https://artificialanalysis.ai/models/kimi-k3)
