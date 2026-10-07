# Qwen3-Coder-Next

**Creator:** Alibaba / Qwen · **Family:** Qwen3-Coder · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-02-03

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Local repository editing (medium confidence)

Useful coding-specialist candidate where non-thinking responses and permissive licensing matter.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: coding.repository_work

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-6c53b662d08a63d0

Conditions: Use its coding chat template and supported tool parser; do not add thinking tokens.

Failure modes / limitations: General knowledge/reasoning quality is not established by SWE performance; small quantization may degrade code correctness.

Supporting sources: [Qwen3-Coder-Next model card](https://huggingface.co/Qwen/Qwen3-Coder-Next) · [Qwen3-Coder-Next technical report](https://arxiv.org/abs/2603.00729)

Contradictory or limiting sources: [Qwen3-Coder-Next independently profiled](https://artificialanalysis.ai/models/qwen3-coder-next)

### Coding.debugging (low confidence)

Can assist narrowly specified quantum-circuit repair with executable validation and retries.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-4205dcdceec8959d

Conditions: QBugLM; OpenQASM3; five5-qubit circuit families; structured prompts; up to two feedback retries.

Failure modes / limitations: BV repair score depended strongly on prompting:95%structured versus45%CoT and63%ReAct.; Semantic-error cases remained difficult.

Supporting sources: [QBugLM quantum software debugging](https://arxiv.org/html/2606.07314v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Paper has inconsistent category wording; do not use its contradictory category100%claims.; Non-thinking checkpoint: do not repeat paper's reasoning-mode characterization.; Confidence concerns this bounded claim, not a capability score.

### Coding.debugging (low confidence)

Useful for test-guided single-file repair locally, with edge-case checks.

Scope: direct / warning. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-7de8091ed4d4e8fd

Conditions: ClosedCode/Ollama; ASUSGX10/GB10,128GB unified memory; Q4_K_M.

Failure modes / limitations: CSV repair passed14/14visible tests but6/8hidden; another run passed8/8.; Q8_0 configuration stalled under its hardware/time conditions; that is deployment evidence, not proof of weaker weights.

Supporting sources: [Local ClosedCode editing and CSV repair study](https://zenn.dev/nicktominaga/articles/closedcode-local-llm-benchmark?locale=en)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

### Coding.refactoring (low confidence)

Constrained cleanup is promising; deeper restructuring remains weakly established.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.refactoring

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-588f397f0e9fc08d

Conditions: GAUNTLET LM Studio on Apple M5 Max 128 GB; fixed LLM judge, private prompt/rubric. APEX multi-model grading plus operator review, not a published behavior-equivalence test.

Failure modes / limitations: CQRS result much weaker than cleanup; incompatible tests and serving routes cannot be averaged.

Supporting sources: [Qwen3-Coder-Next 80B 4bit MLX](https://www.gauntletbench.com/models/qwen3-coder-next-80b-4bit-mlx/) · [Qwen3 Coder Next — APEX Testing](https://www.apex-testing.org/models/c649241c-1f6d-4dca-8817-daf63b0b60fe)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Only low-confidence, narrowly scoped evidence. No demonstrated large-repository refactoring reliability or architecture rating.; Confidence concerns this bounded claim, not a capability score.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Hybrid MoE Gated DeltaNet / gated attention |
| parameters | total billion: 80; active billion: 3; scope: creator-declared count; see notes; exact parameter count: Unknown / not established |
| context window | native tokens: 262144; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

2 recorded access route(s); 1 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Apache-2.0

Restrictions: Retain copyright/license notices; comply with the license.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: allowed

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Planning estimate: 48–64GB aggregate GPU/unified memory at 4-bit and moderate context; 24GB GPU can offload experts into 64GB+ RAM at a throughput cost.; 

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| novita | Standard / current | input: 0.2 USD / per 1 million tokens; output: 1.5 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |

## Recorded access routes

- novita / Serverless inference: officially_documented_not_execution_tested. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Alibaba / Qwen

## Sources

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) · [Qwen3-Coder-Next model card](https://huggingface.co/Qwen/Qwen3-Coder-Next) · [Qwen3-Coder-Next technical report](https://arxiv.org/abs/2603.00729) · [Qwen3-Coder-Next independently profiled](https://artificialanalysis.ai/models/qwen3-coder-next)
