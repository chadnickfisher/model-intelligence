# MiniMax M3

**Creator:** MiniMax · **Family:** MiniMax M · **Status:** active
**Verified:** 2026-10-06 · **Release:** Unknown

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Multimodal long context work (medium confidence)

A candidate for cost-sensitive image/video coding and work agents; compare using the >512k price band when relevant.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.repository_work; agent.tool_use; context.reasoning

Judgment ID: judgment-733be35f32bab45e

Conditions: Thinking can be enabled, adaptive or disabled; paid hosting terms are separate from weight license.

Failure modes / limitations: Long-context requests cost more; reported attention speedups are creator comparisons against M2, not universal application speedups.

Supporting sources: [MiniMax M3 model card](https://huggingface.co/MiniMaxAI/MiniMax-M3) · [MiniMax M3 independently profiled](https://artificialanalysis.ai/models/minimax-m3) · [MiniMax API pricing](https://platform.minimax.io/docs/pricing/overview)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Coding.scoped_edit (low confidence)

Useful evidence for exact, fully specified file changes in the measured tooling; semantic edits remain unestablished.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.scoped_edit

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-93c890d81197f7fc

Conditions: Provider route: opencode-go; 3 contributing harness families; detailed effort mix not extracted.; API/checkpoint identity follows source's exact named model; underlying quantization not supplied.; 226 tasks; shell/native editing tools allowed.; Score combines 75% initial exactness and 25% final exactness after permitted recovery.; Record describes a model route with mixed harnesses; do not interpret as pass@1 or a causal model ranking.

Failure modes / limitations: Some initial or final file trees failed exact comparison; this aggregate does not isolate the failure mechanism.

Supporting sources: [Explicit Edit Benchmark public data](https://huggingface.co/datasets/alexshpunt/explicit-edit-benchmark) · [Explicit Edit methodology](https://github.com/alexshpunt/explicit-edit-benchmark/blob/main/docs/methodology.md) · [Explicit Edit task definitions](https://github.com/alexshpunt/explicit-edit-benchmark/blob/main/docs/tasks.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: No matched independent contradictory evaluation located. This source establishes a narrow measured route, not a general ability ranking.; Potential transfer risk, not measured semantic failure: test-free byte matching does not establish a correct code change.; Confidence concerns this bounded claim, not a capability score.

### Coding.debugging (low confidence)

Evidence supports some issue-directed Odin repairs under a fixed, patch-only protocol.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-fd22697316fb56f3

Conditions: 168eligible public Odin issues; supplied source scope; one scored patch; no execution feedback to generator.; Exact request budget/API run date not independently audited.

Failure modes / limitations: A patch applying or reproducing an issue does not ensure complete repair.

Supporting sources: [OdinEval program repair](https://arxiv.org/html/2608.18595v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Preprint; check released manifest before stronger confidence. No universal language or harness transfer.; Confidence concerns this bounded claim, not a capability score.

### Coding.refactoring (medium confidence)

Credible supervised multi-file refactoring candidate; structural retrieval helps, and green self-written tests are insufficient.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.refactoring

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-43822338c45cc056

Conditions: Single-run campaigns; descriptive What/Where/How prompts, isolated terminal agents via OpenRouter/Copilot-supported platform, AST unit-test scoring. Tasks span nine repositories and2–31 files. Approximate reported cost/success $0.65/$0.66.; Claude Code; about 2h 40m implementation; Opus 4.8 used as second reviewer. Paid MiniMax partnership disclosed.

Failure modes / limitations: 19% still failed with retrieval. AST structural tests are narrower than a full behavioral proof.; Independent review reportedly caught save-format incompatibility and duplicated critical-hit scaling despite green self-written tests; six partial and six untouched fixes.

Supporting sources: [RefactorPlatform](https://arxiv.org/html/2609.04898v1) · [Testing MiniMax M3 on real tasks](https://andlukyane.com/blog/minimax-m3)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: One campaign, no uncertainty estimate; results tied to retrieval/scaffold. Do not transfer qwen3.6-flash or kimi-k2.6 results to current siblings. deepseek-v4-pro 77/89% has no 0813 pin and is excluded.; One author/project, no independent replication. A useful failure warning, not a measured population failure rate.; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-a2fa0a68ce24b775

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Native multimodal MoE with MiniMax Sparse Attention |
| parameters | total billion: 428; active billion: 23; scope: creator-declared count; see notes; exact parameter count: Unknown / not established |
| context window | native tokens: 1000000; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; video; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

5 recorded access route(s); 6 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: MiniMax Community License

Restrictions: Retain copyright and permission notices.; Commercial use: branding plus one-time notice; >$20M yearly product/service revenue requires prior written authorization.; Prohibited-use appendix applies, including any military use.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: conditional

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Datacenter / high-memory workstation: ideal 4-bit roughly 214GB; plan >=256GB aggregate memory plus workload headroom.; Card ~428B versus HF serialized 427B and alternate MXFP8 artifact ~440B; scope/rounding differs. Supported quantized backend required.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| together | Standard / current | input: 0.3 USD / per 1 million tokens; output: 1.2 USD / per 1 million tokens; cached_input: 0.06 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |
| minimax-api | priority_long / current | input: 0.8999999999999999 USD / per_1000000_tokens; output: 3.5999999999999996 USD / per_1000000_tokens; cached_input: 0.18 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Input length >512k. Current displayed effective rates, not struck-through list prices. | 2026-10-06 |
| minimax-api | priority_short / current | input: 0.44999999999999996 USD / per_1000000_tokens; output: 1.7999999999999998 USD / per_1000000_tokens; cached_input: 0.09 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Input length <=512k. Current displayed effective rates, not struck-through list prices. | 2026-10-06 |
| minimax-api | standard_short / current | input: 0.3 USD / per_1000000_tokens; output: 1.2 USD / per_1000000_tokens; cached_input: 0.06 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Input length <=512k. Current displayed effective rates, not struck-through list prices. | 2026-10-06 |
| minimax-api | standard_long / current | input: 0.6 USD / per_1000000_tokens; output: 2.4 USD / per_1000000_tokens; cached_input: 0.12 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Input length >512k. Current displayed effective rates, not struck-through list prices. | 2026-10-06 |
| together | standard displayed serverless / current | input: 0.3 USD / per 1M tokens; cached_input: 0.06 USD / per 1M tokens; output: 1.2 USD / per 1M tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- minimax-api / Legacy Token Plan: documented_not_execution_tested. Not established in this pass
- together / hosted metered api: documented_not_execution_tested. Not established in this pass
- minimax-api / hosted metered api: documented_not_execution_tested. Not established in this pass
- minimax-api / hosted_api: documented route; account eligibility unverified. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is MiniMax

## Sources

[MiniMax M3 Community License](https://huggingface.co/MiniMaxAI/MiniMax-M3/blob/main/LICENSE) · [MiniMax M3 model card](https://huggingface.co/MiniMaxAI/MiniMax-M3) · [MiniMax M3 independently profiled](https://artificialanalysis.ai/models/minimax-m3) · [MiniMax API pricing](https://platform.minimax.io/docs/pricing/overview)
