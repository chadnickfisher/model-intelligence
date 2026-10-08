# Phi-4 Multimodal Instruct

**Creator:** Microsoft · **Family:** Phi-4 · **Status:** active
**Verified:** 2026-10-06 · **Release:** Unknown

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Compact audio image understanding (low confidence)

Multimodal adds image and audio input to a small text-output model.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): audio.understanding; vision.question_answering

Judgment ID: judgment-43dd1128b74944f9

Conditions: Use supported modality adapters; it does not generate audio.

Failure modes / limitations: Speech-language coverage differs from text; long-session drift and misleading sensitive voice-attribute inferences.

Supporting sources: [Phi-4 Multimodal official card](https://huggingface.co/microsoft/Phi-4-multimodal-instruct)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence limited by vendor-heavy task evidence and missing exact-task independent replication; documented interface support alone is not task quality.

### Vision.question_answering (low confidence)

The exact card supports a candidate for document questions delivered as synthetic speech, with a vendor s_DocVQA result; pure text-query and all-language performance are separate.

Scope: direct / conditional. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: vision.question_answering

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-61024ceeda4b1074

Conditions: Image plus synthetic spoken query; retain the s_ benchmark prefix. Korean fine-tuned adapter scores excluded.

Failure modes / limitations: Not established in this pass

Supporting sources: [Phi-4 Multimodal official card](https://huggingface.co/microsoft/Phi-4-multimodal-instruct)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence: limited exact-task evidence, vendor-heavy or unresolved configuration; scores are not confidence.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

### Vision.question_answering (low confidence)

Document and chart question results support useful visual answers, with counting and relationship limits that require material checking.

Scope: direct / conditional. English text-query visual QA under the creator zero-shot setup; spoken queries remain a separate finding.

Direct task IDs: vision.question_answering

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-2d69fe2e03e66c8c

Conditions: English image-plus-text questions; zero-shot prompts on the creator internal evaluation platform.; Dataset images; API formatting and JPEG conversion where interfaces require it; shared answer extraction.; Native model assessment; no specific provider route or quantized deployment assessed.

Failure modes / limitations: Counting and functional relationships require checking; scores across different benchmarks are not a common difficulty scale.

Supporting sources: [Phi-4 Multimodal official card](https://huggingface.co/microsoft/Phi-4-multimodal-instruct)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Vendor-only evidence; independent reproduction, immutable checkpoint, measurement date and full decoding/harness settings remain unknown.; Text-query DocVQA is distinct from synthetic spoken-query s_DocVQA; no transfer to other languages or fine-tuned audio adapters.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Phi-4 Mini dense language backbone with vision/audio encoders and modality-specific adapters |
| parameters | total billion: 5.6; active billion: Unknown / not established; scope: Creator-declared complete model; multimodal active count depends on input modality.; exact parameter count: Unknown / not established |
| context window | native tokens: 131072; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; audio; output: text |
| language support | text: Arabic; Chinese; Czech; Danish; Dutch; English; Finnish; French; German; Hebrew; Hungarian; Italian; Japanese; Korean; Norwegian; Polish; Portuguese; Russian; Spanish; Swedish; Thai; Turkish; Ukrainian; vision: English; audio: English; Chinese; German; French; Italian; Japanese; Spanish; Portuguese |

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

Hardware: Planning:8–12GB for supported quantization, or16–24GB for BF16 plus vision/audio/runtime headroom.; 128k capacity does not automatically fit local budgets; modality batches increase memory.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|

## Recorded access routes

- azure-foundry / Microsoft Foundry model catalog: documented_not_execution_tested. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Microsoft created the model; Hugging Face hosts artifacts.

## Sources

[MIT License](https://opensource.org/license/mit) · [Phi-4 Multimodal official card](https://huggingface.co/microsoft/Phi-4-multimodal-instruct) · [Phi-4 Multimodal config](https://huggingface.co/microsoft/Phi-4-multimodal-instruct/raw/main/config.json) · [Phi4 Multimodal catalog](https://artificialanalysis.ai/models/phi-4-multimodal)
