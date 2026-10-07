# Gemini 3.8 Flash

**Creator:** Google DeepMind · **Family:** Gemini · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-02

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Fast multimodal assistant and bounded coding tasks (medium confidence)

Strong candidate when throughput matters and outputs can be tested.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): vision.question_answering; coding.scoped_edit

Judgment ID: judgment-262c08414297adcf

Conditions: high reasoning; Google API; high; temperature 1; Google API; max output 65,536; high; Google API

Failure modes / limitations: Not established in this pass

Supporting sources: [Artificial Analysis gemini-3-8-flash](https://artificialanalysis.ai/models/gemini-3-8-flash) · [Vals AI gemini-3.8-flash](https://www.vals.ai/models/google_gemini-3.8-flash)

Contradictory or limiting sources: [Gemini 3.8 Flash model card](https://deepmind.google/models/model-cards/gemini-3-8-flash/) · [Vals AI gemini-3.8-flash](https://www.vals.ai/models/google_gemini-3.8-flash)

Evidence notes: task-conditioned synthesis; no inference runs performed; Observation obs-62d94da56cdb: Fast streamed decoding in the observed benchmark service.; Observation obs-7445edb36893: Competitive contained coding tasks, with much weaker results on harder general terminal work.; Observation obs-a6b7a76a516c: Supports demanding visual/scientific question answering in independent evaluation.; Observation obs-623d3b669e5c: Provider discloses hallucinations, occasional timeouts, and increased tokens at higher effort; multilingual safety regressed versus 3.7.

### Unsupervised long horizon terminal execution (medium confidence)

Conditional; use tests and checkpointing rather than assuming benchmark coding strength transfers.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: agent.long_horizon

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-46e287976a5cc041

Conditions: high; temperature 1; Google API; max output 65,536

Failure modes / limitations: Not established in this pass

Supporting sources: [Vals AI gemini-3.8-flash](https://www.vals.ai/models/google_gemini-3.8-flash)

Contradictory or limiting sources: [Vals AI gemini-3.8-flash](https://www.vals.ai/models/google_gemini-3.8-flash) · [Gemini 3.8 Flash model card](https://deepmind.google/models/model-cards/gemini-3-8-flash/)

Evidence notes: task-conditioned synthesis; no inference runs performed; Observation obs-7445edb36893: Competitive contained coding tasks, with much weaker results on harder general terminal work.; Observation obs-623d3b669e5c: Provider discloses hallucinations, occasional timeouts, and increased tokens at higher effort; multilingual safety regressed versus 3.7.

### Coding.scoped_edit (low confidence)

Useful evidence for exact, fully specified file changes in the measured tooling; semantic edits remain unestablished.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.scoped_edit

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-d060233bb88428f3

Conditions: Provider route: gemini; 1 contributing harness families; detailed effort mix not extracted.; API/checkpoint identity follows source's exact named model; underlying quantization not supplied.; 226 tasks; shell/native editing tools allowed.; Score combines 75% initial exactness and 25% final exactness after permitted recovery.; Record describes a model route with mixed harnesses; do not interpret as pass@1 or a causal model ranking.

Failure modes / limitations: Some initial or final file trees failed exact comparison; this aggregate does not isolate the failure mechanism.

Supporting sources: [Explicit Edit Benchmark public data](https://huggingface.co/datasets/alexshpunt/explicit-edit-benchmark) · [Explicit Edit methodology](https://github.com/alexshpunt/explicit-edit-benchmark/blob/main/docs/methodology.md) · [Explicit Edit task definitions](https://github.com/alexshpunt/explicit-edit-benchmark/blob/main/docs/tasks.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: No matched independent contradictory evaluation located. This source establishes a narrow measured route, not a general ability ranking.; Potential transfer risk, not measured semantic failure: test-free byte matching does not establish a correct code change.; Research provenance: history/research/2026-10-07/coding-input.json :: scoped_debugging:gemini-3-8-flash-scoped-mechanical; Confidence concerns this bounded claim, not a capability score.

### Coding.debugging (low confidence)

Can repair a subset of hidden repository defects; use as an assisted audit, not a completeness guarantee.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-37a2484d83177e9d

Conditions: CLI version/context/compaction unrecoverable; parity between three runs not established.; Harness: Antigravity CLI; effort: high; effort evidence: verified_ceiling.; 105 planted defects across TypeScript VS Code extension (~28K lines) and React/Supabase LMS (~60K lines).; One agentic round per repository; native CLI/tools; same task prompt but nonidentical harnesses, contexts and budgets.; Blind diff-based answer-key grading; extra unplanted fixes excluded; private corpus/judgments prevent full external reproduction.

Failure modes / limitations: Many planted defects remained unresolved in the measured runs.; Run variance and harness differences prevent fine-grained cross-model ranking.

Supporting sources: [Bug Hunt Bench frozen measurements](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/data/benchmark.json) · [Bug Hunt Bench receipts and boundaries](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/README.md) · [Bug Hunt Bench individual configuration caveats](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/run-notes.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Result measures finding AND implementing fixes; do not relabel it as code-review recall or test-generation quality.; No matched independent contradiction located; partial successes and misses coexist.; Research provenance: history/research/2026-10-07/coding-input.json :: scoped_debugging:gemini-3-8-flash-debug-bughunt; Confidence concerns this bounded claim, not a capability score.

### Coding.refactoring (medium confidence)

Meaningful repository refactoring capability, with fewer than half of tasks resolved.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.refactoring

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-cab8e45e5c2e7550

Conditions: 70 tasks, 10 production repositories, 6 languages; Harbor/Modal sandboxes. Resolve requires unchanged tests, zero regressions, and every mandatory Opus 4.5-judged rubric.

Failure modes / limitations: Incomplete extraction, unwired callers, stale implementations/artifacts; failure taxonomy is pooled, not per-model.

Supporting sources: [SWE Atlas - Refactoring](https://labs.scale.com/leaderboard/sweatlas-refactoring)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Harnesses differ; uncertainty overlaps, so no significant ordering claimed. Preserve xHigh as board label. Intro's below 50% statement is stale. Gemini 3.1 Pro 33.81±6.64 is withheld pending preview-ID mapping.; Research provenance: history/research/2026-10-07/coding-input.json :: architecture_refactoring:R03; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (low confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-751724bc0907712b

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Research provenance: history/research/2026-10-07/coding-input.json :: review_tests_frontend:frontend-arena-gemini-3-8-flash; Confidence concerns this bounded claim, not a capability score.

### Coding.review (medium confidence)

Useful bounded reviewer when requirements and focused diffs are supplied; security coverage remains incomplete.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.review

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-155aaea76681afab

Conditions: Explicit-rule tasks are saturated; do not generalize their perfect score.; Named release matches; preserve source-specific provider, snapshot and precision limitations.

Failure modes / limitations: Security misses and occasional unparsable output.

Supporting sources: [Living AI code review benchmark](https://diffdojo.com/benchmark.html) · [Can Jev make a code review agent cheaper and faster?](https://github.com/gemanor/jev-code-review-benchmark/blob/95932b43f227dc759a7147d4e2d371388a148eb8/README.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Research provenance: history/research/2026-10-07/coding-input.json :: review_tests_frontend:review-gemini38; Confidence concerns this bounded claim, not a capability score.

### Measured generation behavior (medium confidence)

Fast streamed decoding in the observed benchmark service. Measurements: {"output_tokens_per_second": 241.9}. These describe the cited benchmark configuration only.

Scope: performance / conditional. Cost, deployment or throughput observation; not a task capability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-4d183583f2850a0e

Conditions: high reasoning; Google API

Failure modes / limitations: Not established in this pass

Supporting sources: [Artificial Analysis gemini-3-8-flash](https://artificialanalysis.ai/models/gemini-3-8-flash)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Excludes time to first token and tool-loop overhead; not an SLA.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 1048576 |
| maximum output | 65536 |
| modalities | input: text; image; video; audio; PDF; output: text |
| language support | Unknown / not established |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

7 recorded access route(s); 3 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Not established / proprietary terms must be checked

Restrictions: Not established in this pass

Commercial use: Unknown / not established

Redistribution: Unknown / not established

Hosted service: Unknown / not established

Local weights/runtime availability: unavailable

Hardware: Not established in this pass

Local conditions: Not established in this pass

## Gaps and caveats

- Full language coverage list
- Architecture beyond published dependency
- Private production latency/SLAs

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| google-developer-api | paid_standard / current | input: 0.75 USD / per_1M_tokens; output_including_thinking: 3.75 USD / per_1M_tokens; cache_read: 0.075 USD / per_1M_tokens | Not established in this pass | 2026-10-06 |
| google-developer-api | paid_batch / current | input: 0.375 USD / per_1M_tokens; output_including_thinking: 1.875 USD / per_1M_tokens | Not established in this pass | 2026-10-06 |
| google-developer-api | paid_standard / current | input: 1.5 USD / per_1M_tokens; output_including_thinking: 7.5 USD / per_1M_tokens; cache_read: 0.15 USD / per_1M_tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- google-cloud / Gemini Enterprise Agent Platform: officially_documented_not_execution_tested. Not established in this pass
- google-developer-api / Gemini Developer API / Google AI Studio: officially_documented_not_execution_tested. Not established in this pass
- google-ai / Gemini app / Search AI Mode / Sheets: Conditional consumer/client product; exact account entitlement unverified. Model-specific launch documents AI Pro/Ultra access. Current app help permits Flash family on all plans, without exact minor-version mapping.
- google-developer-api / first-party-api: documented route; account eligibility unverified. Not established in this pass
- google-ai-studio / Google AI Studio: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass
- google-antigravity / Google Antigravity: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass
- google-consumer / Gemini app / Google AI plans: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass

## Sources

[Gemini 3.8 Flash model card](https://deepmind.google/models/model-cards/gemini-3-8-flash/) · [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Gemini 3.8 Flash API model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash) · [Gemini API release notes](https://ai.google.dev/gemini-api/docs/changelog)
