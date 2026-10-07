# Mistral Medium 3.5 128B

**Creator:** Mistral AI · **Family:** Mistral Medium · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-04-28

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Unified reasoning coding (medium confidence)

Current Mistral candidate when one model must combine image input, coding and selectable reasoning.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): reasoning.general; coding.repository_work

Judgment ID: judgment-85878a81f8d11b0d

Conditions: Verify license eligibility and corrected long-context configuration.

Failure modes / limitations: Official card warns early Transformers config and GGUF conversions from it degrade long-context performance.

Supporting sources: [Mistral Medium 3.5 128B model card](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B) · [Mistral Medium3.5 independently profiled](https://artificialanalysis.ai/models/mistral-medium-3-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Dense multimodal decoder; unified instruction, reasoning and coding |
| parameters | total billion: 128; active billion: 128; scope: creator-declared count; see notes; exact parameter count: Unknown / not established |
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

License: Modified MIT

Restrictions: Retain notices.; No license rights if company/employer consolidated monthly revenue exceeds $20M in preceding month; obtain separate license or use Mistral hosting.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: conditional

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Planning estimate: 80–96GB class aggregate memory at 4-bit; multi-GPU FP8 needs over 128GB weights plus headroom.; Dense compute cost is much higher than 6.5B-active Small4. Card gives 8-way tensor-parallel serving examples, not a universal minimum.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.
- Replaces Medium3.1/Magistral in Le Chat and Devstral2 in Vibe; do not infer those products expose this exact configuration.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| mistral-api | standard / current | input: 1.5 USD / per_1000000_tokens; output: 7.5 USD / per_1000000_tokens; cached_input: 0.15 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Default standard tier; regional inference, batch and priority may have different rates. | 2026-10-06 |

## Recorded access routes

- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Mistral AI
- mistral-api / hosted_api: documented route; account eligibility unverified. Not established in this pass

## Sources

[Mistral Medium3.5 Modified MIT](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/blob/main/LICENSE) · [Mistral Medium 3.5 128B model card](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B) · [Mistral Medium3.5 independently profiled](https://artificialanalysis.ai/models/mistral-medium-3-5)
