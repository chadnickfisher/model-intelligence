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

### Vision.question_answering (low confidence)

Answered the tested simple synthetic image questions accurately; natural-image and high-resolution transfer remain unestablished.

Scope: direct / conditional. Bounded direct task evidence in the specified workflow; no transfer to untested tasks or configurations.

Direct task IDs: vision.question_answering

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-2733964500e64515

Conditions: 17 generated images, two trials each; chart, OCR, counting and diagram tasks; Codex subscription default effort.

Failure modes / limitations: Not established in this pass

Supporting sources: [GPT-6.1 Sol vision and Korean instruction tests](https://github.com/joonlab/gpt-6.1-sol-benchmark/blob/main/data/vision_ko/README.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: 34/34 trials passed all expected fields; small clean synthetic images omit natural-image clutter and distribution shift.; No matched independent replication established; confidence concerns this narrow conclusion, not the numerical score.

### Language.instruction_following (low confidence)

Followed the tested Korean output-format constraints; this supports constrained formatting rather than broad language fluency.

Scope: direct / conditional. Bounded direct task evidence in the specified workflow; no transfer to untested tasks or configurations.

Direct task IDs: language.instruction_following

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-289b144d4efd3f48

Conditions: 16 Korean instruction cases repeated twice, 48 constraints, Codex subscription default effort.

Failure modes / limitations: Not established in this pass

Supporting sources: [GPT-6.1 Sol vision and Korean instruction tests](https://github.com/joonlab/gpt-6.1-sol-benchmark/blob/main/data/vision_ko/README.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: 32/32 cases passed the author's deterministic constraint checks; naturalness and conversational coherence were not graded.; No matched independent replication established; confidence concerns this narrow conclusion, not the numerical score.

### Agent.tool_use (low confidence)

Useful evidence for choosing and chaining a small set of deterministic mock tools; validate arguments and results in real workflows.

Scope: direct / conditional. Bounded direct task evidence in the specified workflow; no transfer to untested tasks or configurations.

Direct task IDs: agent.tool_use

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-2cec8c99696f4a0c

Conditions: Codex subscription, September 30; effort left at environment default.; Five mock tools; 60 strict selection/argument cases and 16 agent cases with three to five calls, maximum 12 turns.

Failure modes / limitations: Not established in this pass

Supporting sources: [GPT-6.1 Sol tool-use and schema tests](https://github.com/joonlab/gpt-6.1-sol-benchmark/blob/main/data/tools/README.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: 60/60 strict tool cases and 16/16 agent cases passed. Synthetic ceiling tests do not establish recovery from real service failures.; No matched independent replication established; confidence concerns this narrow conclusion, not the numerical score.

### Language.writing (low confidence)

Useful candidate for drafting scripts against a supplied voice guide and research packet; human editorial review remains necessary.

Scope: direct / conditional. Bounded direct task evidence in the specified workflow; no transfer to untested tasks or configurations.

Direct task IDs: language.writing

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-3d20bc120f7b5508

Conditions: High effort, Codex subscription, default sampling; ten YouTube-script briefs with five runs each.; About 13K prompt tokens of guide, brief and research packet; no external tools.

Failure modes / limitations: Not established in this pass

Supporting sources: [ToneBench GPT-6.1 Sol high](https://benchmark.towardsai.com/models/gpt-6-1-sol-high.html)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: October 11 run: WritingScore 81.1/100; three LLM judges plus the typed Jev 1.13 classifier. Same-family GPT-6.1 Sol medium creates judge dependence. Narrow single-creator voice, private rubric and references.; No matched independent replication established; confidence concerns this narrow conclusion, not the numerical score.

### Coding.refactoring (low confidence)

Can preserve measured legacy binary behavior during constrained rewrites at high, xhigh and max effort; retain the executable acceptance suite.

Scope: direct / conditional. Bounded direct task evidence in the specified workflow; no transfer to untested tasks or configurations.

Direct task IDs: coding.refactoring

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-60dbd819022599bd

Conditions: Codex CLI 0.159.0 Pro; September 29–30; 23 tasks per effort, one run per task.; Frozen v3.18 benchmark grades 231 hidden behavior checks; preserve actual binary behavior, including departures from specification.

Failure modes / limitations: Low and medium efforts missed some hidden behavior targets.

Supporting sources: [GPT-6.1 Sol legacy binary rewrite study v3.18](https://vulcanbench.com/benchmarks/swe-v4-gpt61-sol-v318.html)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: High/xhigh/max each passed 23/23 tasks; medium 22/23 and low 20/23. Code-style LLM scores are not the correctness result.; No matched independent replication established; confidence concerns this narrow conclusion, not the numerical score.

### Context.retrieval (low confidence)

Synthetic needle retrieval remained accurate across the tested long contexts; production document retrieval still needs task-specific evaluation.

Scope: direct / conditional. Bounded direct task evidence in the specified workflow; no transfer to untested tasks or configurations.

Direct task IDs: context.retrieval

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-9d24ce6aabf3f9dd

Conditions: Codex Pro, low effort, September 30; 16K to about 914K input tokens at five insertion depths.; Repeated filler contexts; largest cells sometimes have one run; source reports 98/98 successful needle cases.

Failure modes / limitations: Not established in this pass

Supporting sources: [GPT-6.1 Sol long-context tests](https://github.com/joonlab/gpt-6.1-sol-benchmark/blob/main/data/longctx/README.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: This is retrieval of inserted strings, not distractor-rich evidence synthesis; no immutable server checkpoint reported.; No matched independent replication established; confidence concerns this narrow conclusion, not the numerical score.

### Knowledge.retrieval (low confidence)

A plausible low-effort reranker for short multilingual candidate excerpts; check recall and language performance on the actual corpus.

Scope: direct / conditional. Bounded direct task evidence in the specified workflow; no transfer to untested tasks or configurations.

Direct task IDs: knowledge.retrieval

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-fa71065d8579ec80

Conditions: 240 MIRACL queries, 40 each in six languages; 24 fixed candidates per query; candidate excerpts truncated to 1200 characters.; GPT-6.1 Sol low; 8192 maximum output tokens; the exact result row identifies Bedrock us-west-2. Specific Bedrock endpoint/API, inference profile and immutable serving revision are not established.

Failure modes / limitations: Approximately 23% of evaluated first choices were not the target passage.

Supporting sources: [Reranking with a classifier](https://stuga.dev/blog/reranking-with-a-classifier)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Published Hit@1 is 77%, bootstrap interval 72–82%; this does not measure generated-answer groundedness.; No matched independent replication established; confidence concerns this narrow conclusion, not the numerical score.

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
