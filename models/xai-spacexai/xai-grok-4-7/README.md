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

Evidence notes: Result measures finding AND implementing fixes; do not relabel it as code-review recall or test-generation quality.; No matched independent contradiction located; partial successes and misses coexist.; Research provenance: history/research/2026-10-07/coding-input.json :: scoped_debugging:xai-grok-4-7-debug-bughunt; Confidence concerns this bounded claim, not a capability score.

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

Evidence notes: Research provenance: history/research/2026-10-07/coding-input.json :: review_tests_frontend:frontend-arena-xai-grok-4-7; Confidence concerns this bounded claim, not a capability score.

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
