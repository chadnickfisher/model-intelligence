# Nemotron3 Ultra 550B-A55B

**Creator:** NVIDIA · **Family:** Nemotron3 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-06-04

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### High throughput text agents (medium confidence)

A strong deployment candidate for low-latency text agents on suitable NVIDIA infrastructure.

Conditions: NVFP4 and runtime support are material; distinguish prerelease service speed from local hardware.

Failure modes / limitations: High-end math/physics reasoning still weak on some tasks; no native vision input.

Supporting sources: [Nemotron3 Ultra 550B-A55B model card](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16) · [Nemotron3 Ultra release evaluation](https://artificialanalysis.ai/articles/nvidia-nemotron-3-ultra-released)

Contradictory or limiting sources: [Nemotron3 Ultra release evaluation](https://artificialanalysis.ai/articles/nvidia-nemotron-3-ultra-released)

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Mamba2 / attention hybrid LatentMoE with MTP |
| parameters | total billion: 550; active billion: 55; scope: creator-declared count; see notes; exact parameter count: Unknown / not established |
| context window | native tokens: 1048576; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; output: text |
| language support | supported: English; French; Spanish; Italian; German; Japanese; Hindi; Korean; Brazilian Portuguese; Chinese; notes: Creator-declared supported languages. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

1 recorded access route(s); 0 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: OpenMDW-1.1

Restrictions: Redistribution must retain agreement and origin notices.; Patent/copyright litigation termination clause, defensive exception.; No output restrictions; third-party rights still require diligence.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: allowed

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Vendor BF16 example: 8×B200 (~1.5TB HBM); summary lists 16×H100 or 8×H200. NVFP4 cuts ideal weight floor to275GB.; Vendor minimum snippets vary by precision/runtime; full 1M needs explicit configuration. TensorRT-LLM currently documented as Blackwell-only in card.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.
- Creator releases training data and recipes in addition to weights; completeness of full reproducible training source was not audited.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|

## Recorded access routes

- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is NVIDIA

## Sources

[OpenMDW1.1](https://raw.githubusercontent.com/OpenMDW/OpenMDW/refs/heads/main/1.1/LICENSE.OpenMDW-1.1) · [Nemotron3 Ultra 550B-A55B model card](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16) · [Nemotron3 Ultra release evaluation](https://artificialanalysis.ai/articles/nvidia-nemotron-3-ultra-released)
