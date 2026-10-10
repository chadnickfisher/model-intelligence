# Grok 4.7

**Creator:** xAI / SpaceXAI · **Family:** Grok · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-21

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Agentic coding and knowledge workflows (medium confidence)

Credible candidate; medium confidence for task-fit. AA's xhigh snapshot improves Terminal-Bench 4.0 from 21% (4.6 high) to 26%, but costs roughly twice per evaluated task.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.repository_work; research.synthesis

Judgment ID: judgment-445f99a05ebe5177

Conditions: Grok4.7 xhigh vs Grok4.6 high, first-party API

Failure modes / limitations: Not established in this pass

Supporting sources: [artificialanalysis.ai](https://artificialanalysis.ai/models/comparisons/grok-4-7-vs-grok-4-6)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Observation obs-281c2bae7ad0: AA Intelligence Index v4.3.2 and component tasks

### Coding.debugging (low confidence)

Can repair a subset of hidden repository defects; use as an assisted audit, not a completeness guarantee.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-2216eba8e5c983c7

Conditions: Native Grok CLI; subagent counts varied between runs and regime parity was not fully verifiable.; Harness: Grok Build CLI (ACP); effort: xhigh; effort evidence: verified.; 105 planted defects across TypeScript VS Code extension (~28K lines) and React/Supabase LMS (~60K lines).; One agentic round per repository; native CLI/tools; same task prompt but nonidentical harnesses, contexts and budgets.; Blind diff-based answer-key grading; extra unplanted fixes excluded; private corpus/judgments prevent full external reproduction.

Failure modes / limitations: Many planted defects remained unresolved in the measured runs.; Run variance and harness differences prevent fine-grained cross-model ranking.

Supporting sources: [Bug Hunt Bench frozen measurements](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/data/benchmark.json) · [Bug Hunt Bench receipts and boundaries](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/README.md) · [Bug Hunt Bench individual configuration caveats](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/run-notes.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Result measures finding AND implementing fixes; do not relabel it as code-review recall or test-generation quality.; No matched independent contradiction located; partial successes and misses coexist.; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-ecc0a660e49ca126

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.; Fresh October 8 snapshot is 1658 ±12 from 3, 082 votes, rank spread 11–21. This remains preference evidence and is not the reason for the separate executable-frontend assessment.

### Coding.debugging (low confidence)

Repairs were highly prompt-sensitive in a small test: the familiar JavaScript median formulation passed all five checks, while the Python reformulation repeatedly retained defects.

Scope: direct / conditional. Exact task and recorded conditions only; no transfer from benchmark components to neighboring tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-018736055ee45c29

Conditions: Five responses per code prompt, default settings, output code executed against five assertions; actual run date and route undisclosed.

Failure modes / limitations: Python outputs never fixed even-length averaging or empty input; only two of five fixed lexicographic sorting.

Supporting sources: [Grok 4.7 Review: Self-Checking](https://developer.puter.com/blog/grok-4-7-review/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: The Python mean was 2.4 defects fixed of 5; this does not measure test generation or prove an internal self-checking mechanism.

### Vision.question_answering (medium confidence)

Useful for questions requiring visual relationships and derived answers, but needs material checking under the measured image-question setup.

Scope: direct / conditional. Exact task and recorded public setup only; no transfer from compound scores or neighboring tasks.

Direct task IDs: vision.question_answering

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-0ba4cb2ee9068e43

Conditions: Roboflow current visual-reasoning task; Grok 4.7 low/high native effort;3runs each; fixed public examples require interpreting diagrams and images.; Gemini 3.5 Flash temperature 0 judges against ground truth; strict normalized-match score also provided; sample count, resolution, model-run date, immutable snapshot and exact inference route undisclosed.

Failure modes / limitations: Mean judged accuracy 64.2%low and 66.9%high; additional effort did not establish uniformly correct interpretation.

Supporting sources: [Visual Reasoning Benchmark](https://playground.roboflow.com/evals/visual-reasoning) · [Vision Evals methodology](https://playground.roboflow.com/evals)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Half-range bars and observed run range are not confidence intervals; model-page six-task composite not used.

### Coding.scoped_edit (low confidence)

Useful bounded script generation still requires runtime validation: the tested backup scripts worked, while every first-pass non-root nginx manifest crash-looped despite clean schema validation.

Scope: direct / conditional. Exact task and recorded conditions only; no transfer from benchmark components to neighboring tasks.

Direct task IDs: coding.scoped_edit

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-50e15107482eac41

Conditions: Josphat Mutai tested three prompts three times each at default high and low via xAI API on September 25.; Bash was tested with stubbed commands; Terraform was only validated/formatted, not deployed.

Failure modes / limitations: All six nginx manifests omitted necessary writable mounts; generated scripts generally used the current directory for backups.

Supporting sources: [Grok 4.7 real DevOps results](https://computingforgeeks.com/grok-4-7-tested/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Do not convert the mixed 6-of-9 checks total into a narrow function, repository or security rate.

### Coding.debugging (low confidence)

A single log-assisted follow-up repaired a crashing non-root nginx manifest on the tested cluster; the result supports a narrow corrective workflow, not general autonomous recovery.

Scope: direct / conditional. Exact task and recorded conditions only; no transfer from benchmark components to neighboring tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-539a094d8fd79d60

Conditions: Original failed manifest and two-line error supplied; xAI API, September 25, k3s 1.36.4 on Ubuntu 26.04.

Failure modes / limitations: The repaired manifest relies on the runtime allowing unprivileged port 80; its added capability line did not confer the claimed effective capability.

Supporting sources: [Grok 4.7 real DevOps results](https://computingforgeeks.com/grok-4-7-tested/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: The author deployed the repaired output and observed HTTP 200. One repair is not a repeat estimate.

### Coding.repository_work, coding.architecture, coding.refactoring, coding.tests (low confidence)

Attributable Cursor users report both useful Rust multi-file work and architecture/refactor drift; the anecdotes do not isolate model quality or establish behavior-preserving refactoring.

Scope: unresolved / unknown. Unresolved compound evidence retained for navigation only; no direct task endorsement.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.repository_work; coding.architecture; coding.refactoring; coding.tests

Judgment ID: judgment-545f5cc024f99a3d

Conditions: Exact effort, serving route, patches and acceptance checks were not disclosed.

Failure modes / limitations: Unnecessary abstractions, unreadable refactors and unapplied changes are reported, without controlled reproduction.

Supporting sources: [Grok 4.7 Cursor Rust-workflow discussion](https://www.reddit.com/r/cursor/comments/1wrktgc/am_i_the_only_one_who_thinks_grok_47_is_actually/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Mixed user experiences are not sufficient by themselves for an aggregate Disputed rating.

### Coding.frontend (low confidence)

Grok Build xhigh produced usable visual code and a game satisfying the explicit brief, but visible animation, camera and interaction-polish problems required direct rendered-output review.

Scope: direct / conditional. Exact task and recorded conditions only; no transfer from benchmark components to neighboring tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-a610fa0194677cb5

Conditions: One attempt per brief. Browser self-check was forbidden for three initial builds and required/available for the separate Hill Climb game.

Failure modes / limitations: Reported faults included disconnected animation layers, a camera losing the rocket, abrupt coasting and floating background scenery.

Supporting sources: [Grok 4.7 Hill Climb build test](https://www.bitsminds.com/news/claude-opus-5-vs-gpt-5-6-sol-vs-grok-4-7-hill-climb-2026) · [Grok 4.7 three visual build briefs](https://www.bitsminds.com/news/grok-4-7-vs-fable-5-1-vs-astra-6-build-off-2026)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: All explicit Hill Climb requirements passed. Its 6/20 subjective score is not a functional failure rate; exact prompts and blinded grading were unavailable.

### Vision.grounding (medium confidence)

Can emit normalized boxes for described image classes, but localization is weak enough that precise coordinates need substantial correction.

Scope: direct / conditional. Exact task and recorded public setup only; no transfer from compound scores or neighboring tasks.

Direct task IDs: vision.grounding

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-b638cfe00b628c73

Conditions: Roboflow zero-shot object detection; requested labels and normalized[ymin,xmin,ymax,xmax]coordinates; Grok 4.7 low/high;3runs each.; Deterministic box-overlap mAP; sample/object denominators, image resolution, immutable checkpoint and route undisclosed.

Failure modes / limitations: mAP@50= 40.4% low / 41.2% high; mAP@75=23.0%/23.7% and mAP@50:95=23.6%/24.4%.

Supporting sources: [Object Detection Benchmark](https://playground.roboflow.com/evals/object-detection) · [Vision Evals methodology](https://playground.roboflow.com/evals)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: mAP is not a fraction of task successes; no GUI-action or segmentation conclusion.

### Low latency assistance (medium confidence)

Not a latency-first default at high reasoning effort; evaluate low effort or alternatives.

Scope: performance / warning. Cost, deployment or throughput observation; not a task capability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-4353bef7f2c69a6b

Conditions: Grok4.7 xhigh vs Grok4.6 high, first-party API

Failure modes / limitations: Not established in this pass

Supporting sources: [artificialanalysis.ai](https://artificialanalysis.ai/models/comparisons/grok-4-7-vs-grok-4-6)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Observation obs-281c2bae7ad0: AA Intelligence Index v4.3.2 and component tasks

### Measured generation behavior (medium confidence)

AA Intelligence Index v4.3.2 and component tasks Measurements: {"output_tokens_per_task": [81000, 36000]}. These describe the cited benchmark configuration only.

Scope: performance / conditional. Cost, deployment or throughput observation; not a task capability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-8d9ae7f7de890d41

Conditions: Grok4.7 xhigh vs Grok4.6 high, first-party API

Failure modes / limitations: Not established in this pass

Supporting sources: [artificialanalysis.ai](https://artificialanalysis.ai/models/comparisons/grok-4-7-vs-grok-4-6)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Different reasoning settings; broad quality gain is not across every task. Benchmark cost reflects its workload and cannot price user tasks.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 500000 |
| maximum output | Unknown / not established |
| modalities | input: text; image; output: text |
| language support | Unknown / not established |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

6 recorded access route(s); 3 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: proprietary service terms

Restrictions: Not established in this pass

Commercial use: Unknown / not established

Redistribution: Unknown / not established

Hosted service: Unknown / not established

Local weights/runtime availability: unavailable

Hardware: Not established in this pass

Local conditions: Not established in this pass

## Gaps and caveats

- Real-time facts require search tools; model alone has no live event access.
- Do not equate published context capacity with perfect long-context recall.
- Price depends on prompt length, tool charges and actual reasoning-token usage.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| opencode-zen | prompt >200k / current | input: 4 USD / per 1M tokens; cached_input: 1 USD / per 1M tokens; output: 12 USD / per 1M tokens | Not established in this pass | 2026-10-06 |
| opencode-zen | prompt <=200k / current | input: 2 USD / per 1M tokens; cached_input: 0.5 USD / per 1M tokens; output: 6 USD / per 1M tokens | Not established in this pass | 2026-10-06 |
| xai | standard, short context / current | input: 2 USD / per 1M tokens; cached_input: 0.5 USD / per 1M tokens; output: 6 USD / per 1M tokens | Higher-context pricing exists above 200k; exact boundary/rates require reconciliation with general page. These are base displayed rates.; not stated | 2026-10-06 |

## Recorded access routes

- xai / SuperGrok shared pool: shared_API_allowance_described_but_exact_auth_entitlement_unverified. Not established in this pass
- xai / Grok / SuperGrok: documented_not_execution_tested. Not established in this pass
- opencode-zen / gateway metered api: documented_not_execution_tested. Not established in this pass
- xai / hosted metered api: documented_not_execution_tested. Not established in this pass
- google-cloud / Gemini Enterprise Agent Platform / Vertex partner model: preview_fixed_quota. Not established in this pass
- xai / Grok 4.7 Fast in Cursor / Grok Build: documented_not_execution_tested. Not established in this pass

## Sources

[artificialanalysis.ai](https://artificialanalysis.ai/models/grok-4-7-high) · [docs.x.ai](https://docs.x.ai/developers/models/grok-4.7) · [docs.x.ai](https://docs.x.ai/developers/models) · [artificialanalysis.ai](https://artificialanalysis.ai/models/comparisons/grok-4-7-vs-grok-4-6)
