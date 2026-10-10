# Phi-4-Reasoning-Vision-15B

**Creator:** Microsoft · **Family:** Phi-4 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-03-04

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### English visual math and grounding (low confidence)

A compact specialist candidate for charts, visual math and GUI element grounding.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): reasoning.math; vision.question_answering; vision.grounding

Judgment ID: judgment-3947e022646bea11

Conditions: English-focused; selective thinking can save compute but benchmark all required task types.

Failure modes / limitations: 16k window; hallucination/visual reasoning limitations; independent matched evaluation not verified.

Supporting sources: [Phi-4-Reasoning-Vision-15B model card](https://huggingface.co/microsoft/Phi-4-reasoning-vision-15B) · [Phi-4-reasoning-vision and the lessons of training a multimodal reasoning model](https://www.microsoft.com/en-us/research/blog/phi-4-reasoning-vision-and-the-lessons-of-training-a-multimodal-reasoning-model/)

Contradictory or limiting sources: [Phi-4-reasoning-vision and the lessons of training a multimodal reasoning model](https://www.microsoft.com/en-us/research/blog/phi-4-reasoning-vision-and-the-lessons-of-training-a-multimodal-reasoning-model/)

### Vision.grounding (low confidence)

Vendor ScreenSpot V2 measurements support static GUI element localization as a candidate; this does not demonstrate an autonomous computer-use agent.

Scope: direct / conditional. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: vision.grounding

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-87ac71979507153c

Conditions: Default hybrid model under VLMEvalKit; forced no-think/thinking columns kept separate.

Failure modes / limitations: Not established in this pass

Supporting sources: [Phi-4-Reasoning-Vision-15B model card](https://huggingface.co/microsoft/Phi-4-reasoning-vision-15B)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence: limited exact-task evidence, vendor-heavy or unresolved configuration; scores are not confidence.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Dense Phi4-Reasoning backbone + SigLIP2 mid-fusion dynamic-resolution vision encoder |
| parameters | total billion: 15; active billion: 15; scope: 15B declared complete model; dense active label is shorthand, not precise per-image conditional compute.; exact parameter count: Unknown / not established |
| context window | native tokens: 16384; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; output: text |
| language support | supported: English; notes: Microsoft says not intended for multilingual use; other languages may degrade. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

2 recorded access route(s); 0 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: MIT

Restrictions: Retain copyright/license notices; comply with the license.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: allowed

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: BF16 planning: 40–48GB GPU comfortable; 4-bit 12–16GB theoretical planning target only when the runtime supports the vision architecture.; Microsoft recommends BF16 vLLM and tested A6000/A100/H100/B200. Quantized local compatibility was not verified.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|

## Recorded access routes

- azure-foundry / Microsoft Foundry model catalog: documented_not_execution_tested. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Microsoft

## Sources

[MIT License](https://opensource.org/license/mit) · [Phi-4-Reasoning-Vision-15B model card](https://huggingface.co/microsoft/Phi-4-reasoning-vision-15B) · [Phi-4-reasoning-vision and the lessons of training a multimodal reasoning model](https://www.microsoft.com/en-us/research/blog/phi-4-reasoning-vision-and-the-lessons-of-training-a-multimodal-reasoning-model/)
