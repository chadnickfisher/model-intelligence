# GLM-5.3-Flash

**Creator:** Z.ai / Zhipu AI · **Family:** GLM5 · **Status:** active
**Verified:** 2026-10-06 · **Release:** Unknown

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Cost constrained multimodal agents (medium confidence)

Useful candidate where image-capable agents, MIT terms and lower token prices matter.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): vision.question_answering; agent.tool_use

Judgment ID: judgment-df9e1cacb62e57ae

Conditions: Exact hosted vs local runtime multimodal adapters differ; profile full task latency.

Failure modes / limitations: Verbose reasoning and measured 53 tokens/sec can dominate latency; no guarantee of flagship GLM5.3 task parity.

Supporting sources: [GLM-5.3-Flash model card](https://huggingface.co/zai-org/GLM-5.3-Flash) · [GLM5.3 Flash independently profiled](https://artificialanalysis.ai/models/glm-5-3-flash) · [Z.ai pricing](https://docs.z.ai/guides/overview/pricing)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Coding.scoped_edit (low confidence)

Useful evidence for exact, fully specified file changes in the measured tooling; semantic edits remain unestablished.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.scoped_edit

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-35e494a9a2bcd94d

Conditions: Provider route: zai; 8 contributing harness families; detailed effort mix not extracted.; API/checkpoint identity follows source's exact named model; underlying quantization not supplied.; 226 tasks; shell/native editing tools allowed.; Score combines 75% initial exactness and 25% final exactness after permitted recovery.; Record describes a model route with mixed harnesses; do not interpret as pass@1 or a causal model ranking.

Failure modes / limitations: Some initial or final file trees failed exact comparison; this aggregate does not isolate the failure mechanism.

Supporting sources: [Explicit Edit Benchmark public data](https://huggingface.co/datasets/alexshpunt/explicit-edit-benchmark) · [Explicit Edit methodology](https://github.com/alexshpunt/explicit-edit-benchmark/blob/main/docs/methodology.md) · [Explicit Edit task definitions](https://github.com/alexshpunt/explicit-edit-benchmark/blob/main/docs/tasks.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: No matched independent contradictory evaluation located. This source establishes a narrow measured route, not a general ability ranking.; Potential transfer risk, not measured semantic failure: test-free byte matching does not establish a correct code change.; Research provenance: history/research/2026-10-07/coding-input.json :: scoped_debugging:glm-5-3-flash-scoped-mechanical; Confidence concerns this bounded claim, not a capability score.

### Coding.debugging (low confidence)

Can repair a subset of hidden repository defects; use as an assisted audit, not a completeness guarantee.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-56713cac2c5e623e

Conditions: glm-5.3-flash;1M requested;2.1.269 then2.1.270; token/context parity unverified.; Harness: Claude Code / Z.ai API; effort: max; effort evidence: verified_ceiling.; 105 planted defects across TypeScript VS Code extension (~28K lines) and React/Supabase LMS (~60K lines).; One agentic round per repository; native CLI/tools; same task prompt but nonidentical harnesses, contexts and budgets.; Blind diff-based answer-key grading; extra unplanted fixes excluded; private corpus/judgments prevent full external reproduction.

Failure modes / limitations: Many planted defects remained unresolved in the measured runs.; Run variance and harness differences prevent fine-grained cross-model ranking.

Supporting sources: [Bug Hunt Bench frozen measurements](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/data/benchmark.json) · [Bug Hunt Bench receipts and boundaries](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/README.md) · [Bug Hunt Bench individual configuration caveats](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/run-notes.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Result measures finding AND implementing fixes; do not relabel it as code-review recall or test-generation quality.; No matched independent contradiction located; partial successes and misses coexist.; Research provenance: history/research/2026-10-07/coding-input.json :: scoped_debugging:glm-5-3-flash-debug-bughunt; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-1d57d36d40d69678

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Research provenance: history/research/2026-10-07/coding-input.json :: review_tests_frontend:frontend-arena-glm-5-3-flash; Confidence concerns this bounded claim, not a capability score.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Native multimodal MoE combining sparse and linear attention with mHC |
| parameters | total billion: 320; active billion: 18; scope: creator-declared count; see notes; exact parameter count: Unknown / not established |
| context window | native tokens: 1000000; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

5 recorded access route(s); 3 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: MIT

Restrictions: Retain copyright/license notices; comply with the license.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: allowed

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Planning estimate: 192–256GB aggregate memory for supported 4-bit with modest batching; FP8 requires over 320GB weights plus headroom.; HF serialized metadata rounds to 321B; official model-card declaration is 320B.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| together | Standard / current | input: 0.15 USD / per 1 million tokens; output: 0.5 USD / per 1 million tokens; cached_input: 0.03 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |
| zai-api | Standard / current | input: 0.15 USD / per 1 million tokens; output: 0.5 USD / per 1 million tokens; cached_input: 0.03 USD / per 1 million tokens | Cache storage currently limited-time free. Former/current coding subscribers have protocol/account restrictions; check exact key. | 2026-10-07 |
| zai-api | standard / historical | input: 0.15 USD / per_1000000_tokens; output: 0.5 USD / per_1000000_tokens; cached_input: 0.03 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Cached-input storage currently labeled limited-time free; promotional expired rates are excluded. | 2026-10-06 |

## Recorded access routes

- zai-api / GLM Coding Plan: documented_not_execution_tested. Not established in this pass
- zai-api / hosted metered api: documented_not_execution_tested. Not established in this pass
- together / hosted metered api: documented_not_execution_tested. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Z.ai / Zhipu AI
- zai-api / hosted_api: documented route; account eligibility unverified. Not established in this pass

## Sources

[GLM5.3 Flash MIT license](https://huggingface.co/zai-org/GLM-5.3-Flash/blob/main/LICENSE) · [GLM-5.3-Flash model card](https://huggingface.co/zai-org/GLM-5.3-Flash) · [GLM5.3 Flash independently profiled](https://artificialanalysis.ai/models/glm-5-3-flash) · [Z.ai pricing](https://docs.z.ai/guides/overview/pricing) · [GLM5.3 Flash endpoint guide](https://docs.z.ai/guides/vlm/glm-5.3-flash)
