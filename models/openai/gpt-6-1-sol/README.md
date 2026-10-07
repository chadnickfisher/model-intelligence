# GPT-6.1 Sol

**Creator:** OpenAI · **Family:** GPT-6 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-29

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Coding and document reasoning at constrained spend (medium confidence)

Useful first comparison against Astra for routine complex work.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.repository_work; context.reasoning

Judgment ID: judgment-7d037d39575a5ff8

Conditions: Same named max effort; harness and token usage differ across models.

Failure modes / limitations: Lower SciCode and AA-LCR results than GPT-6 Sol in the cited max-effort comparison.

Supporting sources: [GPT-6.1 Sol versus GPT-6 Sol, max effort](https://artificialanalysis.ai/models/comparisons/gpt-6-1-sol-vs-gpt-6-sol)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: AA max: Terminal-Bench4.0 rises44% to56% versus GPT-6 Sol; GDP.pdf25% to31%.; contradictory evidence: SciCode declines58% to54%; AA-LCR84% to83%. Newer is not better on every task.; Observation obs-e5d2a15ea501: Useful first comparison against Astra for routine complex work.; Potential risk (not a measured failure): Long-context misses and task-specific coding regressions.

### Factual answers and tool backed research (low confidence)

Improved but requires checking sources and tool failures.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): research.fact_check; research.synthesis

Judgment ID: judgment-6485858c395995b9

Conditions: Use current retrieval for changing facts.

Failure modes / limitations: Vendor selected error-inducing prompts still produce factual errors; this is not typical-use prevalence.

