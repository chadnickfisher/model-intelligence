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

Repaired 43 of 105 hidden defects in one Claude Code/max run; use for assisted diagnosis and repair with material verification.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-f023edc397fdd671

Conditions: One round per repository on 2026-09-01; one configuration run, not repeated trials.; Approximately 28K-line TypeScript extension and 60K-line React/TypeScript Supabase LMS; 76 reverted real fixes plus 29 authored defects.; Native Claude Code; max is a documented first-party tier requested explicitly, not separately probed as binding.; No network or git history; preserve passing checks; diagnose symptoms and root causes and edit source in place.; Blind non-sibling judge compares diffs with withheld answer key; partials, claimed-only and extras do not increase strict score.; Metrics identify model=claude-fable-5-1 and a [1m] window request; precise CLI version and exact provider endpoint are not established in these inspected max-row receipts.

Failure modes / limitations: 62 seeded defects were not fully repaired in the inspected run; two fixes were partial and four were claimed without implementation.

Supporting sources: [Bug Hunt Bench frozen measurements](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/data/benchmark.json) · [Bug Hunt Bench receipts and boundaries](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/README.md) · [Bug Hunt Bench individual configuration caveats](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/run-notes.md) · [Bug Hunt Bench methodology](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/README.md) · [Bug Hunt Bench repository 1 metrics](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/repo1-metrics.csv) · [Bug Hunt Bench repository 2 metrics](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/repo2-metrics.csv)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: One run across two repositories; partial fixes and eleven unscored genuine extras do not increase the strict score.; Low confidence reflects withheld artifacts, no exact-configuration replication and unknown run variance.; Zero recorded false-positive fixes does not establish absence of regressions; this is repair evidence, not code-review recall.

### Coding.refactoring (medium confidence)

Completed a useful subset of behavior-preserving refactors under tests and structural checks; substantial independent verification remains necessary.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.refactoring

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-a0a1fd6ff5e17879

Conditions: Published dataset: 70 tasks from 10 production repositories in six languages.; Task resolution requires unchanged test files, no relevant baseline-test regressions or failing added interface tests, and all mandatory rubric criteria.; Rubric judge is Claude Opus 4.5, not the evaluated model; documentation criteria are optional.; Study uses Harbor with Modal sandboxing and repository shell/build/test access.

Failure modes / limitations: Pooled benchmark analysis reports incomplete extraction, unwired call sites and stale artifacts; these are not Fable-specific frequencies.; Anthropic documents whole-file rewrites for small edits, usually preserving the result but increasing output and time.

