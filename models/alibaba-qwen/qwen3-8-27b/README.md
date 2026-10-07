# Qwen3.8-27B

**Creator:** Alibaba / Qwen · **Family:** Qwen3.8 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-08-14

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Local multimodal coding (medium confidence)

A credible compact candidate for iterative code editing and image-grounded workflows.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.scoped_edit; vision.question_answering

Judgment ID: judgment-dadec61aa2e25c5d

Conditions: Use supported thinking/template settings; compare medium and xhigh by whole-task cost.

Failure modes / limitations: Dependent tool-call ordering failures and runtime grammar issues were reported in one local setup.

Supporting sources: [Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B) · [Qwen3.8 27B xhigh independently profiled](https://artificialanalysis.ai/models/qwen3-8-27b) · [Single-R9700 Qwen3.8 comparison](https://www.reddit.com/r/Qwen_AI/comments/1wxshto/qwen3827b_vs_qwen38flashnext_as_agent_workers_on/)

Contradictory or limiting sources: [Single-R9700 Qwen3.8 comparison](https://www.reddit.com/r/Qwen_AI/comments/1wxshto/qwen3827b_vs_qwen38flashnext_as_agent_workers_on/)

### Long context reasoning (low confidence)

Treat million-token mode as an extension to validate, rather than a proven local operating point.

Scope: unresolved / warning. Scope needs review; the original claim does not establish a specific task ability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): context.reasoning

Judgment ID: judgment-6db95607e291642c

Conditions: Native 262,144; extension requires appropriate runtime configuration and memory.

Failure modes / limitations: Long reasoning traces, context pressure, retrieval misses.

Supporting sources: [Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B)

Contradictory or limiting sources: [Qwen3.8 27B xhigh independently profiled](https://artificialanalysis.ai/models/qwen3-8-27b)

### Coding.debugging (low confidence)

Long local debugging chats need enough context for the model's own output.

Scope: direct / warning. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-74505ce6779ad313

Conditions: TheTom/offlabel,stockllama.cpp,Q4_K_M;12-turn debugging loop at16,384context.

Failure modes / limitations: Empty content from turn6 as remaining context shrank;32,768context control completed without truncation.

Supporting sources: [Qwen3.8-27B local deployment probes](https://github.com/TheTom/offlabel/blob/main/models/qwen3.8-27b.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: A configuration-specific continuity warning, not a measured code-correctness score; hardware/quant/template changes require recheck.; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-5d5b9be0c4200c38

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

### Agent.tool_use (low confidence)

Base Qwen3.8-27B supports tool-use evaluation with substantial refusal and multi-turn gaps; adapter results do not transfer to the base.

Scope: direct / conditional. Exact base-checkpoint tool decisions in one reproducible setup.

Direct task IDs: agent.tool_use

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-159ca9252e0e8eff

Conditions: BF16, one AMD MI300X 192GB; vLLM ROCm, qwen3_xml parser, reasoning enabled, temperature 0.001, seed 300.

Failure modes / limitations: Aggregate function-calling accuracy hides refusal and missing-parameter weaknesses.

Supporting sources: [Qwen3.8-27B base and fine-tune tool-use evaluation](https://github.com/Nicolas-Formenton/qwen3.8-27b-finetune-eval)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: One hardware configuration and seed; measurement date and immutable base revision not pinned.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Dense hybrid Gated DeltaNet / gated-attention decoder with vision encoder |
| parameters | total billion: 27; active billion: 27; scope: 27B language model; official HF tensor metadata rounds complete artifact to 28B.; exact parameter count: Unknown / not established |
| context window | native tokens: 262144; extended tokens: 1000000; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; video; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

3 recorded access route(s); 2 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Apache-2.0

Restrictions: Retain copyright/license notices; comply with the license.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: allowed

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Planning estimate: 24–32GB GPU or 32–48GB unified memory with 4-bit weights, modest context; BF16 usually needs 64–80GB class memory.; 27B is the language-model declaration; HF serialized model is approximately 28B including additional components.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| novita | Standard / current | input: 0.42 USD / per 1 million tokens; output: 3 USD / per 1 million tokens; cached_input: 0.085 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |
| featherless | Standard / current | input: 0.4 USD / per 1 million tokens; output: 3 USD / per 1 million tokens; cached_input: 0.15 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |

## Recorded access routes

- novita / Serverless inference: officially_documented_not_execution_tested. Not established in this pass
- featherless / Featherless Developer: officially_documented_not_execution_tested. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Alibaba / Qwen

## Sources

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) · [Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B) · [Single-R9700 Qwen3.8 comparison](https://www.reddit.com/r/Qwen_AI/comments/1wxshto/qwen3827b_vs_qwen38flashnext_as_agent_workers_on/) · [Qwen3.8 27B xhigh independently profiled](https://artificialanalysis.ai/models/qwen3-8-27b)
