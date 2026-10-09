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

### Agent.long_horizon (medium confidence)

Sustains useful iterative engineering work under a long-running scaffold, while final acceptance still needs checking.

Scope: direct / conditional. Original exact-model source inspected against this task rubric; no transfer to neighboring tasks.

Direct task IDs: agent.long_horizon

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-01c94f547da25077

Conditions: Proximus, max effort, 20 hours per task, 34 tasks, mean of 5 trials; Fable 5.1 with Opus 5 fallback scores 56.29% normalized reward.; Scaffold supplies compaction, progress files, self-check feedback and checkpointed submissions.

Failure modes / limitations: Partial solutions remain; normalized reward does not mean a complete outcome.

Supporting sources: [FrontierSWE v2](https://www.frontierswe.com/blog/v2)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Original trajectory examples show feedback-driven revisions, including reverting a compiler optimization and generating new astrometry test inputs.; Fallback and evaluation-aware prompting limit attribution to a standalone Fable checkpoint.

### Language.summarization (low confidence)

Check source attribution in document summaries; Anthropic reports unmarked reuse of source wording.

Scope: direct / warning. Exact assigned rubric task; conclusion applies only to the documented evaluation or reported behavior.

Direct task IDs: language.summarization

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-028a36af1a3ac2ad

Conditions: Vendor prompting guidance for Fable 5.1; no disclosed sample size, effort or measured recovery.

Failure modes / limitations: Source passages may be reproduced without quotation marking.

Supporting sources: [Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: A prompting remedy is not a fidelity or completeness benchmark. Aggregate suitability remains unknown.

### Knowledge.retrieval (medium confidence)

Can shortlist research literature, but incomplete recall requires additional search and expert screening.

Scope: direct / conditional. Exact assigned rubric task; conclusion applies only to the documented evaluation or reported behavior.

Direct task IDs: knowledge.retrieval

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-03386ed90ef9abfd

Conditions: ScholarCatalyst tool-calling agent; 207 CoreQ and687 SubQ; default thinking, Gemini Embedding 2, five search rounds and 60-paper pool.; Titles/abstracts in temporally filtered local corpus; no web; unknown API checkpoint, run date and precision.

Failure modes / limitations: R@20 misses roughly half the labeled inspirations; declines and ranking backfill affect results.

Supporting sources: [ScholarCatalyst: A Benchmark for Retrieving Papers That Inspire New Research](https://arxiv.org/html/2610.02202v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Post-cutoff comparison only; does not establish RAG answer grounding or research synthesis.

### Coding.repository_work (low confidence)

The reported Snake conversion integrates an engine, browser interface, CLI simulator and tests, supporting assisted repository changes with material review.

Scope: direct / conditional. Original exact-model source inspected against this task rubric; no transfer to neighboring tasks.

Direct task IDs: coding.repository_work

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-0632bedb804079d6

Conditions: One existing-app transformation with shared deterministic outcomes required across browser and CLI.

Failure modes / limitations: No published patch or hidden acceptance results establish full cross-file consistency or repeatability.

Supporting sources: [Fable 5.1 review: Coding tests and code review results](https://www.coderabbit.ai/blog/fable-5-1-model-review)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: This case is distinct from review metrics and is not a repository-wide completion rate.

### Vision.question_answering (medium confidence)

Useful for checked image-grounded answers; material answer and output-format errors remain.

Scope: direct / conditional. Exact task in one evaluator workflow.

Direct task IDs: vision.question_answering

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-066745f9ef77af12

Conditions: Roboflow low/high benchmark tiers, three repeated runs per tier; exact native effort mapping unspecified.; Provider endpoint, snapshot, precision, context length, sample denominator and measurement dates undisclosed.

Failure modes / limitations: Judge-accepted correctness substantially exceeds exact-match compliance.

Supporting sources: [Visual Reasoning Benchmark](https://playground.roboflow.com/evals/visual-reasoning) · [Vision Evals methodology](https://playground.roboflow.com/evals) · [Claude Fable 5.1 Vision Evals](https://playground.roboflow.com/models/anthropic/claude-fable-5-1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Judge accuracy low72.0/high73.1; strict accuracy low18.3/high36.2. Gemini3.5 Flash temperature0 judge.; Displayed ± is half-range, not confidence interval. Independent evaluator but one study; no external replication found.

### Coding.frontend (low confidence)

Produces useful initial interfaces, with interaction, responsiveness and product-logic corrections still needed.

Scope: direct / conditional. Original exact-model source inspected against this task rubric; no transfer to neighboring tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-21c1f66c73e4b3b1

Conditions: Three briefs: finance dashboard, reference-guided portfolio and video-editor prototype; one focused feedback round.; Author reports functioning dashboard tooltips; website task used Mobbin and 21st.dev MCP references.

Failure modes / limitations: Responsive and interaction decisions needed correction; the editor was a shell rather than a verified full editing product.

Supporting sources: [I Tested Claude Fable 5.1 as a UI Designer](https://griffinwooldridge.com/blog/claude-fable-5-1-ui-design-test)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Named practitioner, small subjective sample and affiliate disclosure. Exact serving configuration and systematic acceptance tests are absent.

### Context.reasoning (medium confidence)

Useful cross-document reasoning at tested lengths, with explicit checking of derived conclusions.

Scope: direct / conditional. Exact assigned rubric task; conclusion applies only to the documented evaluation or reported behavior.

Direct task IDs: context.reasoning

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-226284e4e8c7d97e

Conditions: AA-LCR v1.1:~10K–100K supplied text, 100 questions × 3, no tools, GPT-5.6 Luna (medium) equality checker.; Fable 5.1 max/default-fallback service; task-specific fallback share and measurement date unknown.

Failure modes / limitations: Some questions fail; separate professional-document all-pass performance is substantially lower.

Supporting sources: [Fable5.1 versus Fable5 benchmark comparison](https://artificialanalysis.ai/models/comparisons/claude-fable-5-1-vs-claude-fable-5) · [Artificial Analysis Intelligence Benchmarking Methodology](https://artificialanalysis.ai/methodology/intelligence-benchmarking) · [Artificial Analysis Long Context Reasoning Benchmark](https://artificialanalysis.ai/evaluations/artificial-analysis-long-context-reasoning)

Contradictory or limiting sources: [Fable5.1 versus Fable5 benchmark comparison](https://artificialanalysis.ai/models/comparisons/claude-fable-5-1-vs-claude-fable-5) · [GDP.pdf Benchmark](https://artificialanalysis.ai/evaluations/gdp-pdf)

Evidence notes: AA-LCR 85% cannot be extrapolated to 1M context. GDP.pdf 26% all-pass has different criteria and document input.

### Context.reasoning (medium confidence)

Can aggregate facts across supplied enterprise documents in the tested 128K setup; verify important conclusions.

Scope: direct / conditional. Exact assigned rubric task; conclusion applies only to the documented evaluation or reported behavior.

Direct task IDs: context.reasoning

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-2baa77d0e49174ac

Conditions: Anthropic API thinking mode, measured2026-09-02; RIKER 128K, no retrieval tools, generated-ground-truth grading.; Exact effort, per-component task denominator, repetitions, provider checkpoint and precision undisclosed.

Failure modes / limitations: Aggregation not perfect; generated corpora limit real-document generalization.

Supporting sources: [Claude Fable 5.1 on Signal65 PINNACLE](https://pinnacle.signal65.com/articles/claude-fable-5-1-on-signal65-pinnacle/) · [Signal65 PINNACLE: Measuring Correct Work](https://pinnacle.signal65.com/wp-content/uploads/2026/08/Signal65-Pinnacle_Measuring-Correct-Work.pdf)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Aggregation 95.3 is distinct from RIKER retrieval 97.3 and the agentic workflow total.

### Language.writing (medium confidence)

Useful English creative-writing drafts; edit for audience, readability and preferred style.

Scope: direct / conditional. Exact assigned rubric task; conclusion applies only to the documented evaluation or reported behavior.

Direct task IDs: language.writing

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-386854e040d319d5

Conditions: Exact claude-fable-5-1 rows in evaluator site data; effort, underlying provider and measurement date undisclosed.; Creative Writing v3:32 prompts × 3; longform:eight chapters; LLM judgments, not human acceptance.

Failure modes / limitations: Judge style preferences may differ from readers; vendor reports dense prose.

Supporting sources: [EQ-Bench longform leaderboard data](https://raw.githubusercontent.com/EQ-bench/EQ-bench-site/refs/heads/main/creative_writing_longform.js) · [EQ-Bench Longform Creative Writing](https://eqbench.com/creative_writing_longform.html) · [EQ-Bench Creative Writing v3 leaderboard data](https://raw.githubusercontent.com/EQ-bench/EQ-bench-site/refs/heads/main/creative_writing.js) · [EQ-Bench methodology](https://eqbench.com/about.html)

Contradictory or limiting sources: [Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)

Evidence notes: Longform 85.3/100 and v3 Elo 2152.7/rubric 16.95 are separate, subjective metrics from one evaluator group.

### Reasoning.math (medium confidence)

Strong mathematical answer-solving candidate; check derivations and final answers before relying on them.

Scope: direct / conditional. Exact assigned rubric task; conclusion applies only to the documented evaluation or reported behavior.

Direct task IDs: reasoning.math

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-5716da0bdaa18296

Conditions: Epoch mathematical evaluations; FrontierMath permits Python and1M combined-token budget; OTIS scores integer answers.; Rendered model rows do not disclose Fable effort, provider, checkpoint, repeat counts, actual denominator or measurement date.

Failure modes / limitations: Advanced problems still receive incorrect answers; proof validity is not separately evaluated.

Supporting sources: [Claude Fable 5.1](https://epoch.ai/models/claude-fable-5-1) · [FrontierMath Tiers 1-3 (v2)](https://epoch.ai/benchmarks/frontiermath-tiers-1-3-v2) · [OTIS Mock AIME 2024-2025](https://epoch.ai/benchmarks/otis-mock-aime-2024-2025)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Rounded original scorecard:90% FrontierMath1–3, 88% Tier 4, 100% OTIS. Final-answer scores do not certify proofs.

### Coding.scoped_edit (low confidence)

Constrain the edit boundary: the vendor reports unrequested additions and larger edits than necessary.

Scope: direct / warning. Original exact-model source inspected against this task rubric; no transfer to neighboring tasks.

Direct task IDs: coding.scoped_edit

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-689bb2ecd898d750

Conditions: Open-ended feature requests; official guidance says nearby fixes or extra tests may be added.; Whole-file rewriting can increase output tokens and time even when the resulting file is equivalent.

Failure modes / limitations: Scope expansion and edit overhead require review; overhead alone is not correctness failure.

Supporting sources: [Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Prompting advice does not establish measured recovery or a bounded edit success rate.

### Agent.long_horizon (medium confidence)

Completes a useful subset of dependent terminal workflows with a minimal agent loop, with many tasks still requiring intervention.

Scope: direct / conditional. Original exact-model source inspected against this task rubric; no transfer to neighboring tasks.

Direct task IDs: agent.long_horizon

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-7072f78efd6409e3

Conditions: Fable 5.1 Max, Default Fallback: 52% Terminal-Bench 4.0 pass@1 averaged across three repeats of 66 tasks.; mini-swe-agent; bash; 500 steps; no compaction; task success requires all verifier tests.

Failure modes / limitations: Nearly half of the rounded aggregate does not pass all task tests; a mixed terminal total does not isolate a coding skill.

Supporting sources: [Fable5.1 versus Fable5 benchmark comparison](https://artificialanalysis.ai/models/comparisons/claude-fable-5-1-vs-claude-fable-5) · [Artificial Analysis Intelligence Benchmarking Methodology](https://artificialanalysis.ai/methodology/intelligence-benchmarking)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Independent evaluation configuration differs from the vendor launch harness. Fallback, missing checkpoint and run dates constrain transfer.

### Agent.computer_use (low confidence)

Vendor evidence supports assisted desktop workflows, with checkpoints and human recovery required for incomplete tasks.

Scope: direct / conditional. Original exact-model source inspected against this task rubric; no transfer to neighboring tasks.

Direct task IDs: agent.computer_use

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-792deb882f31613b

Conditions: OSWorld 2.0 August 2026 task release: 77.9% partial credit and 41.7% strict completion; production safeguards enabled and refused tasks scored zero.

Failure modes / limitations: Most tasks did not reach strict completion; partial progress must not be presented as a saved or completed outcome.

Supporting sources: [Introducing Claude Fable 5.1 and Mythos 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Vendor-only task evidence. Original system card body could not be fetched; effort, client, step limit, trials and task denominator remain unverified.; No independent exact-model OSWorld reproduction located in the allotted searches.

### Knowledge.extraction (medium confidence)

Useful for specified fields in images, with value verification and output-format checks.

Scope: direct / conditional. Exact assigned rubric task; conclusion applies only to the documented evaluation or reported behavior.

Direct task IDs: knowledge.extraction

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-86bb987e0b07f068

Conditions: Roboflow low/high benchmark tiers; three runs each; native API effort mapping, sample denominator and run dates unknown.; Gemini 3.5 Flash temperature0 judge plus normalized exact-match companion.

Failure modes / limitations: Incorrect values remain; strict output matching trails semantic correctness.

Supporting sources: [Data Extraction Benchmark: Vision Evals](https://playground.roboflow.com/evals/data-extraction) · [Claude Fable 5.1 Vision Evals](https://playground.roboflow.com/models/anthropic/claude-fable-5-1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low 93.1% judged/89.7% strict; high 93.5%/92.1%. Reported±values are half-ranges, not confidence intervals.

### Language.translation (low confidence)

Useful ancient-text translation drafts; require scholarly fidelity review and English style revision.

Scope: direct / conditional. Exact assigned rubric task; conclusion applies only to the documented evaluation or reported behavior.

Direct task IDs: language.translation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-aa593e899e272552

Conditions: Ancient Greek/Classical Chinese into English; ten passages, one cold draft per passage; Opus 5 blind/adversarial judging.; Provider, API effort, immutable snapshot, token budget and precision were not disclosed.

Failure modes / limitations: Minor translation errors and excessively literal English persisted.

Supporting sources: [Does the new director translate better?](https://openscriptorium.com/session-logs/001-fable-5-1-vs-fable-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: 24/30 preferences are judge votes, not30 independent translations. Historical controls and prompts were unmatched.

### Vision.grounding (medium confidence)

Useful for reviewed zero-shot bounding boxes; localization errors require material correction.

Scope: direct / conditional. Exact task in one evaluator workflow.

Direct task IDs: vision.grounding

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-aabef5a9b68bec41

Conditions: Roboflow low/high benchmark tiers, three repeated runs per tier; exact native effort mapping unspecified.; Provider endpoint, snapshot, precision, context length, sample denominator and measurement dates undisclosed.

Failure modes / limitations: Stricter box-overlap scores are substantially lower; do not treat mAP as complete-task success.

Supporting sources: [Object Detection Benchmark](https://playground.roboflow.com/evals/object-detection) · [Vision Evals methodology](https://playground.roboflow.com/evals) · [Claude Fable 5.1 Vision Evals](https://playground.roboflow.com/models/anthropic/claude-fable-5-1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: mAP@50 low61.4/high65.0; mAP@75 low40.2/high40.4; mAP@50:95 low38.0/high39.6.; Displayed ± is half-range, not confidence interval. Independent evaluator but one study; no external replication found.

### Agent.tool_use (medium confidence)

Can complete many multi-tool workflows in MCP Atlas, but validate final claims and consequential tool effects.

Scope: direct / conditional. Original exact-model source inspected against this task rubric; no transfer to neighboring tasks.

Direct task IDs: agent.tool_use

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-aae2313e7b9446b7

Conditions: Fable 5.1 default configuration; 87.20% pass rate, displayed ±2.05; public 500-task subset; 100 tool-call cap.; A pass requires at least 75% claim coverage, not every objective.

Failure modes / limitations: Failures remain, and a passing task may still omit part of its answer.

Supporting sources: [MCP Atlas](https://labs.scale.com/leaderboard/mcp_atlas) · [MCP Atlas evaluation repository](https://github.com/scaleapi/mcp-atlas/tree/main)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Exact effort, trial count, serving checkpoint and run date undisclosed.; Judge identity unresolved: leaderboard says Gemini 2.5 Pro, linked current code says Gemini 3.1 Pro Preview. These are one study, not corroborating streams.

### Coding.frontend (low confidence)

A reported Battlesnake prototype demonstrates useful working interface generation, but does not establish production acceptance.

Scope: direct / conditional. Original exact-model source inspected against this task rubric; no transfer to neighboring tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-b9dc2f9ad518ea55

Conditions: CodeRabbit changed an existing Snake app into a five-agent spectator arena with a shared browser/CLI engine; its recorded match reached turn 793.

Failure modes / limitations: One showcased coding case is not a measured general frontend success rate.

Supporting sources: [Fable 5.1 review: Coding tests and code review results](https://www.coderabbit.ai/blog/fable-5-1-model-review)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Separate from the 45-task code-review study. Effort, endpoint, attempts, executable artifact and accessibility checks were not disclosed.

### Coding.debugging, coding.scoped_edit (low confidence)

A small saturated pilot corroborates basic repair execution, without isolating diagnosis from implementing a supplied correction.

Scope: unresolved / conditional. Repair-only pilot does not disclose whether diagnosis or implementing a supplied correction is the measured work.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.debugging; coding.scoped_edit

Judgment ID: judgment-c62c550542276e11

Conditions: September 1 pilot: Fable 5.1 low, Vercel AI Gateway pinned to Anthropic; all six JavaScript repair cases passed hidden tests.

Failure modes / limitations: Six small tasks cannot establish broad repository or debugging reliability.

Supporting sources: [Claude Fable 5.1: Benchmarks, Price & Verdict](https://kingy.ai/blog/claude-fable-5-1-benchmarks-price-mythos-access/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: The overall 30/30 includes 20 streaming checks and four research cases; it is never used as a coding success denominator.

### Coding.tests (medium confidence)

Useful for drafting behavior-focused repository tests, with material correction and mutation checking still required.

Scope: direct / conditional. Original exact-model source inspected against this task rubric; no transfer to neighboring tasks.

Direct task IDs: coding.tests

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-e3faa2efb33104c6

Conditions: Fable-5.1 (Claude Code) xHigh*: 67.04% mean resolve rate, displayed ±5.33; 90 tasks and 3 trials.; Tests must pass before mutation, fail after the relevant code mutation, and meet mandatory coverage rubrics.

Failure modes / limitations: A substantial fraction of tasks still failed the combined acceptance checks; pooled error taxonomy is not a Fable-specific rate.

Supporting sources: [SWE Atlas - Test Writing](https://labs.scale.com/leaderboard/sweatlas-tw)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Independent task-specific evaluation; exact checkpoint, client build and measurement dates remain unknown.; Star footnote explicitly names Fable 5; no Fable 5.1-specific refusal frequency is inferred.

### Agent.tool_use (medium confidence)

Useful partial SaaS workflow execution under structured API tools; do not treat partial objectives as complete business workflows.

Scope: direct / conditional. Original exact-model source inspected against this task rubric; no transfer to neighboring tasks.

Direct task IDs: agent.tool_use

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-ee5501be80efeccf

Conditions: Fable 5.1 Max, Default Fallback: 59% AutomationBench-AA headline score.; 657 tasks, dataset 1.0.6, one run per task, 50-turn cap; final-state assertions; any guardrail violation zeros the task.

Failure modes / limitations: Unmet objectives and policy failures can remain; headline is average objective share rather than full completion.

Supporting sources: [Fable5.1 versus Fable5 benchmark comparison](https://artificialanalysis.ai/models/comparisons/claude-fable-5-1-vs-claude-fable-5) · [Artificial Analysis Intelligence Benchmarking Methodology](https://artificialanalysis.ai/methodology/intelligence-benchmarking)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Fallback affects provenance; exact model-only result and run dates unavailable.; Separate API workflow evidence supports tool use, not graphical computer use.

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

License: Anthropic Commercial Terms of Service (Claude API route)

Restrictions: Usage, Supported Regions and Service Specific Terms apply to commercial API use.; Competing-service development, competing-model training, duplication/reverse engineering, and unapproved resale are restricted by the Commercial Terms.

Commercial use: Commercial API use may power customer-facing products, subject to the Commercial Terms and incorporated policies.

Redistribution: Unknown / not established

Hosted service: Claude API access is governed by Anthropic Commercial Terms; consumer plans and partner offerings have separate applicable terms.

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
