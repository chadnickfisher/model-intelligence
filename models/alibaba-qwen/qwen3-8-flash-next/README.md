# Qwen3.8-Flash-Next

**Creator:** Alibaba / Qwen · **Family:** Qwen3.8 · **Status:** preview
**Verified:** 2026-10-06 · **Release:** 2026-08-26

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Efficient agent workers (medium confidence)

Interesting for local tool-heavy workers when offloading and license terms fit.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): agent.tool_use; coding.repository_work

Judgment ID: judgment-dfc392840f6a0569

Conditions: Benchmark the exact quantized runtime; medium effort performed better than xhigh in one looping case.

Failure modes / limitations: Runtime-specific grammar failures, thinking loops, CPU/SSD bottlenecks.

Supporting sources: [Qwen3.8-Flash-Next model card](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) · [Qwen3.8 Flash-Next independently profiled](https://artificialanalysis.ai/models/qwen3-8-flash-next) · [Single-R9700 Qwen3.8 comparison](https://www.reddit.com/r/Qwen_AI/comments/1wxshto/qwen3827b_vs_qwen38flashnext_as_agent_workers_on/)

Contradictory or limiting sources: [Single-R9700 Qwen3.8 comparison](https://www.reddit.com/r/Qwen_AI/comments/1wxshto/qwen3827b_vs_qwen38flashnext_as_agent_workers_on/)

### Coding.frontend (low confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-2e3d7688d669fd57

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Research provenance: history/research/2026-10-07/coding-input.json :: review_tests_frontend:frontend-arena-qwen3-8-flash-next; Confidence concerns this bounded claim, not a capability score.

### Commercial coding assistant hosting (medium confidence)

Do not assume permissive self-hosted commercial availability.

Scope: performance / warning. Cost, deployment or throughput observation; not a task capability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-89c7c704304def1d

Conditions: Check whether business is MaaS or an independent coding/office assistant.

Failure modes / limitations: License choice can block a deployment even when weights are downloadable.

Supporting sources: [Qwen Community License 1.0](https://huggingface.co/Qwen/Qwen3.8-Flash-Next/blob/main/LICENSE)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Conservative baseline confidence: broader convergence has not been independently audited.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Hybrid MoE: Gated DeltaNet, Qwen Sparse Attention, n-gram lookup embeddings, gated residual, MTP |
| parameters | total billion: 180; active billion: 6; scope: creator-declared count; see notes; exact parameter count: Unknown / not established; components billion: backbone: 125; ngram embeddings: 51; mtp: 4 |
| context window | native tokens: 262144; extended tokens: 1000000; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; video; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

2 recorded access route(s); 1 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Qwen Community License 1.0

Restrictions: Retain notices.; Separate commercial license for MaaS or independent coding/office AI assistant businesses; internal-use exemption.; Display model name above 100M MAU or $20M monthly product/service revenue; see exact definitions.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: conditional

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Planning: roughly 100–128GB aggregate memory for a full 4-bit layout; specialized SSD/RAM offload can run on smaller accelerators.; Creator separates 125B backbone, 51B n-gram table and 4B MTP. A 32GB GPU + 64GB RAM practitioner setup relies on SSD tables, CPU experts, patched runtime and reduced effective resident weight footprint.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| featherless | Standard / current | input: 0.15 USD / per 1 million tokens; output: 0.5 USD / per 1 million tokens; cached_input: 0.03 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |

## Recorded access routes

- featherless / Featherless Developer: officially_documented_not_execution_tested. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Alibaba / Qwen

## Sources

[Qwen Community License 1.0](https://huggingface.co/Qwen/Qwen3.8-Flash-Next/blob/main/LICENSE) · [Qwen3.8-Flash-Next model card](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) · [Single-R9700 Qwen3.8 comparison](https://www.reddit.com/r/Qwen_AI/comments/1wxshto/qwen3827b_vs_qwen38flashnext_as_agent_workers_on/) · [Qwen3.8 Flash-Next independently profiled](https://artificialanalysis.ai/models/qwen3-8-flash-next)
