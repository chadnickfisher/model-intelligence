# Llama 4 Maverick 17B-128E Instruct

**Creator:** Meta · **Family:** Llama 4 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2025-04-05

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Multilingual visual chat (medium confidence)

Established downloadable option for image QA and multilingual chat when custom terms fit.

Conditions: Twelve explicitly supported languages; image evaluation up to five images.

Failure modes / limitations: Official instruction benchmarks used BF16, so quantized equivalence is unproven.

Supporting sources: [Llama 4 Scout / Maverick model card](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct) · [Llama 4 Maverick official card](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Early-fusion multimodal MoE autoregressive Transformer |
| parameters | total billion: 400; active billion: 17; scope: Creator-declared total and per-token active parameters.; exact parameter count: Unknown / not established |
| context window | native tokens: 1000000; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; output: text |
| language support | supported: Arabic; English; French; German; Hindi; Indonesian; Italian; Portuguese; Spanish; Tagalog; Thai; Vietnamese; notes: Other languages require additional tuning/evaluation and compliance. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

1 recorded access route(s); 0 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Llama 4 Community License

Restrictions: License copy, notices and Built with Llama labeling required.; Distributed improved models must begin name with Llama.; Separate authorization for >700M MAU at release-date test.; Incorporated AUP; EU-domicile restriction for these multimodal weights, except product/service end users.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: conditional

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Vendor: FP8 weights fit one H100 DGX host. Planning4-bit floor200GB before metadata/cache; multi-GPU or high-memory workstation.; Maverick is400B total, despite the17B-active name.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.
- No independently verified Maverick checkpoint-specific comparison extracted in this bounded pass; Scout evidence is not assigned to Maverick.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|

## Recorded access routes

- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Meta created the model; Hugging Face hosts gated artifacts.

## Sources

[Llama 4 Community License](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE) · [Llama 4 Maverick official card](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct) · [Llama 4 Scout / Maverick model card](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct) · [Llama 4 acceptable-use policy](https://github.com/meta-llama/llama-models/blob/main/models/llama4/USE_POLICY.md)