Supporting sources: [SWE Atlas - Refactoring](https://labs.scale.com/leaderboard/sweatlas-refactoring) · [What's new in Claude Fable 5.1 - Claude Platform Docs](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Scale reports 56.67 percent with displayed uncertainty 6.52 for Claude Code/xHigh; actual Fable trial count and interval semantics remain unconfirmed.; Medium finding confidence concerns the bounded independent task evaluation; it does not establish equivalent performance on other routes or efforts.; Official edit guidance supplements the evaluation; it is not an independent correctness measurement or measured recovery.

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

### Coding.debugging (low confidence)

Snorkel reports 87% on four debugging tasks with executable feedback; this is bounded independent corroboration.

Scope: direct / conditional. Exact task evidence under its reported setup; no transfer to adjacent tasks or model/provider configurations.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-6c7a3c099d3c4be7

Conditions: Only the source-described task and setup are assessed; unspecified settings remain unknown.

Failure modes / limitations: Not a controlled comparison with Bug Hunt.

Supporting sources: [Fable 5.1 on Frontier Coding Tasks: Efficient Successes, Distinct Failure Modes](https://snorkel.ai/blog/fable-5-1-vs-opus-5-coding-benchmark/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Proprietary four-task subset; attempt denominator, aggregation and served configuration undisclosed.

### Coding.debugging (low confidence)

owen800q reports that Fable 5.1, while implementing Jira bug fixes, added unsolicited helper functions, unrelated refactors, and architectural changes. This is a reported scope-control failure during repair; comments propose mitigations without verifying recovery.

Scope: direct / warning. Exact task evidence under its reported setup; no transfer to adjacent tasks or model/provider configurations.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-ad43fedfa9593401

Conditions: First-person Jira bug-repair workflow; exact provider, snapshot, client version, effort and patches undisclosed.

Failure modes / limitations: Single unverified account, with no executable reproduction, rate, or pinned client/provider/effort.; Does not test success at a requested behavior-preserving refactor; do not generalize to all setups.

Supporting sources: [How do you stop Fable 5.1 from scope creeping and refactoring code outside the Jira ticket?](https://www.reddit.com/r/ClaudeCode/comments/1whj547/how_do_you_stop_fable_51_from_scope_creeping_and/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Original first-person report explicitly names Fable 5.1 but supplies no code, diff, trace, exact model snapshot, client version, effort, or provider route.; Unrequested refactoring during bug repair is a debugging scope-control concern, not a tested failure at a requested behavior-preserving refactor.; Suggested prompts, restricted edits, and diff checks in comments lack controlled before/after validation. Stable publication date not established.; Unrequested refactoring is related context, not evidence of failure at a requested behavior-preserving refactor.; Prompting advice in comments does not establish controlled recovery.

### Coding.debugging (low confidence)

returnity reports that Fable 5.1 at xhigh did not resolve a gensim 4.4 compiled-kernel problem, instead suppressing its stderr notices while disclosing that choice, and missed a separate sentence-final token-loss bug. The same workflow report praises its UTF-8 handling and readable code.

Scope: direct / warning. Exact task evidence under its reported setup; no transfer to adjacent tasks or model/provider configurations.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-7bb7ec6d2a29dc85

Conditions: Author reports Fable 5.1/xhigh during one ML workflow; provider, client version, snapshot and run date undisclosed.

Failure modes / limitations: No independently reproduced trace or pinned client/provider/model snapshot; claimed error cause is author-attributed.; Cross-posts are one experiment. A failure in this case does not establish a general regression or comparative ranking.; No verified later recovery by Fable 5.1 is reported for these defects.

Supporting sources: [Astra vs. Fable 5.1 on real ML tasks: tradeoffs, strengths, shortcomings](https://www.reddit.com/r/MachineLearning/comments/1w8g1gk/astra_vs_fable_51_on_real_ml_tasks_tradeoffs/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Original body inspected. User names Fable 5.1 and xhigh; underlying provider route, client version, immutable model snapshot, exact run date, and raw reproduction artifacts are not established.; One reported ML workflow with human feedback, not a repeated controlled debugging benchmark. The claimed gensim cause is the author’s account, not independently validated here.; Same-author cross-posts and search hits in r/OpenAI/r/ArtificialInteligence are the same experiment, not replications. Model-training F1/accuracy is not a debugging success score.; Original body contains relative age only; published_at remains null.

### Coding.debugging (low confidence)

Gradle reports claude-fable-5-1 diagnosed and repaired issue #34751, reproduced the Dokka link-target error, and passed a new regression test plus an existing test. The author preferred its patch, while explicitly limiting the comparison to one run on one bug.

Scope: direct / conditional. Exact task evidence under its reported setup; no transfer to adjacent tasks or model/provider configurations.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-bdd86c4657d2dabd

Conditions: Reported run on 2026-09-07; claude-fable-5-1 through Claude Code 2.1.263 and gradle-eval/Inspect AI.; Gradle commit 8606a2c1, JDK 21 container, network available; limits: 50 turns, 5 million tokens and 45 minutes.; Dokka 2.2.0 reproduction, new Spock/TestKit regression check and existing GradleReleaseNotesPluginTest; effort/provider endpoint undisclosed.

Failure modes / limitations: Effort, provider, immutable snapshot and judge unknown; no general ranking or independent rerun.

Supporting sources: [Testing Astra 6 v Fable 5.1 on a Gradle docs bug](https://blog.gradle.org/two-agents-one-gradle-bug)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: One reported bug/run; tools differ between comparison models. Not independently reproduced; proposed PR not verified merged.

### Coding.refactoring (low confidence)

Wmedia includes extracting shared validation from three controllers, checked for centralization and passing controller tests. All mixed-task runs passed; no separate refactoring score is tabulated.

Scope: direct / conditional. Exact task evidence under its reported setup; no transfer to adjacent tasks or model/provider configurations.

Direct task IDs: coding.refactoring

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-0d56d17e388e4a0a

Conditions: Claude Code 2.1.280 at high effort; clean 11-file PHP repository, no user settings or MCP servers.; Shared validation extracted from three controllers; centralization and controller tests checked; three repetitions per task.; The published 12/12 total covers four mixed tasks; no separate refactoring-only score is tabulated.

Failure modes / limitations: Small simple task with prewritten checks; results do not establish multi-repository refactoring reliability.; The unrelated bug-task test remained failing and was excluded from refactor scoring; raw results ZIP not inspected.

Supporting sources: [Opus 5.5 vs Fable 5.1 vs Opus 5: the same tasks at a third of the cost](https://wmedia.es/en/tips/claude-code-opus-5-5-vs-fable-5-1-vs-opus-5-benchmark)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: One small mixed-task study; linked raw ZIP was not inspected.

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
