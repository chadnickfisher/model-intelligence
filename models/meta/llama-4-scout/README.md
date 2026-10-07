# Llama 4 Scout 17B-16E Instruct

**Creator:** Meta · **Family:** Llama 4 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2025-04-05

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Multilingual visual chat (medium confidence)

Established downloadable option for image QA and multilingual chat when custom terms fit.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): language.multilingual_chat; vision.question_answering

Judgment ID: judgment-3bdbe688baf73a67

Conditions: Twelve explicitly supported languages; image evaluation up to five images.

Failure modes / limitations: Official instruction benchmarks used BF16, so quantized equivalence is unproven.

Supporting sources: [Llama 4 Scout / Maverick model card](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct) · [Llama 4 Maverick official card](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Very long document work (medium confidence)

Scout’s 10M advertised capacity is not enough evidence to prefer it for difficult long-document reasoning.

Scope: unresolved / warning. Scope needs review; the original claim does not establish a specific task ability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): context.reasoning

Judgment ID: judgment-9a9a7a9cb18c9163

Conditions: Test position sensitivity and retrieval on real documents.

Failure modes / limitations: Very large KV memory and incomplete long-context reasoning reliability.

Supporting sources: [Llama 4 Scout / Maverick model card](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct)

Contradictory or limiting sources: [Scout independent comparison](https://artificialanalysis.ai/models/comparisons/llama-4-scout-vs-llama-3-1-instruct-405b)

### Coding.review (low confidence)

Can assist with low-context refactoring preference review; does not establish deep design judgment.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.review

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-b0524d80aaeb6829

Conditions: Public API defaults; exact revision undisclosed; only two refactoring types.; Named release matches; preserve source-specific provider, snapshot and precision limitations.

Failure modes / limitations: Style shortcuts, missing context and conservative ties.

Supporting sources: [High Agreement, Shallow Reasoning: A Mixed-Method Study of LLMs in Refactoring Reviews](https://homepages.dcc.ufmg.br/~figueiredo/publications/promise2026preprint.pdf)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Early-fusion multimodal MoE autoregressive Transformer |
| parameters | total billion: 109; active billion: 17; scope: Creator-declared total and per-token active parameters.; exact parameter count: Unknown / not established |
| context window | native tokens: 10000000; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; output: text |
| language support | supported: Arabic; English; French; German; Hindi; Indonesian; Italian; Portuguese; Spanish; Tagalog; Thai; Vietnamese; notes: Other languages require additional tuning/evaluation and compliance. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

3 recorded access route(s); 1 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Llama 4 Community License

Restrictions: License copy, notices and Built with Llama labeling required.; Distributed improved models must begin name with Llama.; Separate authorization for >700M MAU at release-date test.; Incorporated AUP; EU-domicile restriction for these multimodal weights, except product/service end users.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: conditional

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Vendor: one H100 with on-the-fly INT4. Planning: >=80GB accelerator/unified memory for modest context.; The10M context maximum is not a demonstrated one-GPU operating point.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| novita | Standard / current | input: 0.18 USD / per 1 million tokens; output: 0.59 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |

## Recorded access routes

- novita / hosted metered api: documented_not_execution_tested. Not established in this pass
- fireworks / hosted deployment: exact model family listing observed; deployment offer/price not promoted from catalog. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Meta created the model; Hugging Face hosts gated artifacts.

## Sources

[Llama 4 Community License](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE) · [Llama 4 Scout / Maverick model card](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct) · [Llama 4 Maverick official card](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct) · [Scout independent comparison](https://artificialanalysis.ai/models/comparisons/llama-4-scout-vs-llama-3-1-instruct-405b) · [Llama 4 acceptable-use policy](https://github.com/meta-llama/llama-models/blob/main/models/llama4/USE_POLICY.md)
