# Phi-4 Mini Instruct

**Creator:** Microsoft · **Family:** Phi-4 · **Status:** active
**Verified:** 2026-10-06 · **Release:** Unknown

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Low memory instruction tasks (medium confidence)

Mini is suitable to evaluate for small, bounded instruction and simple coding tasks.

Conditions: 23 supported text languages; verify APIs beyond common Python packages.

Failure modes / limitations: Card reports function-name/URL hallucination, long-chat drift and multilingual safety gaps.

Supporting sources: [Phi-4 Mini / Multimodal model card](https://huggingface.co/microsoft/Phi-4-mini-instruct)

Contradictory or limiting sources: [Phi4 Mini catalog audit](https://artificialanalysis.ai/models/phi-4-mini)

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Dense decoder-only GQA Transformer |
| parameters | total billion: 3.8; active billion: 3.8; scope: Creator-declared complete model; multimodal active count depends on input modality.; exact parameter count: Unknown / not established |
| context window | native tokens: 131072; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; output: text |
| language support | supported: Arabic; Chinese; Czech; Danish; Dutch; English; Finnish; French; German; Hebrew; Hungarian; Italian; Japanese; Korean; Norwegian; Polish; Portuguese; Russian; Spanish; Swedish; Thai; Turkish; Ukrainian; notes: This is Mini text-language list. Multimodal audio-language coverage must be checked separately. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

1 recorded access route(s); 0 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: MIT

Restrictions: Retain copyright/license notices; comply with the license.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: allowed

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Planning:4–8GB device memory with supported4-bit weights and modest context. BF16 floor7.6GB before runtime/cache.; Full128k context may exceed these budgets.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|

## Recorded access routes

- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Microsoft created the model; Hugging Face hosts artifacts.

## Sources

[MIT License](https://opensource.org/license/mit) · [Phi-4 Mini / Multimodal model card](https://huggingface.co/microsoft/Phi-4-mini-instruct) · [Phi4 Mini catalog audit](https://artificialanalysis.ai/models/phi-4-mini) · [Phi-4 Mini config](https://huggingface.co/microsoft/Phi-4-mini-instruct/raw/main/config.json)
