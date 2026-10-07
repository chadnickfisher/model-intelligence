# Claude Fable 5.1

**Creator:** Anthropic · **Family:** Claude 5 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-01

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Long horizon reasoning and coding (medium confidence)

Escalation candidate with strong evidence but expensive effort-sensitive operation.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): agent.long_horizon; reasoning.general; coding.repository_work

Judgment ID: judgment-7416a8c0468f622a

Conditions: Evaluated service includes safety fallback to other Claude models.

Failure modes / limitations: Cited GDP.pdf all-pass result is26%; failed cases are not categorized in the retrieved comparison.

Supporting sources: [Fable5.1 versus Fable5 benchmark comparison](https://artificialanalysis.ai/models/comparisons/claude-fable-5-1-vs-claude-fable-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: AA max/default fallback: Terminal-Bench4.0 52%, HLE59%, AA-LCR85%; all improve over Fable5 except some nearly flat tasks.; contradictory evidence: GDP.pdf only26%; these results do not make Fable universally preferable to newer Opus/Sonnet.; Observation obs-8614ee721f1d: Escalation candidate with strong evidence but expensive effort-sensitive operation.; Potential risk (not a measured failure): Fallback changes model provenance; errors persist on document reasoning.

### Coding.debugging (low confidence)

Can repair a subset of hidden repository defects; use as an assisted audit, not a completeness guarantee.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-f023edc397fdd671

Conditions: Single configuration run; no robust ranking implied.; Harness: Claude Code; effort: max; effort evidence: first_party.; 105 planted defects across TypeScript VS Code extension (~28K lines) and React/Supabase LMS (~60K lines).; One agentic round per repository; native CLI/tools; same task prompt but nonidentical harnesses, contexts and budgets.; Blind diff-based answer-key grading; extra unplanted fixes excluded; private corpus/judgments prevent full external reproduction.

Failure modes / limitations: Many planted defects remained unresolved in the measured runs.; Run variance and harness differences prevent fine-grained cross-model ranking.

Supporting sources: [Bug Hunt Bench frozen measurements](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/data/benchmark.json) · [Bug Hunt Bench receipts and boundaries](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/README.md) · [Bug Hunt Bench individual configuration caveats](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/run-notes.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Result measures finding AND implementing fixes; do not relabel it as code-review recall or test-generation quality.; No matched independent contradiction located; partial successes and misses coexist.; Confidence concerns this bounded claim, not a capability score.

### Coding.refactoring (medium confidence)

Strong benchmark candidate; bound edit scope and retain regression checks.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.refactoring

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-a0a1fd6ff5e17879

Conditions: 70 tasks, 10 production repositories, 6 languages; Harbor/Modal sandboxes. Resolve requires unchanged tests, zero regressions, and every mandatory Opus 4.5-judged rubric.; Always-on adaptive thinking; effort-controlled operation.

Failure modes / limitations: Incomplete extraction, unwired callers, stale implementations/artifacts; failure taxonomy is pooled, not per-model.; Official documentation warns it favors whole-file rewrites for small changes, increasing output/time; targeted-edit prompting recommended.

Supporting sources: [SWE Atlas - Refactoring](https://labs.scale.com/leaderboard/sweatlas-refactoring) · [What's new in Claude Fable 5.1](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Harnesses differ; uncertainty overlaps, so no significant ordering claimed. Preserve xHigh as board label. Intro's below 50% statement is stale. Gemini 3.1 Pro 33.81±6.64 is withheld pending preview-ID mapping.; Vendor behavior description supplements E07; it is not an independent refactor success measurement.; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-2b7a37781171e7e2

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

### Coding.review (low confidence)

Can surface known issues but needs validation; lower tested effort was preferable in this pipeline.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.review

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-cf376fda86010ad5

Conditions: Separate tiny rule checking from open-ended review.; Named release matches; preserve source-specific provider, snapshot and precision limitations.; Low/High are evaluator pipeline configurations, not established single API effort values.; The evaluation corpus and scoring pipeline limit external reproducibility.

Failure modes / limitations: Substantial judge-rejected commentary and misses; higher reasoning did not improve aggregate results.

Supporting sources: [Fable 5.1 review: Coding tests and code review results](https://www.coderabbit.ai/blog/fable-5-1-model-review) · [Can Jev make a code review agent cheaper and faster?](https://github.com/gemanor/jev-code-review-benchmark/blob/95932b43f227dc759a7147d4e2d371388a148eb8/README.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.; CodeRabbit evaluated 45 review tasks with 105 known issues; lower and higher configurations traded recall, precision and comment load.; Low confidence reflects the inspected evaluator, corpus/pipeline dependence and unpublished replication inputs; it is not a low ability rating.

### Cache heavy agents (medium confidence)

Cache price cut can help context-heavy workflows, but task cost is workload-dependent.

Scope: performance / conditional. Cost, deployment or throughput observation; not a task capability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-b82fd561ee151f9f

Conditions: Vendor default-effort August traffic and AA max benchmark are different workloads, not directly contradictory arithmetic.

Failure modes / limitations: AA reports higher benchmark task cost despite lower cached-token rates.

Supporting sources: [Introducing Claude Fable 5.1 and Mythos 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1) · [Fable 5.1 launch measurement](https://artificialanalysis.ai/zh/articles/claude-fable-5-1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Conservative baseline confidence: broader convergence has not been independently audited.; supporting evidence: Vendor reports25% typical and up to45% highly agentic savings versus Fable5.; contradictory evidence: AA launch measurement reports20% higher cost/task despite cheaper cache reads.; Observation obs-c5fa019c8d8a: Cache price cut can help context-heavy workflows, but task cost is workload-dependent.; Potential risk (not a measured failure): Longer reasoning can erase cache savings.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 1000000 |
| maximum output | 128000 |
| modalities | input: text; image; output: text |
| language support | Multilingual; exact inventory not specified |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

15 recorded access route(s); 2 model-specific price record(s).

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
| anthropic | Standard / current | input: 10 USD / per 1 million tokens; output: 50 USD / per 1 million tokens; cached_input: 0.25 USD / per 1 million tokens; cache_write_5m: 12.5 USD / per 1 million tokens; cache_write_1h: 20 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |
| anthropic | Batch / current | input: 5.0 USD / per 1 million tokens; output: 25.0 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |

## Recorded access routes

- aws-bedrock / Amazon Bedrock: officially_documented_not_execution_tested. Not established in this pass
- anthropic / Usage-based Claude Enterprise: Conditional consumer/client product; exact account entitlement unverified. Seat fee plus usage at API rates; this is a separately evidenced metered client route.
- google-cloud / Gemini Enterprise Agent Platform (formerly Vertex AI): officially_documented_not_execution_tested. Not established in this pass
- azure-foundry / Claude in Microsoft Foundry / Hosted on Anthropic: officially_documented_not_execution_tested. Message Batches, Models API and server-side fallback are unsupported on Foundry.; New computer/browser toolsets are unsupported; older beta computer tools are separate.
- anthropic / Claude apps / Cowork / Claude Code: Conditional consumer/client product; exact account entitlement unverified. All paid plans can access, with materially different inclusion: Max and premium Team/legacy Enterprise seats include up to 50% of shared weekly usage; Pro and standard Team/legacy Enterprise seats use usage credits from first request.
- claude-platform-on-aws / Claude Platform on AWS: officially_documented_not_execution_tested. Not established in this pass
- anthropic / Claude Code terminal and IDE: Conditional consumer/client product; exact account entitlement unverified. Full model IDs can be selected subject to plan and organization permissions. Separate subscription sign-in from API-key/partner billing.
- anthropic / Claude API: officially_documented_not_execution_tested. Not established in this pass
- anthropic / Claude API: Active. quota: Tier/account-specific; exact numeric public tier table not captured
- aws-bedrock / Amazon Bedrock: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- azure-foundry / Microsoft Foundry / Azure: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- google-cloud / Google Cloud: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- anthropic / Claude Code terminal: All paid Claude plans include Code; API-credit billing is a separate option. quota: Shared with web/desktop/mobile plan pool; IDE entitlement details not separately verified
- anthropic / Claude Code IDE integrations: documented route; account eligibility unverified. Not established in this pass
- anthropic / Claude apps: Pro uses usage credits; Max has Fable access within50% of weekly limits. quota: Not equivalent to unlimited subscription access

## Sources

[Claude fable-5-1 specifications](https://platform.claude.com/docs/en/models/fable-5-1/overview) · [Claude current model overview](https://platform.claude.com/docs/en/models/overview) · [Fable5.1 versus Fable5 benchmark comparison](https://artificialanalysis.ai/models/comparisons/claude-fable-5-1-vs-claude-fable-5) · [Introducing Claude Fable 5.1 and Mythos 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1) · [Fable 5.1 launch measurement](https://artificialanalysis.ai/zh/articles/claude-fable-5-1)
