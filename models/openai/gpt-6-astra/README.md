# GPT-6 Astra

**Creator:** OpenAI · **Family:** GPT-6 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-03

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Complex coding and computer workflows (medium confidence)

Strong candidate when difficult end-to-end work justifies latency and token cost.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.repository_work; agent.computer_use

Judgment ID: judgment-fbf53a2171375503

Conditions: AA harness/version and reasoning effort are material; these are not success probabilities for an arbitrary user task.

Failure modes / limitations: AA terminal tasks still fail at high and max effort; OpenAI documents legitimate work being interrupted by safety monitoring.

Supporting sources: [Astra high versus max benchmark comparison](https://artificialanalysis.ai/models/comparisons/gpt-6-astra-high-vs-gpt-6-astra) · [GPT-6 Astra: A new generation of intelligence](https://openai.com/index/gpt-6-astra/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: AA Terminal-Bench4.0: high54%, max59%; AutomationBench-AA high67%, max68%.; contradictory evidence: Higher effort is not uniformly better: AA-Omniscience high44 versus max43; GDP.pdf31% for both.; Observation obs-a91fd388dc88: Strong candidate when difficult end-to-end work justifies latency and token cost.; Potential risk (not a measured failure): Incorrect or out-of-scope actions remain possible; production safety monitors can stop legitimate work.

### Scientific research (medium confidence)

A strong escalation model for hard scientific workflows.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: reasoning.scientific

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-4e7af644a89ef0a9

Conditions: Maximum effort; tool-enabled scientific terminal workflow.

Failure modes / limitations: Not established in this pass

Supporting sources: [Introducing GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: OpenAI reports68.1% on Terminal-Bench Science0.1 in the Sol comparison.; contradictory evidence: Substantial residual failures; vendor-run setting and benchmark version affect results.; Observation obs-8eab532ce0f9: A strong escalation model for hard scientific workflows.; Potential risk (not a measured failure): Confident wrong derivations or incomplete experiments require independent verification.

### Coding.debugging (medium confidence)

Can repair a subset of hidden repository defects; use as an assisted audit, not a completeness guarantee.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-50e193772d714514

Conditions: Codex ChatGPT route; documented effort, not a separately measured effort magnitude.; Harness: Codex CLI; effort: max; effort evidence: first_party.; 105 planted defects across TypeScript VS Code extension (~28K lines) and React/Supabase LMS (~60K lines).; One agentic round per repository; native CLI/tools; same task prompt but nonidentical harnesses, contexts and budgets.; Blind diff-based answer-key grading; extra unplanted fixes excluded; private corpus/judgments prevent full external reproduction.

Failure modes / limitations: Many planted defects remained unresolved in the measured runs.; Run variance and harness differences prevent fine-grained cross-model ranking.

Supporting sources: [Bug Hunt Bench frozen measurements](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/data/benchmark.json) · [Bug Hunt Bench receipts and boundaries](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/README.md) · [Bug Hunt Bench individual configuration caveats](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/run-notes.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Result measures finding AND implementing fixes; do not relabel it as code-review recall or test-generation quality.; No matched independent contradiction located; partial successes and misses coexist.; Research provenance: history/research/2026-10-07/coding-input.json :: scoped_debugging:gpt-6-astra-debug-bughunt; Confidence concerns this bounded claim, not a capability score.

### Coding.debugging (low confidence)

Promising for small Python repairs when concrete failing examples are available.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-3ee716fcfdb2364d

Conditions: Codex subscription environment, medium effort; seven failed samples from other models, twice each.; One repair round; at most six failed tests/errors disclosed; Python3.12 standard library.

Failure modes / limitations: No failures observed in14attempts; this is too small and feedback-rich to establish general reliability.

Supporting sources: [Python coding and repair track](https://github.com/joonlab/gpt-6.1-sol-benchmark/blob/main/data/coding/README.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Different code scale from Bug Hunt Bench; both findings should coexist.; Research provenance: history/research/2026-10-07/coding-input.json :: scoped_debugging:gpt-6-astra-debug-small-python; Confidence concerns this bounded claim, not a capability score.

### Coding.architecture (low confidence)

One unfamiliar-system report cautions that strong local edits can still conflict with the broader architecture.

Scope: direct / warning. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.architecture

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-92341ccdd95f6b40

Conditions: Complex unfamiliar mod/reverse-engineering work; human testing loop.

Failure modes / limitations: Patching before adequately reconstructing state/callback interactions.

Supporting sources: [GPT-6 Astra is good, but still far from what I would call AGI](https://community.openai.com/t/gpt-6-astra-is-good-but-still-far-from-what-i-would-call-agi/1395147)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Single anecdote, no code or controlled runs. Warning about this workload only; cannot establish a general failure rate or override refactoring benchmark E07.; Research provenance: history/research/2026-10-07/coding-input.json :: architecture_refactoring:A05; Confidence concerns this bounded claim, not a capability score.

### Coding.refactoring (medium confidence)

Strong relative result on difficult refactoring, with substantial unresolved tasks.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.refactoring

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-5e13f6bbea5e1900

Conditions: 70 tasks, 10 production repositories, 6 languages; Harbor/Modal sandboxes. Resolve requires unchanged tests, zero regressions, and every mandatory Opus 4.5-judged rubric.

Failure modes / limitations: Incomplete extraction, unwired callers, stale implementations/artifacts; failure taxonomy is pooled, not per-model.

Supporting sources: [SWE Atlas - Refactoring](https://labs.scale.com/leaderboard/sweatlas-refactoring)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Harnesses differ; uncertainty overlaps, so no significant ordering claimed. Preserve xHigh as board label. Intro's below 50% statement is stale. Gemini 3.1 Pro 33.81±6.64 is withheld pending preview-ID mapping.; Research provenance: history/research/2026-10-07/coding-input.json :: architecture_refactoring:R01; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-6d1cd0c0da04925a

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Research provenance: history/research/2026-10-07/coding-input.json :: review_tests_frontend:frontend-arena-gpt-6-astra; Confidence concerns this bounded claim, not a capability score.

### Coding.review (medium confidence)

Review strength depends on context and reporting threshold; no uniform bug-discovery advantage established.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.review

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-b2cbbb99f4f4d7db

Conditions: Keep repository-aware and diff-only evaluations separate.; Named release matches; preserve source-specific provider, snapshot and precision limitations.

Failure modes / limitations: Diff-only study missed security issues despite high finding precision.

Supporting sources: [GPT-6 Astra review: Code review results, privacy, and cost](https://www.coderabbit.ai/blog/gpt-6-astra-code-review-evaluation) · [GPT-6 Astra Cost 1.6x More Per Verified Bug Than GPT-5.6 Sol](https://entelligence.ai/blogs/gpt-6-astra-cost-1.6x-more-per-verified-bug-than-gpt-5.6-sol)

Contradictory or limiting sources: [GPT-6 Astra Cost 1.6x More Per Verified Bug Than GPT-5.6 Sol](https://entelligence.ai/blogs/gpt-6-astra-cost-1.6x-more-per-verified-bug-than-gpt-5.6-sol)

Evidence notes: Research provenance: history/research/2026-10-07/coding-input.json :: review_tests_frontend:review-astra; Confidence concerns this bounded claim, not a capability score.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 1050000 |
| maximum output | 128000 |
| modalities | input: text; image; output: text |
| language support | Multilingual; exact inventory not specified |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

13 recorded access route(s); 6 model-specific price record(s).

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

- Undisclosed architecture and parameter count
- Exact supported-language inventory and per-language quality not verified

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| openai | Flex / current | input: 5.0 USD / per 1 million tokens; cached_input: 0.5 USD / per 1 million tokens; cache_write: 6.25 USD / per 1 million tokens; output: 25.0 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Standard / current | input: 10 USD / per 1 million tokens; cached_input: 1 USD / per 1 million tokens; cache_write: 12.5 USD / per 1 million tokens; output: 50 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Standard / current | input: 20 USD / per 1 million tokens; cached_input: 2 USD / per 1 million tokens; cache_write: 25.0 USD / per 1 million tokens; output: 75.0 USD / per 1 million tokens | input >272000 tokens; full request uses long-context rates; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Ultrafast / current | input: 60 USD / per 1 million tokens; cached_input: 6 USD / per 1 million tokens; cache_write: 75 USD / per 1 million tokens; output: 300 USD / per 1 million tokens | short context; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Batch / current | input: 5.0 USD / per 1 million tokens; cached_input: 0.5 USD / per 1 million tokens; cache_write: 6.25 USD / per 1 million tokens; output: 25.0 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Fast / current | input: 20 USD / per 1 million tokens; cached_input: 2 USD / per 1 million tokens; cache_write: 25.0 USD / per 1 million tokens; output: 100 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |

## Recorded access routes

- openai / Responses / Chat Completions: officially_documented_not_execution_tested. Not established in this pass
- aws-bedrock / Bedrock Runtime / Mantle: officially_documented_not_execution_tested. Not established in this pass
- openai / ChatGPT Enterprise USD Work/Codex: Conditional consumer/client product; exact account entitlement unverified. Enterprise USD agreement only; standard token rates separately published.
- openai / ChatGPT Work and Codex (desktop / CLI / IDE / supported cloud surfaces): Conditional consumer/client product; exact account entitlement unverified. Eligible paid plans and workspace model permissions; ChatGPT authentication uses shared plan usage. API-key authentication is separately metered.
- azure-foundry / Azure OpenAI: officially_documented_not_execution_tested. Not established in this pass
- openai / ChatGPT Chat: GPT-6 Pro: Conditional consumer/client product; exact account entitlement unverified. Pro $100, Pro $200, Business and Enterprise; workspace permissions apply. Plus Astra access is Work/Codex, not established Chat access.
- openai / Responses / Chat Completions: Available; endpoint feature differences apply. quota: Tier/account dependent; actual remaining quota unknown; subscription_includes_api: false
- openai / ChatGPT: Eligible Plus/Pro/Business/Enterprise access; workspace permissions and current picker govern. quota: Included allowance and model-specific availability vary; not an unlimited API entitlement; Current Astra-powered Chat access is Pro $100/$200, Business and Enterprise; Plus belongs to Work/Codex.
- openai / ChatGPT Work: Paid-plan access; Luna also documented for Free/Go desktop. quota: Shared plan usage; actual allowance/reset account-specific
- openai / Codex CLI: Codex product access; paid plan or separately billed API authentication depends on setup. quota: Plan allowances are not model/API token limits
- openai / Codex IDE extension: Codex IDE product documented; model access still depends on account and workspace settings. quota: Plan allowances are not model/API token limits
- aws-bedrock / Amazon Bedrock: Official launch names these providers; region, contract and prices not independently verified. Not established in this pass
- azure-foundry / Microsoft Foundry / Azure: Official launch names these providers; region, contract and prices not independently verified. Not established in this pass

## Sources

[gpt-6-astra model specifications](https://developers.openai.com/api/docs/models/gpt-6-astra) · [OpenAI current model catalog](https://developers.openai.com/api/docs/models) · [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) · [Astra high versus max benchmark comparison](https://artificialanalysis.ai/models/comparisons/gpt-6-astra-high-vs-gpt-6-astra) · [GPT-6 Astra: A new generation of intelligence](https://openai.com/index/gpt-6-astra/) · [Introducing GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol/)
