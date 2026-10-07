# Llama 4 Maverick 17B-128E Instruct

**Creator:** Meta · **Family:** Llama 4 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2025-04-05

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Multilingual visual chat (medium confidence)

Established downloadable option for image QA and multilingual chat when custom terms fit.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): language.multilingual_chat; vision.question_answering

Judgment ID: judgment-c7238ff23167f60d

Conditions: Twelve explicitly supported languages; image evaluation up to five images.

Failure modes / limitations: Official instruction benchmarks used BF16, so quantized equivalence is unproven.

Supporting sources: [Llama 4 Scout / Maverick model card](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct) · [Llama 4 Maverick official card](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Coding.repository_work (low confidence)

Scale reports a low SWE-bench Pro result for the named Maverick Instruct route. This is a repository-task warning under that scaffold, not a verdict on every coding task.

Scope: direct / warning. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: coding.repository_work

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-4c86ac1246e4aa6b

Conditions: Scale route llama4-maverick-17b-instruct; provider precision/serving revision not extracted. Experimental Arena chat-variant Elo excluded.

Failure modes / limitations: Low repository-task completion in the inspected Scale setup.

Supporting sources: [Llama 4 Maverick official card](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct) · [SWE-bench Pro public leaderboard](https://labs.scale.com/leaderboard/swe_bench_pro)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence in generalization: one independent scaffold and incomplete route/turn-limit configuration.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

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

Hardware: Vendor: FP8 weights fit one H100 DGX host. Planning4-bit floor200GB before metadata/cache; multi-GPU or high-memory workstation.; Maverick is400B total, despite the17B-active name.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.
- No independently verified Maverick checkpoint-specific comparison extracted in this bounded pass; Scout evidence is not assigned to Maverick.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| novita | Standard / current | input: 0.27 USD / per 1 million tokens; output: 0.85 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |

## Recorded access routes

- fireworks / hosted deployment: exact model family listing observed; deployment offer/price not promoted from catalog. Not established in this pass
- novita / hosted metered api: documented_not_execution_tested. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Meta created the model; Hugging Face hosts gated artifacts.

## Sources

[Llama 4 Community License](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE) · [Llama 4 Maverick official card](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct) · [Llama 4 Scout / Maverick model card](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct) · [Llama 4 acceptable-use policy](https://github.com/meta-llama/llama-models/blob/main/models/llama4/USE_POLICY.md) · [SWE-bench Pro public leaderboard](https://labs.scale.com/leaderboard/swe_bench_pro)