Supporting sources: [Introducing GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: OpenAI difficult-prompt factual error rate:7.7% versus11.4% for GPT-6 Sol at low effort.; contradictory evidence: This is a selected error-inducing set, not ordinary-use prevalence.; Observation obs-c5c416a3125b: Improved but requires checking sources and tool failures.; Potential risk (not a measured failure): Undisclosed search failure remains possible; fabricated certainty.; Confidence limited by vendor-heavy task evidence and missing exact-task independent replication; documented interface support alone is not task quality.

### Coding.scoped_edit (low confidence)

Useful evidence for exact, fully specified file changes in the measured tooling; semantic edits remain unestablished.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.scoped_edit

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-98fd19b09613391e

Conditions: Provider route: openai-codex; 3 contributing harness families; detailed effort mix not extracted.; API/checkpoint identity follows source's exact named model; underlying quantization not supplied.; 226 tasks; shell/native editing tools allowed.; Score combines 75% initial exactness and 25% final exactness after permitted recovery.; Record describes a model route with mixed harnesses; do not interpret as pass@1 or a causal model ranking.

Failure modes / limitations: Not established in this pass

Supporting sources: [Explicit Edit Benchmark public data](https://huggingface.co/datasets/alexshpunt/explicit-edit-benchmark) · [Explicit Edit methodology](https://github.com/alexshpunt/explicit-edit-benchmark/blob/main/docs/methodology.md) · [Explicit Edit task definitions](https://github.com/alexshpunt/explicit-edit-benchmark/blob/main/docs/tasks.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: No matched independent contradictory evaluation located. This source establishes a narrow measured route, not a general ability ranking.; Potential transfer risk, not measured semantic failure: test-free byte matching does not establish a correct code change.; Confidence concerns this bounded claim, not a capability score.

### Coding.debugging (medium confidence)

Can repair a subset of hidden repository defects; use as an assisted audit, not a completeness guarantee.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-c6d6c0d605aaa494

Conditions: Codex0.159.0; max is not the account's highest setting (ultra also existed).; Harness: Codex CLI; effort: max; effort evidence: first_party.; 105 planted defects across TypeScript VS Code extension (~28K lines) and React/Supabase LMS (~60K lines).; One agentic round per repository; native CLI/tools; same task prompt but nonidentical harnesses, contexts and budgets.; Blind diff-based answer-key grading; extra unplanted fixes excluded; private corpus/judgments prevent full external reproduction.

Failure modes / limitations: Many planted defects remained unresolved in the measured runs.; Run variance and harness differences prevent fine-grained cross-model ranking.

Supporting sources: [Bug Hunt Bench frozen measurements](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/data/benchmark.json) · [Bug Hunt Bench receipts and boundaries](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/README.md) · [Bug Hunt Bench individual configuration caveats](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/run-notes.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Result measures finding AND implementing fixes; do not relabel it as code-review recall or test-generation quality.; No matched independent contradiction located; partial successes and misses coexist.; Confidence concerns this bounded claim, not a capability score.

### Coding.debugging (low confidence)

Promising for small Python repairs when concrete failing examples are available.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-a5e619c615a3a665

Conditions: Codex subscription environment, medium effort; seven failed samples from other models, twice each.; One repair round; at most six failed tests/errors disclosed; Python3.12 standard library.

Failure modes / limitations: No failures observed in14attempts; this is too small and feedback-rich to establish general reliability.

Supporting sources: [Python coding and repair track](https://github.com/joonlab/gpt-6.1-sol-benchmark/blob/main/data/coding/README.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Different code scale from Bug Hunt Bench; both findings should coexist.; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-8573c4b7da9f04dd

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

### Coding.tests (low confidence)

Higher-effort builds showed meaningful test design, but author-reported pass claims remain unverified.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.tests

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-445903182a61db95

Conditions: CodexCLI 0.159.0; two frontend builds, one run/effort.; Named release matches; preserve source-specific provider, snapshot and precision limitations.

Failure modes / limitations: No full independent execution audit; low effort may omit real tests.

Supporting sources: [GPT-6.1 Sol reasoning effort test on two builds](https://spectrumailab.com/blog/gpt-6-1-sol-reasoning-effort-test-2026)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Frontend output can look convincing before maintainability and validation are satisfactory.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-2fb42e70216e4400

Conditions: Effort-sensitive Codex harness; inspect artifacts and actually run acceptance checks.; Named release matches; preserve source-specific provider, snapshot and precision limitations.

Failure modes / limitations: Dense low-effort source; false localhost-running summaries.

Supporting sources: [GPT-6.1 Sol reasoning effort test on two builds](https://spectrumailab.com/blog/gpt-6-1-sol-reasoning-effort-test-2026) · [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

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

11 recorded access route(s); 5 model-specific price record(s).

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
| openai | Flex / current | input: 1.0 USD / per 1 million tokens; cached_input: 0.05 USD / per 1 million tokens; cache_write: 1.25 USD / per 1 million tokens; output: 5.0 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Batch / current | input: 1.0 USD / per 1 million tokens; cached_input: 0.05 USD / per 1 million tokens; cache_write: 1.25 USD / per 1 million tokens; output: 5.0 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Standard / current | input: 4 USD / per 1 million tokens; cached_input: 0.2 USD / per 1 million tokens; cache_write: 5.0 USD / per 1 million tokens; output: 15.0 USD / per 1 million tokens | input >272000 tokens; full request uses long-context rates; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Fast / current | input: 4 USD / per 1 million tokens; cached_input: 0.2 USD / per 1 million tokens; cache_write: 5.0 USD / per 1 million tokens; output: 20 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Standard / current | input: 2 USD / per 1 million tokens; cached_input: 0.1 USD / per 1 million tokens; cache_write: 2.5 USD / per 1 million tokens; output: 10 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |

## Recorded access routes

- openai / ChatGPT Enterprise USD Work/Codex: Conditional consumer/client product; exact account entitlement unverified. Enterprise USD agreement only; standard token rates separately published.
- openai / Responses / Chat Completions: officially_documented_not_execution_tested. Not established in this pass
- openai / ChatGPT Work and Codex (desktop / CLI / IDE / supported cloud surfaces): Conditional consumer/client product; exact account entitlement unverified. Eligible paid plans and workspace model permissions; ChatGPT authentication uses shared plan usage. API-key authentication is separately metered.
- openai / Regular Chat: Conditional consumer/client product; exact account entitlement unverified. Explicitly not yet available in regular Chat.
- aws-bedrock / Bedrock Runtime / Mantle: official_route_with_conflicting_global_availability_evidence. Not established in this pass
- azure-foundry / Azure OpenAI: officially_documented_not_execution_tested. Not established in this pass
- openai / Responses / Chat Completions: Available; endpoint feature differences apply. quota: Tier/account dependent; actual remaining quota unknown; subscription_includes_api: false
- openai / ChatGPT Work: Paid-plan access; Luna also documented for Free/Go desktop. quota: Shared plan usage; actual allowance/reset account-specific
- openai / Codex CLI: Codex product access; paid plan or separately billed API authentication depends on setup. quota: Plan allowances are not model/API token limits
- openai / Codex IDE extension: Codex IDE product documented; model access still depends on account and workspace settings. quota: Plan allowances are not model/API token limits
- openai / ChatGPT Chat: Not yet available in Chat according to current launch/help documentation. Not established in this pass

## Sources

[gpt-6.1-sol model specifications](https://developers.openai.com/api/docs/models/gpt-6.1-sol) · [OpenAI current model catalog](https://developers.openai.com/api/docs/models) · [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) · [GPT-6.1 Sol versus GPT-6 Sol, max effort](https://artificialanalysis.ai/models/comparisons/gpt-6-1-sol-vs-gpt-6-sol) · [Introducing GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol/)
