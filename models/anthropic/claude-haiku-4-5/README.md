# Claude Haiku 4.5

**Creator:** Anthropic · **Family:** Claude 4.5 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2025-10-15

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Fast bounded coding and assistant subtasks (medium confidence)

Useful responsive model when limited task scope and validation matter.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.scoped_edit; language.instruction_following

Judgment ID: judgment-86b4ad915dcef6a0

Conditions: Vendor partner testimonials are selected marketing evidence, not independent controlled replications.

Failure modes / limitations: Low cited non-reasoning HLE and AA-LCR performance; specific errors not categorized in retrieved page.

Supporting sources: [Introducing Claude Haiku 4.5](https://www.anthropic.com/news/claude-haiku-4-5) · [Haiku non-reasoning benchmark comparison](https://artificialanalysis.ai/models/comparisons/hy3-vs-claude-4-5-haiku)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: Vendor SWE-bench Verified73.3%,500 tasks,50 trials, custom prompt and large thinking budget; launch partners report responsive coding.; contradictory evidence: AA non-reasoning HLE4%, AA-LCR50%; older near-frontier claims must not be generalized to2026 hardest work.; Observation obs-ca2b56257797: Useful responsive model when limited task scope and validation matter.; Potential risk (not a measured failure): Hard reasoning and long-context misses; weaker date freshness.

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-db0341f19aa38f54

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

### Coding.tests (low confidence)

The source does isolate Haiku test validity under code evolution: Figure 7 reports 88.4% test passing after semantics-preserving edits and 63.6% after semantic-changing edits. Useful fault detection remains unestablished; these are freshly generated tests intended to match the new supplied code.

Scope: direct / warning. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.tests

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-19237c319f0876ad

Conditions: Two-shot API snippet workflow; fresh session per changed valid program; baseline programs selected for all-passing tests.; Figure 7 combines the documented Java/Python evolution conditions; exact serving checkpoint, effort and experiment day are unreported.

Failure modes / limitations: Generated assertions can fail the newly supplied code semantics. Coverage and test pass rate are not fault-detection success.

Supporting sources: [Evaluating LLM-Based Test Generation Under Software Evolution](https://arxiv.org/html/2603.23443v1) · [Test generation under software evolution, Figure 7](https://arxiv.org/pdf/2603.23443v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

### Coding.scoped_edit (low confidence)

One original hosted evaluation passes all nine short Python function tasks; this supports only small, self-contained implementation under that harness.

Scope: direct / conditional. The measured workload fits this task; conclusion is limited to the recorded setup.

Direct task IDs: coding.scoped_edit

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-c01714fd674be14c

Conditions: Single-turn function signature and specification; nine hidden-assertion tasks; one attempt each.

Failure modes / limitations: Small saturated suite does not establish repository, debugging, tool-use or production correctness.

Supporting sources: [DataLLM Lab Claude Haiku 4.5 short-function evaluation](https://www.datallmlab.com/blog/claude-haiku-4-5-review.html) · [DataLLM Lab benchmark methodology](https://www.datallmlab.com/blog/methodology.html)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence reflects setup breadth, identity uncertainty and source limitations, not the score. No contradictory result located in this bounded pass does not establish agreement.

### Language.instruction_following (low confidence)

Portuguese literary constraint evaluation supports a warning about exact counts and structural constraints; use explicit output checks under this setup.

Scope: direct / warning. The measured task fits this rubric boundary; no transfer to adjacent tasks.

Direct task IDs: language.instruction_following

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-7156ae35731ec615

Conditions: Temperature zero; 200 single-turn literary prompts and 100 three-turn conversations.; Original saved single-turn artifacts establish OpenRouter requested model anthropic/claude-haiku-4.5, 147/200 strict prompts and 334/405 constraints.

Failure modes / limitations: Rule-based constraint compliance does not establish factual literary correctness or all-language instruction quality.

Supporting sources: [CAPITU: Instruction-Following in Brazilian Portuguese](https://arxiv.org/html/2603.22576v1) · [CAPITU paper model run script](https://raw.githubusercontent.com/maritaca-ai/capitu/main/run_paper_models.sh) · [CAPITU Haiku single-turn metrics](https://raw.githubusercontent.com/maritaca-ai/capitu/main/runs/claude-haiku-4.5/eval/single-turn/metrics_report.json)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence reflects limited tasks, source/setup uncertainty and lack of independent replication; scores do not define confidence. Empty contradictory evidence means none was located in this bounded pass.

### Language.writing (low confidence)

Small English business-task evaluations support conditional drafting use; audience/style quality outside the five tested cases is unestablished.

Scope: direct / conditional. The measured task fits this rubric boundary; no transfer to adjacent tasks.

Direct task IDs: language.writing

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-391bee7f74fddbd3

Conditions: May 10 cohort; English single-turn text; five cases in this category, four LLM judges.

Failure modes / limitations: No public full response traces, immutable serving revision or independent replication.

Supporting sources: [Claude Haiku 4.5 May 10 benchmark](https://www.orcflo.com/orcflo-index/benchmarks/claude-haiku-4-5-2026-05-10) · [ORCFLO Index methodology](https://www.orcflo.com/orcflo-index/methodology)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence reflects limited tasks, source/setup uncertainty and lack of independent replication; scores do not define confidence. Empty contradictory evidence means none was located in this bounded pass.

### Language.summarization (low confidence)

ORCFLO recommends avoiding summary-heavy executive digests and meeting recaps, but its public five-case mean and comparative rank do not establish that core summary fidelity failures undermine usefulness. Preserve this as an attributed caution; aggregate task suitability remains unknown.

Scope: direct / warning. The measured task fits this rubric boundary; no transfer to adjacent tasks.

Direct task IDs: language.summarization

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-d14d5e6960fa913c

Conditions: May 10 cohort; English single-turn text; five cases in this category, four LLM judges.

Failure modes / limitations: No public full response traces, immutable serving revision or independent replication.

Supporting sources: [Claude Haiku 4.5 May 10 benchmark](https://www.orcflo.com/orcflo-index/benchmarks/claude-haiku-4-5-2026-05-10) · [ORCFLO Index methodology](https://www.orcflo.com/orcflo-index/methodology)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: The caution is principally comparative; neither score nor cohort rank defines a suitability threshold.; Five English single-turn cases and four LLM judges form one evaluation stream. Public summary-specific fidelity failures and correction burden are unestablished.; A relative rank and evaluator recommendation are not themselves a rubric-grounded Low suitability threshold.

### Knowledge.extraction (low confidence)

Five business extraction cases support a conditional structured-extraction conclusion; exact source types and public answer traces are incomplete.

Scope: direct / conditional. The measured task fits this rubric boundary; no transfer to adjacent tasks.

Direct task IDs: knowledge.extraction

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-623c7e8d247d4615

Conditions: May 10 cohort; English single-turn text; five cases in this category, four LLM judges.

Failure modes / limitations: No public full response traces, immutable serving revision or independent replication.

Supporting sources: [Claude Haiku 4.5 May 10 benchmark](https://www.orcflo.com/orcflo-index/benchmarks/claude-haiku-4-5-2026-05-10) · [ORCFLO Index methodology](https://www.orcflo.com/orcflo-index/methodology)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence reflects limited tasks, source/setup uncertainty and lack of independent replication; scores do not define confidence. Empty contradictory evidence means none was located in this bounded pass.

### Coding.debugging (low confidence)

CI log diagnosis depends materially on the reduction method; evidence supports a bounded diagnostic use with preserved failure signals, not an autonomous fix guarantee.

Scope: direct / conditional. The measured task fits this rubric boundary; no transfer to adjacent tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-4310e42c6be1639d

Conditions: Thirty-five public GitHub Actions failures; single-shot Haiku diagnosis JSON, deterministic diagnosis_score_v1_1.

Failure modes / limitations: Corpus-tuned threshold; AI-drafted ground truth checked by one author; no outside rescoring.

Supporting sources: [LogDx-CI: Log Reduction for Root-Cause Diagnosis](https://arxiv.org/html/2605.28876v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence reflects limited tasks, source/setup uncertainty and lack of independent replication; scores do not define confidence. Empty contradictory evidence means none was located in this bounded pass.

### Coding.review (low confidence)

Two one-shot review fixtures support a warning about missed or unsupported findings; the small directional study cannot establish general review quality.

Scope: direct / warning. The measured task fits this rubric boundary; no transfer to adjacent tasks.

Direct task IDs: coding.review

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-e35ebbffc833ea6a

Conditions: Tools disabled and one-turn assertion; one scored response per review fixture; LLM rubric and two blind judges.

Failure modes / limitations: Unpinned CLI/backend and tiny review sample; source adaptive-thinking explanation conflicts with official manual-thinking support.

Supporting sources: [LLM review benchmark](https://github.com/MarcinDudekDev/llm-review-bench)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence reflects limited tasks, source/setup uncertainty and lack of independent replication; scores do not define confidence. Empty contradictory evidence means none was located in this bounded pass.

### Knowledge.classification (low confidence)

In one 900-comment Reddit response classification study, pinned Haiku 4.5 achieved mean pooled macro-F1 0.50 with universal labels. Validate the label schema and class errors before use on similar discourse.

Scope: direct / warning. The measured task fits this rubric boundary; no transfer to adjacent tasks.

Direct task IDs: knowledge.classification

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-889de5fb1a96f5d4

Conditions: claude-haiku-4-5-20251001 via vendor CLI; empty tools; April 2–9, 2026; sampling parameters unexposed.; Three response classes; fold-composition variability, not repeat-run model uncertainty.

Failure modes / limitations: Belief-class misses; topic and label sensitivity; no surrounding thread context; corpus prefilter/annotation limits.

Supporting sources: [Long Live Fine-Tuning: Misinformation Response Classification on Reddit](https://arxiv.org/html/2606.04274v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Direct task scope follows the reported output and metric; confidence is low because this is one bounded study with the stated setup limitations.

### Reasoning.math (low confidence)

One 1000-pair GSM-Symbolic study reports 97.9% original and 96.6% modified accuracy with eight-shot chain-of-thought. This supports grade-school numerical reasoning under that prompt, with broader math ability unresolved.

Scope: direct / conditional. The measured task fits this rubric boundary; no transfer to adjacent tasks.

Direct task IDs: reasoning.math

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-2e00e2f0e910045e

Conditions: Anthropic API, temperature zero, eight-shot examples, tuned format and reasoning prefill; no code execution in CoT.; Paper-linked implementation requests claude-haiku-4-5-20251001 with max_tokens=1024; response-level serving metadata remains unverified.

Failure modes / limitations: Prompt tuning and familiar corpus; two collection runs across methods; numerical-answer matching does not evaluate proof validity; experiment day unreported.

Supporting sources: [Reasoning, Code, or Both? Variations in Math Questions](https://arxiv.org/html/2605.26414v1) · [GSM-Symbolic study Anthropic API implementation](https://raw.githubusercontent.com/masamodelkin/llm-robustness-code-execution/main/src/Claude_API.py)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Direct task scope follows the reported output and metric; confidence is low because this is one bounded study with the stated setup limitations.

### Coding.refactoring (low confidence)

The structured workflow preserves tests but completes no API-usage repairs, including two genuine cases, and no unstable-dependency repairs. These core cross-module failures undermine usefulness for that difficult refactoring scope.

Scope: direct / warning. Bounded to the explicitly evaluated task and recorded configuration.

Direct task IDs: coding.refactoring

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-0e2ad8ff50a90bd1

Conditions: 65 hard-tier scikit-learn smells: 11 genuine, 41 false positives, 13 partial. One run per configuration; no repeated trials.; 18/65 disappeared, including cascading effects;16 new smells, net +2; full test suite showed no deviations.

Failure modes / limitations: Single project/detector; task ordering and false-positive mix affect counts; this is not a genuine-bug success rate.; Exact endpoint, CLI version, decoding, context, precision and experiment date undisclosed.

Supporting sources: [SmellBench: Evaluating LLM Agents on Architectural Code Smell Repair](https://arxiv.org/html/2605.07001v2)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Architectural-smell repair is distinct from designing a new software architecture.

### Research.synthesis, research.fact_check, reasoning.scientific (low confidence)

Controlled multi-source estimate and source-choice probes show sensitivity to credible presentation despite impossible numerical claims.

Scope: compound / warning. Bounded source-specific finding; no transfer to other tasks or serving configurations.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): research.synthesis; research.fact_check; reasoning.scientific

Judgment ID: judgment-10d8ce2322d17da0

Conditions: Four-source synthetic threads across three domains; Bedrock; temperature 1, max_tokens 4000; both thinking modes.

Failure modes / limitations: Source weighting fails to discriminate valid from impossible statistics; explicit statistical detection depends on domain.

Supporting sources: [Trust, but Do Not Verify: Epistemic Blind Spots in LLM Source Evaluation](https://arxiv.org/html/2606.05403v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: These probes do not measure complete attributed research synthesis or source-based fact-checking; no direct task aggregate follows.; Mechanistic claims from Qwen/OLMo do not establish the internal cause in Haiku.

### Coding.review (low confidence)

A separate six-diff test found useful bug-specific reviews and 10 of 18 pairwise wins for Haiku. This small relative-preference result does not establish recall on larger real changes.

Scope: direct / conditional. Directly measured task subset; neighboring tasks and unmeasured operating conditions are not endorsed.

Direct task IDs: coding.review

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-1a104280be08ac23

Conditions: Six common-defect prompts, with no few-shot examples. A Sonnet 4 judge evaluated both presentation orders.

Failure modes / limitations: No absolute bug-recall or completeness metric. Checkpoint, provider route and decoding settings are unknown.

Supporting sources: [LLMTest six-diff code review evaluation](https://llmtest.io/blog/best-llm-for-code-review-2026)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Vision.question_answering (low confidence)

Quantum-plot visual descriptions are useful with checks on axes and features; scientific diagnosis is separately assessed.

Scope: direct / conditional. Bounded to the explicitly evaluated task and recorded configuration.

Direct task IDs: vision.question_answering

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-3c8d2ae9d1bfffd7

Conditions: Zero-shot without demonstrations; 243 calibration plots, each question an independent single-turn API request; temperature 0, max output 16384, default top_p; up to 3 API-failure retries.; PNG image plus family background; no shared conversation; no hidden system prompt.

Failure modes / limitations: Original repository labels the identical archived April scores as GPT-5.4-judged; paper claims a GPT-5.4/Gemini3.1Pro average. Exact scoring provenance unresolved.; Paper lists Haiku in results but omits it from the appendix exact-ID/April 6 access list; serving snapshot and run date remain unknown.; One study; reported repeated-run denominator, precision and endpoint not disclosed.

Supporting sources: [QCalEval: Benchmarking Vision-Language Models for Quantum Calibration Plot Understanding](https://arxiv.org/html/2604.25884v1) · [QCalEval original evaluation repository and archived leaderboard](https://github.com/nvidia/QCalEval)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Does not measure coordinate localization or general-image performance.

### Knowledge.classification (low confidence)

Classification quality varies materially with schema layout and instruction consistency on four argumentative-structure labels.

Scope: direct / warning. Bounded source-specific finding; no transfer to other tasks or serving configurations.

Direct task IDs: knowledge.classification

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-4d7a4a67517d2ef4

Conditions: Same 48-message taxonomy and five-repeat conditions as the schema-conflict behavior record.

Failure modes / limitations: Near-half accuracy under ordinary schema/system placement; substantial residual errors after the intermediate-field intervention.

Supporting sources: [Your Prompt Is Not the Only Prompt: How Much Do LLMs Weight Structured-Output Schema Descriptions?](https://arxiv.org/html/2608.08254v1) · [Prompt Placement Effect Evaluation](https://github.com/alina-lin-phd/prompt-placement-eval)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Single taxonomy; not an independent replication of the Reddit classification study.

### Language.translation (low confidence)

Ukrainian-English idiom translation is useful with material semantic review: scored meaning loss occurs in 23.1% of English-to-Ukrainian outputs and 12.8% in the reverse direction. Literal meaning-preserving outputs are not counted as failures.

Scope: direct / conditional. Bounded to the explicitly evaluated task and recorded configuration.

Direct task IDs: language.translation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-4fea9b29bcbbbfba

Conditions: Ukrainian↔English; source-only versus named-idiom prompts. Paper says API defaults; released code sets temperature 0.3/max_tokens 1024 and the dated request ID. Historical script-to-run equivalence unresolved.; Gemini 2.5 Flash judge: 3 idiomatic meaning preserved,2 meaning preserved without idiom, 1 meaning lost/distorted.

Failure modes / limitations: Published Haiku CSVs contain 5,724 EN→UK and 5,474 UK→EN scored outputs (11,198 total); generation-attempt denominator and repeated trials remain unknown. Missing translations and failed judge calls are omitted by the released scorer.; Single language pair; judge agrees with human sample 87% UK→EN and 78% EN→UK; no qualitative error analysis.

Supporting sources: [SimIdioms: A Corpus and Benchmark for Ukrainian Idiom Translation](https://unlp.org.ua/wp-content/uploads/2026/05/simidioms-a-corpus-and-benchmark-for-ukrainian-idiom-translation.pdf) · [SimIdioms Anthropic request settings](https://raw.githubusercontent.com/petrunivyaryna/sim-idioms/54cb5f7c51863ea76dbc63a362cbb174c804012c/translation/providers/anthropic_provider.py) · [SimIdioms translation model registry](https://raw.githubusercontent.com/petrunivyaryna/sim-idioms/54cb5f7c51863ea76dbc63a362cbb174c804012c/translation/translate_examples.py) · [SimIdioms published Haiku English-to-Ukrainian scored outputs](https://raw.githubusercontent.com/petrunivyaryna/sim-idioms/54cb5f7c51863ea76dbc63a362cbb174c804012c/evaluation/judge_scores/claude-haiku-4-5-20251001_en_to_uk.csv) · [SimIdioms published Haiku Ukrainian-to-English scored outputs](https://raw.githubusercontent.com/petrunivyaryna/sim-idioms/54cb5f7c51863ea76dbc63a362cbb174c804012c/evaluation/judge_scores/claude-haiku-4-5-20251001_uk_to_en.csv)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Literal meaning-preserving output is separated from semantic distortion; no transfer to other language pairs.

### Language.writing (medium confidence)

For scientific sentence paraphrasing and news-style rewriting, frequent certainty changes undermine the requirement to preserve the source meaning and qualifications. Ordinary stylistic review is insufficient; source-by-source certainty checking is needed.

Scope: direct / warning. Directly measured task subset; neighboring tasks and unmeasured operating conditions are not endorsed.

Direct task IDs: language.writing

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-758101839480474d

Conditions: 397 scientific sentence inputs. Haiku certainty distortion was 48.1% for paraphrase and 74.8% for news-style rewriting. Generation used temperature 1, top_p 0.9 and a 3,500-token budget.; A GPT-5.4-mini judge evaluated both presentation orders. Human validation used 240 pairs and 129 annotators; human agreement alpha was about 0.25.

Failure modes / limitations: The metric concerns subjective certainty judgments. Provider, experiment day and repeated-generation variance are unknown. No claim is made about unconstrained fiction or every kind of prose.

Supporting sources: [From May to Is: Certainty Distortion in Language Model Rewriting](https://arxiv.org/html/2606.07951v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Judge-human consensus Kendall tau-B was 0.47 (SD 0.09), compared with 0.34 (SD 0.19) for individual humans. Opposite-direction judgments across presentation orders were flagged separately; no numeric inconsistency rate was verified in this pass.

### Coding.frontend (low confidence)

Public generated-HTML examples contain automated accessibility violations. They add concrete caution to preference rankings but do not establish complete frontend interaction correctness.

Scope: direct / warning. Directly measured task subset; neighboring tasks and unmeasured operating conditions are not endorsed.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-7e7ea26a42505283

Conditions: Visible first-variation metrics showed eight axe violations on the landing page and 21 on the dashboard. Scores combine automatic audits and static structural markers.

Failure modes / limitations: Selected harness option, checkpoint, experiment date and functional acceptance tests are unknown.

Supporting sources: [UI Bench Haiku4.5 outputs](https://ui-bench.dev/model/claude-haiku-4.5) · [UI Bench scoring method](https://ui-bench.dev/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Reasoning.scientific (low confidence)

Zero-shot quantum-calibration explanations omit much of the required scientific analysis; demonstrations help but do not establish unattended reliability.

Scope: direct / warning. Bounded to the explicitly evaluated task and recorded configuration.

Direct task IDs: reasoning.scientific

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-82dd0466ce1765b0

Conditions: Zero-shot without demonstrations; 243 calibration plots, each question an independent single-turn API request; temperature 0, max output 16384, default top_p; up to 3 API-failure retries.; PNG image plus family background; no shared conversation; no hidden system prompt.

Failure modes / limitations: Original repository labels the identical archived April scores as GPT-5.4-judged; paper claims a GPT-5.4/Gemini3.1Pro average. Exact scoring provenance unresolved.; Paper lists Haiku in results but omits it from the appendix exact-ID/April 6 access list; serving snapshot and run date remain unknown.; One study; reported repeated-run denominator, precision and endpoint not disclosed.

Supporting sources: [QCalEval: Benchmarking Vision-Language Models for Quantum Calibration Plot Understanding](https://arxiv.org/html/2604.25884v1) · [QCalEval original evaluation repository and archived leaderboard](https://github.com/nvidia/QCalEval)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Judge-scored scientific key-point coverage, not a pass rate or general science score.

### Context.retrieval (low confidence)

The documented full-context setup retrieves many requested conversational facts but needs material verification for omissions and incorrect references.

Scope: direct / conditional. Bounded source-specific finding; no transfer to other tasks or serving configurations.

Direct task IDs: context.retrieval

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-8c70704b38a694d3

Conditions: LongMemEval S single-session subsets: user facts 54/70 and assistant facts 54/56; one December 12,2025 run through OpenRouter.; Whole-run mean input 116,833 tokens; max_tokens 8192; GPT-4o binary judge; immutable endpoint and sampling unpinned.

Failure modes / limitations: Inspected failures deny available commute/internet facts or select the wrong numbered-list entry.; Binary target-answer grading can miss unsupported extra elaboration in otherwise passing outputs.

Supporting sources: [Honcho benchmark raw results](https://github.com/plastic-labs/honcho-benchmarks)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Recommended bounded Medium suitability, Low evidence confidence; not a full-context or all-memory endorsement.

### Knowledge.extraction (medium confidence)

Structured extraction from scholarly PDFs is useful with material human verification. Haiku returned 90.6% fully correct values across 770 graded cells; 8.7% were incorrect and 0.6% required checking.

Scope: direct / conditional. Directly measured task subset; neighboring tasks and unmeasured operating conditions are not endorsed.

Direct task IDs: knowledge.extraction

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-8e60e5da087e6417

Conditions: claude-haiku-4-5-20251001 at temperature 0; 43 PDF articles, one API call per article; tuned JSON prompt requiring verbatim evidence and an uncertainty option.

Failure modes / limitations: Missing outputs were excluded. One generation per article; prompt piloted on five papers. Reference coding was corrected after model disagreement. Difficult variables performed worse.

Supporting sources: [Automating data extraction in meta-research: A multi-model benchmark in network psychometrics papers](https://link.springer.com/article/10.3758/s13428-026-03052-7) · [Meta-research extraction original PDF, Table 1](https://link.springer.com/content/pdf/10.3758/s13428-026-03052-7.pdf)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Coding.repository_work (low confidence)

Repository maintenance is useful with substantial correction in the Russian RuBench setup; the product resolves only part of the sampled workload.

Scope: direct / conditional. Bounded to the explicitly evaluated task and recorded configuration.

Direct task IDs: coding.repository_work

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-b07849d170385317

Conditions: 25 Russian repository-maintenance tasks; 75 rollouts, 14/25,14/25,12/25 resolved; July 5–7, 2026.; Fresh macOS 15.7.3 arm64 workspaces; one-hour timeout; no custom instruction files.; Judge: withheld upstream regression tests. Wilson task-level 95% interval35–71%; all runs, no best-of selection.

Failure modes / limitations: Reported xhigh setting conflicts with Haiku manual-thinking documentation; effective thinking budget remains unknown.; Main text says web-tool restriction ineffective, appendix says web tools disabled; preserve this setup contradiction.; Private oracles, five repositories; no universal repository guarantee.

Supporting sources: [RuBench: A Repository-Level Agentic Coding Benchmark with Natively Authored Russian Task Specifications](https://arxiv.org/html/2607.06411v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence remains Low because effective thinking and web-tool setup are contradictory despite exact checkpoint and repeated runs.

### Coding.scoped_edit (low confidence)

Bulk one-shot Project Euler implementation in Java/Spring Boot produced few correct answers in these Haiku/CLI configurations, despite structural conformance. Do not transfer the nine easy Python-function result to this harder batched workload.

Scope: direct / warning. Directly measured task subset; neighboring tasks and unmeasured operating conditions are not endorsed.

Direct task IDs: coding.scoped_edit

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-b3102f36ea72719b

Conditions: 992 supplied problems per configuration. Cursor and Claude Code were tested separately. P1 grouped up to 100 methods per class; P2 used one class per problem. Each configuration was generated once and repair iteration was forbidden.

Failure modes / limitations: Correct answers ranged from 36 to 76 out of 992 across the four setups. Missing methods, wrong constants and runtime failures occurred. The exact checkpoint and effort were unreported.

Supporting sources: [An Empirical Evaluation of Cost-Efficient Large Language Models on Algorithmic Programming Tasks](https://arxiv.org/pdf/2609.18052)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Context.reasoning (low confidence)

Long-context graph traversal misses substantial required node relationships even when relevant edges remain present.

Scope: direct / warning. Bounded to the explicitly evaluated task and recorded configuration.

Direct task IDs: context.reasoning

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-b4b2fdfa65bc0ad1

Conditions: 50 longest BFS samples within 200k-token filter; median realized input about 68k; max output 4096; temperature 0.; Full signal-aware arm 0.538; 25%-retention 0.621. Separate naive full-context run 0.582, not a replicated mean.

Failure modes / limitations: Synthetic English graphs; selection seed fixed; no independent replication.; Effort, tool configuration, serving provider, exact run dates and precision undisclosed.; Header says August 4 while manuscript text says August 24; neither is a proven experiment date.

Supporting sources: [Distractor-Aware Truncation: Disentangling Context-Length Effects from Signal Loss in Long-Context LLM Benchmarks](https://arxiv.org/html/2608.03297v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: This supports a narrow caution for synthetic graph integration, not a claim about every long document.

### Language.instruction_following (low confidence)

An attributable Claude Code subagent report describes invented field names despite a supplied seven-dimension rubric.

Scope: direct / warning. Bounded source-specific finding; no transfer to other tasks or serving configurations.

Direct task IDs: language.instruction_following

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-b60f654a5d08e6d7

Conditions: March archive: six scenarios and 18 subagent evaluations; May API batch: thirteen scenarios and 39 calls.

Failure modes / limitations: Fourteen reported field-name substitutions; one refusal and one source-file lookup also reported.

Supporting sources: [Newer Is Not Better](https://augustinchan.dev/posts/2026-05-11-newer-isnt-better) · [ARA Eval archived Haiku subagent results](https://github.com/digital-rain-tech/ara-eval/blob/81438fc632de98313001271f7bb50e843622150c/shared/archive/leaderboard-2026-03-21-haiku-scored.json)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: F 2 percentages measure risk detection, not compliance rate. Different dates, scenario sets and harnesses preclude a controlled route/model regression claim.

### Language.instruction_following (low confidence)

Explicit length instructions improved a word-count closeness metric in a small paired test. This does not resolve exact-count failures: the metric gives partial credit and is not the strict exact-length pass rate claimed by some chart labels.

Scope: direct / warning. Directly measured task subset; neighboring tasks and unmeasured operating conditions are not endorsed.

Direct task IDs: language.instruction_following

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-b82993d0f0bc5b0a

Conditions: API request used claude-haiku-4-5 and the returned version was claude-haiku-4-5-20251001. Temperature 0; 10 tasks, five passes per arm collapsed to task pairs; target lengths of 25, 100 and 250 words.

Failure modes / limitations: Small fixed task set. Control used a bare number, not a vague instruction. Reported measurement dates are inconsistent. No strict exact-count pass denominator.

Supporting sources: [Open Addict exact-length experiment](https://openaddict.com/tips/exact-length) · [Open Addict full methodology](https://openaddict.com/methodology/full) · [Open Addict Haiku 4.5 measured prompting and skill results](https://openaddict.com/models/claude-haiku-4-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Knowledge.extraction (low confidence)

A four-document claim-extraction pipeline recovered about two-thirds of required claims under its fixed prompt and judge, supporting the need to inspect omissions rather than trust an apparently complete extraction.

Scope: direct / warning. Directly measured task subset; neighboring tasks and unmeasured operating conditions are not endorsed.

Direct task IDs: knowledge.extraction

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-d1715bde7b56a4b0

Conditions: 35 required claims across four cases, three runs on September 13, 2026. General-extractor 0.14.0, suite v0.2.0, embedding cosine threshold at least 0.80, Anthropic route with a 16,384-token output budget.

Failure modes / limitations: Prompt and judge were tuned for Sonnet. No acceptance threshold; alias without a verified served checkpoint; only four documents.

Supporting sources: [Particles provider extraction survey September 2026](https://docs.linkedparticles.org/benchmarks/provider-survey-2026-09/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Coding.review (low confidence)

In the VibeOps diff-only study, Haiku detects common synthetic defects but misses most issues in larger real pull-request diffs. Standalone broad review is unreliable under this prompt and context setup.

Scope: direct / warning. Directly measured task subset; neighboring tasks and unmeasured operating conditions are not endorsed.

Direct task IDs: coding.review

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-ead74c5a7dd5e11c

Conditions: 100 synthetic cases and 50 real pull requests. Every model received the same JSON prompt at temperature 0.1. Deterministic matching was followed by Opus 4.6 judging.

Failure modes / limitations: Real-PR F1 was 0.066, versus 0.847 on synthetic cases. Automatically extracted ground truth, one prompt and inconsistent summary tables limit confidence.

Supporting sources: [Bigger Is Not Always Better: Automated Code Review](https://arxiv.org/html/2606.15689v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Language.instruction_following (low confidence)

Conflicting tool-schema label definitions can displace correct system instructions in this compact Haiku classification setup.

Scope: direct / warning. Bounded source-specific finding; no transfer to other tasks or serving configurations.

Direct task IDs: language.instruction_following

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-fa364716cf875e26

Conditions: 48 messages; four nonce labels; five repeats; Anthropic rolling alias, temperature 0, max_tokens 2048, forced classify tool.

Failure modes / limitations: Incorrect lower-level schema definitions drive most labels under maximal conflict.

Supporting sources: [Your Prompt Is Not the Only Prompt: How Much Do LLMs Weight Structured-Output Schema Descriptions?](https://arxiv.org/html/2608.08254v1) · [Prompt Placement Effect Evaluation](https://github.com/alina-lin-phd/prompt-placement-eval)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: One study; schema-only reasoning-field improvement does not demonstrate conflict recovery.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 200000 |
| maximum output | 64000 |
| modalities | input: text; image; output: text |
| language support | Multilingual; exact inventory not specified |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

15 recorded access route(s); 2 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Anthropic Commercial Terms for hosted API

Restrictions: Hosted commercial API may power customer applications, subject to terms, Usage Policy and Supported Regions Policy.; No public weight redistribution license established; resale of the service, competing-model training and reverse engineering require separate authorization.

Commercial use: Hosted API permitted subject to Commercial Terms and applicable policies; not an unrestricted weight license.

Redistribution: Unknown / not established

Hosted service: Customer applications powered by the hosted API permitted subject to terms; direct service resale restricted.

Local weights/runtime availability: unavailable

Hardware: Not established in this pass

Local conditions: Not established in this pass

## Gaps and caveats

- Undisclosed architecture and parameter count
- Exact supported-language inventory and per-language quality not verified

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| anthropic | Standard / current | input: 1 USD / per 1 million tokens; output: 5 USD / per 1 million tokens; cached_input: 0.1 USD / per 1 million tokens; cache_write_5m: 1.25 USD / per 1 million tokens; cache_write_1h: 2 USD / per 1 million tokens | Not established in this pass | 2026-10-06 |
| anthropic | Batch / current | input: 0.5 USD / per 1 million tokens; output: 2.5 USD / per 1 million tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- anthropic / Claude API: officially_documented_not_execution_tested. Not established in this pass
- anthropic / Usage-based Claude Enterprise: Conditional consumer/client product; exact account entitlement unverified. Seat fee plus usage at API rates; this is a separately evidenced metered client route.
- google-cloud / Gemini Enterprise Agent Platform (formerly Vertex AI): officially_documented_not_execution_tested. Not established in this pass
- claude-platform-on-aws / Claude Platform on AWS: officially_documented_not_execution_tested. Separate Anthropic organization and AWS Marketplace enrollment; gateway region does not pin inference. Haiku 4.5 rejects inference_geo.
- azure-foundry / Claude in Microsoft Foundry: officially_documented_not_execution_tested. Foundry Claude is an Anthropic-operated Marketplace offering: Azure-hosted processing and Anthropic-hosted processing have distinct boundaries and safety-review exceptions.
- anthropic / Claude apps: Conditional consumer/client product; exact account entitlement unverified. Official model launch says all users; current plan table lists Haiku on Free and paid plans. Quotas apply; no per-token consumer free tariff.
- aws-bedrock / Amazon Bedrock: officially_documented_not_execution_tested. Runtime on-demand uses geo/global inference profiles; bare Haiku alias is Mantle-specific.; Haiku card lists Standard and Reserved; Priority and Flex unsupported.
- anthropic / Claude Code terminal and IDE: Conditional consumer/client product; exact account entitlement unverified. Full model IDs can be selected subject to plan and organization permissions. Separate subscription sign-in from API-key/partner billing.
- anthropic / Claude API: Active. quota: Tier/account-specific; exact numeric public tier table not captured
- aws-bedrock / Amazon Bedrock: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- azure-foundry / Microsoft Foundry / Azure: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- google-cloud / Google Cloud: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- anthropic / Claude Code terminal: All paid Claude plans include Code; API-credit billing is a separate option. quota: Shared with web/desktop/mobile plan pool; IDE entitlement details not separately verified
- anthropic / Claude Code IDE integrations: documented route; account eligibility unverified. Not established in this pass
- anthropic / Claude apps: Sonnet/Haiku families on Free and paid plans; version selection can change. quota: Rolling5h window; paid plans additionally weekly caps; no fixed message count

## Sources

[Claude haiku-4-5 specifications](https://platform.claude.com/docs/en/models/haiku-4-5/overview) · [Claude current model overview](https://platform.claude.com/docs/en/models/overview) · [Introducing Claude Haiku 4.5](https://www.anthropic.com/news/claude-haiku-4-5) · [Haiku non-reasoning benchmark comparison](https://artificialanalysis.ai/models/comparisons/hy3-vs-claude-4-5-haiku) · [Claude Haiku 4.5 May 10 benchmark](https://www.orcflo.com/orcflo-index/benchmarks/claude-haiku-4-5-2026-05-10) · [ORCFLO Index methodology](https://www.orcflo.com/orcflo-index/methodology)
