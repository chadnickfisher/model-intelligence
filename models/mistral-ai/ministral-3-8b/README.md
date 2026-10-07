# Ministral 3 8B Instruct

**Creator:** Mistral AI · **Family:** Ministral 3 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2025-12-02

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Edge multilingual chat (medium confidence)

Practical candidate for bounded local chat, extraction and image description.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): language.multilingual_chat; knowledge.extraction; vision.question_answering

Judgment ID: judgment-dada3e5e7dd7f855

Conditions: Choose the Instruct versus separate Reasoning checkpoint deliberately.

Failure modes / limitations: Complex autonomous planning and reasoning remain weaker; full 256k context can exceed edge memory.

Supporting sources: [Ministral 3 8B Instruct model card](https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512) · [Ministral3 8B independently profiled](https://artificialanalysis.ai/models/ministral-3-8b)

Contradictory or limiting sources: [Ministral3 8B independently profiled](https://artificialanalysis.ai/models/ministral-3-8b)

### Coding.refactoring (low confidence)

A local candidate for small Python simplifications; tiny flawed benchmark cannot justify broader claims.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.refactoring

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-c95618e6317eb57c

Conditions: Compact verbose Python code; three repetitions; Ollama 0.20.0, RTX 4060 8GB,Windows 10; instruct temperature 0; unit-test gating then Gemma 3 judge.

Failure modes / limitations: D5 is among seven universally failing tasks attributed to benchmark defects. Do not treat nominal 60% as calibrated ability.

Supporting sources: [Reasoning vs Instruct: A Local Python Coding Benchmark Across Two 8B Model Families](https://github.com/DenCoy-cloud/Local-llm-coding-python-benchmark)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Tiny function-level slice; no architecture/repository inference. PDF/ZIP artifacts listed, but advertised root CSV returned 404. Qwen3.5-9B was replaced by Qwen3-8B, despite misleading internal key; no transfer.; Confidence concerns this bounded claim, not a capability score.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Dense 8.4B language model plus 0.4B vision encoder |
| parameters | total billion: 8.8; active billion: 8.4; scope: 8.4B LM + 0.4B vision; active_billion denotes dense LM, not per-image encoder compute.; exact parameter count: Unknown / not established |
| context window | native tokens: 262144; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

5 recorded access route(s); 2 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Apache-2.0

Restrictions: Retain copyright/license notices; comply with the license.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: allowed

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Vendor says FP8 fits 12GB VRAM; planning 8–12GB with 4-bit at modest context.; Instruct FP8, BF16 and separate Reasoning checkpoints exist; other family sizes are 3B and 14B, not identical profiles.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| mistral-api | Standard / current | input: 0.15 USD / per 1 million tokens; output: 0.15 USD / per 1 million tokens; cached_input: 0.015 USD / per 1 million tokens | Rates are standard. Batch/priority/regional tiers distinct; do not infer a default account tier. | 2026-10-07 |
| mistral-api | standard / historical | input: 0.15 USD / per_1000000_tokens; output: 0.15 USD / per_1000000_tokens; cached_input: 0.015 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Default standard tier; regional inference, batch and priority may have different rates. | 2026-10-06 |

## Recorded access routes

- fireworks / On-demand GPU deployment: documented_not_execution_tested. Not established in this pass
- mistral-api / Mistral API Standard: documented_not_execution_tested. Not established in this pass
- mistral-api / Mistral plan included API usage: documented_not_execution_tested. Not established in this pass
- mistral-api / hosted_api: documented route; account eligibility unverified. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Mistral AI

## Sources

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) · [Ministral 3 8B Instruct model card](https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512) · [Ministral3 8B independently profiled](https://artificialanalysis.ai/models/ministral-3-8b)
