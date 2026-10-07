# GLM-5.3

**Creator:** Z.ai / Zhipu AI · **Family:** GLM5 · **Status:** active
**Verified:** 2026-10-06 · **Release:** Unknown

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Long horizon text coding (medium confidence)

Strong candidate for coding agents and text-based knowledge work with sufficient serving resources.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): agent.long_horizon; coding.repository_work

Judgment ID: judgment-7617cc55522b828a

Conditions: Preserve reasoning/template semantics; compare max effort using complete-task budgets.

Failure modes / limitations: Creator evaluations alter some anti-cheat checks and harnesses; cyber/terminal strengths do not establish visual capability.

Supporting sources: [GLM-5.3 model card](https://huggingface.co/zai-org/GLM-5.3) · [GLM5.3 max independently profiled](https://artificialanalysis.ai/models/glm-5-3)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Coding.debugging (low confidence)

Can repair a subset of hidden repository defects; use as an assisted audit, not a completeness guarantee.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-a007e05cd0f0f5f6

Conditions: Requested/accepted first-party tier; magnitude not verified. Scored row is complete rerun after voided quota failure.; Harness: Claude Code / Z.ai API; effort: max; effort evidence: first_party.; 105 planted defects across TypeScript VS Code extension (~28K lines) and React/Supabase LMS (~60K lines).; One agentic round per repository; native CLI/tools; same task prompt but nonidentical harnesses, contexts and budgets.; Blind diff-based answer-key grading; extra unplanted fixes excluded; private corpus/judgments prevent full external reproduction.

Failure modes / limitations: Many planted defects remained unresolved in the measured runs.; Run variance and harness differences prevent fine-grained cross-model ranking.

Supporting sources: [Bug Hunt Bench frozen measurements](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/data/benchmark.json) · [Bug Hunt Bench receipts and boundaries](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/README.md) · [Bug Hunt Bench individual configuration caveats](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/run-notes.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Result measures finding AND implementing fixes; do not relabel it as code-review recall or test-generation quality.; No matched independent contradiction located; partial successes and misses coexist.; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-e6af39a05dc0d081

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | MoE with DeepSeek-style sparse attention; same base model as GLM5.2, newer post-training |
| parameters | total billion: 753; active billion: 40; scope: 753B HF serialized artifact, 40B rounded active from independent catalog; runtime maintainer says ~743B/39B. Preserve discrepancy.; exact parameter count: Unknown / not established |
| context window | native tokens: 1000000; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | 128K tokens |
| modalities | input: text; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

7 recorded access route(s); 5 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: GLM-5.3 License

Restrictions: Retain notices.; MaaS operator above $10B aggregate trailing-12-month revenue must pass Z.ai security review before commercial use.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: conditional

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Datacenter / high-memory multi-GPU: ideal 4-bit full weights around 377GB plus substantial headroom.; Runtime-maintainer count ~743B/39B differs from serialized HF 753B / AA 40B; neither equals required VRAM.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| zai-api | Standard / current | input: 1.4 USD / per 1 million tokens; output: 4.4 USD / per 1 million tokens; cached_input: 0.26 USD / per 1 million tokens | Cache storage currently limited-time free. Former/current coding subscribers have protocol/account restrictions; check exact key. | 2026-10-07 |
| mistral-api | Standard / current | input: 1.4 USD / per 1 million tokens; output: 4.4 USD / per 1 million tokens; cached_input: 0.14 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |
| together | Standard / current | input: 1.4 USD / per 1 million tokens; output: 4.4 USD / per 1 million tokens; cached_input: 0.26 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |
| mistral-api | standard / historical | input: 1.4 USD / per_1000000_tokens; output: 4.4 USD / per_1000000_tokens; cached_input: 0.14 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Default standard tier; regional inference, batch and priority may have different rates. | 2026-10-06 |
| zai-api | standard / historical | input: 1.4 USD / per_1000000_tokens; output: 4.4 USD / per_1000000_tokens; cached_input: 0.26 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Cached-input storage currently labeled limited-time free; promotional expired rates are excluded. | 2026-10-06 |

## Recorded access routes

- zai-api / hosted metered api: documented_not_execution_tested. Not established in this pass
- zai-api / GLM Coding Plan: documented_not_execution_tested. Not established in this pass
- mistral-api / hosted metered api: documented_not_execution_tested. Not established in this pass
- together / hosted metered api: documented_not_execution_tested. Not established in this pass
- mistral-api / hosted_api: documented route; account eligibility unverified. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Z.ai / Zhipu AI
- zai-api / hosted_api: documented route; account eligibility unverified. Not established in this pass

## Sources

[GLM5.3 License](https://huggingface.co/zai-org/GLM-5.3/blob/main/LICENSE) · [GLM-5.3 model card](https://huggingface.co/zai-org/GLM-5.3) · [GLM5.3 max independently profiled](https://artificialanalysis.ai/models/glm-5-3) · [vLLM GLM5.3 recipe](https://recipes.vllm.ai/zai-org/GLM-5.3) · [GLM5.3 endpoint guide](https://docs.z.ai/guides/llm/glm-5.3)
