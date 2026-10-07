# GPT-6 Luna

**Creator:** OpenAI · **Family:** GPT-6 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-22

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Focused high volume tasks (medium confidence)

Good low-token-price option for bounded, validated subtasks.

Scope: unresolved / conditional. Scope needs review; the original claim does not establish a specific task ability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.scoped_edit; language.instruction_following

Judgment ID: judgment-0c281701a4185869

Conditions: Reasoning settings and harness matter; DeepSWE and Terminal-Bench are different tests.

Failure modes / limitations: Only13% all-tests-pass on cited AA Terminal-Bench4.0 at max effort.

Supporting sources: [GPT-6 Luna max benchmark comparison](https://artificialanalysis.ai/models/comparisons/gpt-6-luna-vs-gpt-5-3-codex) · [Introducing GPT-6 Sol and Luna](https://openai.com/index/introducing-gpt-6-sol-and-luna/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: AA max AA-LCR83%; vendor DeepSWE66.6% in its own setup.; contradictory evidence: AA max Terminal-Bench4.0 only13%, GDP.pdf23%; narrower competence than price marketing suggests.; Observation obs-18449a135e8c: Good low-token-price option for bounded, validated subtasks.; Potential risk (not a measured failure): Brittle long-horizon work; weak factual calibration; use deterministic checks.

### Coding.scoped_edit (low confidence)

Useful evidence for exact, fully specified file changes in the measured tooling; semantic edits remain unestablished.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.scoped_edit

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-4793164eb12deab7

Conditions: Provider route: opencode-go; 1 contributing harness families; detailed effort mix not extracted.; API/checkpoint identity follows source's exact named model; underlying quantization not supplied.; 226 tasks; shell/native editing tools allowed.; Score combines 75% initial exactness and 25% final exactness after permitted recovery.; Record describes a model route with mixed harnesses; do not interpret as pass@1 or a causal model ranking.

Failure modes / limitations: Some initial or final file trees failed exact comparison; this aggregate does not isolate the failure mechanism.

Supporting sources: [Explicit Edit Benchmark public data](https://huggingface.co/datasets/alexshpunt/explicit-edit-benchmark) · [Explicit Edit methodology](https://github.com/alexshpunt/explicit-edit-benchmark/blob/main/docs/methodology.md) · [Explicit Edit task definitions](https://github.com/alexshpunt/explicit-edit-benchmark/blob/main/docs/tasks.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: No matched independent contradictory evaluation located. This source establishes a narrow measured route, not a general ability ranking.; Potential transfer risk, not measured semantic failure: test-free byte matching does not establish a correct code change.; Confidence concerns this bounded claim, not a capability score.

### Coding.debugging (medium confidence)

Can repair a subset of hidden repository defects; use as an assisted audit, not a completeness guarantee.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-639aaaec04d00c96

Conditions: gpt-6-luna; Codex0.155.1 on ChatGPT account.; Harness: Codex CLI; effort: max; effort evidence: first_party.; 105 planted defects across TypeScript VS Code extension (~28K lines) and React/Supabase LMS (~60K lines).; One agentic round per repository; native CLI/tools; same task prompt but nonidentical harnesses, contexts and budgets.; Blind diff-based answer-key grading; extra unplanted fixes excluded; private corpus/judgments prevent full external reproduction.

Failure modes / limitations: Many planted defects remained unresolved in the measured runs.; Run variance and harness differences prevent fine-grained cross-model ranking.

Supporting sources: [Bug Hunt Bench frozen measurements](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/data/benchmark.json) · [Bug Hunt Bench receipts and boundaries](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/README.md) · [Bug Hunt Bench individual configuration caveats](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/run-notes.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Result measures finding AND implementing fixes; do not relabel it as code-review recall or test-generation quality.; No matched independent contradiction located; partial successes and misses coexist.; Confidence concerns this bounded claim, not a capability score.

### Coding.debugging (low confidence)

Feedback can repair simple code, but a second attempt can also worsen correctness.

Scope: direct / warning. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-ff68302009316769

Conditions: Medium effort, same Python repair protocol as Park's coding track.

Failure modes / limitations: 10/12 self-repairs passed; two regex repairs reduced passing-test counts.

Supporting sources: [Python coding and repair track](https://github.com/joonlab/gpt-6.1-sol-benchmark/blob/main/data/coding/README.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Tiny sample; not evidence that high effort universally hurts.; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-db92b976581cf0cf

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

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
| openai | Flex / current | input: 0.05 USD / per 1 million tokens; cached_input: 0.005 USD / per 1 million tokens; cache_write: 0.0625 USD / per 1 million tokens; output: 0.25 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Standard / current | input: 0.2 USD / per 1 million tokens; cached_input: 0.02 USD / per 1 million tokens; cache_write: 0.25 USD / per 1 million tokens; output: 0.75 USD / per 1 million tokens | input >272000 tokens; full request uses long-context rates; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Batch / current | input: 0.05 USD / per 1 million tokens; cached_input: 0.005 USD / per 1 million tokens; cache_write: 0.0625 USD / per 1 million tokens; output: 0.25 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Fast / current | input: 0.2 USD / per 1 million tokens; cached_input: 0.02 USD / per 1 million tokens; cache_write: 0.25 USD / per 1 million tokens; output: 1.0 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Standard / current | input: 0.1 USD / per 1 million tokens; cached_input: 0.01 USD / per 1 million tokens; cache_write: 0.125 USD / per 1 million tokens; output: 0.5 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |

## Recorded access routes

- openai / ChatGPT Work and Codex (desktop / CLI / IDE / supported cloud surfaces): Conditional consumer/client product; exact account entitlement unverified. Eligible paid plans and workspace model permissions; ChatGPT authentication uses shared plan usage. API-key authentication is separately metered.
- aws-bedrock / Bedrock Runtime / Mantle: officially_documented_not_execution_tested. Not established in this pass
- azure-foundry / Azure OpenAI: officially_documented_not_execution_tested. Not established in this pass
- openai / Responses / Chat Completions: officially_documented_not_execution_tested. Not established in this pass
- openai / ChatGPT Enterprise USD Work/Codex: Conditional consumer/client product; exact account entitlement unverified. Enterprise USD agreement only; standard token rates separately published.
- openai / Regular Chat / Free and Go desktop: Conditional consumer/client product; exact account entitlement unverified. Regular Chat explicitly unavailable. Launch documents Luna access for Free and Go on desktop; no free API entitlement follows.
- openai / Responses / Chat Completions: Available; endpoint feature differences apply. quota: Tier/account dependent; actual remaining quota unknown; subscription_includes_api: false
- openai / ChatGPT Work: Paid-plan access; Luna also documented for Free/Go desktop. quota: Shared plan usage; actual allowance/reset account-specific
- openai / Codex CLI: Codex product access; paid plan or separately billed API authentication depends on setup. quota: Plan allowances are not model/API token limits
- openai / Codex IDE extension: Codex IDE product documented; model access still depends on account and workspace settings. quota: Plan allowances are not model/API token limits
- openai / ChatGPT Chat: Not yet available in Chat according to current launch/help documentation. Not established in this pass

## Sources

[gpt-6-luna model specifications](https://developers.openai.com/api/docs/models/gpt-6-luna) · [OpenAI current model catalog](https://developers.openai.com/api/docs/models) · [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) · [GPT-6 Luna max benchmark comparison](https://artificialanalysis.ai/models/comparisons/gpt-6-luna-vs-gpt-5-3-codex) · [Introducing GPT-6 Sol and Luna](https://openai.com/index/introducing-gpt-6-sol-and-luna/)
