# Claude Sonnet 5.5

**Creator:** Anthropic · **Family:** Claude 5 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-28

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Coding at different effort budgets (medium confidence)

Strong terminal/task benchmark performer; tune effort rather than assuming maximum is best.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: coding.repository_work

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-8418f911db37869b

Conditions: AA max/default fallback; creator and AA terminal scores differ because setups differ.

Failure modes / limitations: Vendor reports two inspected max-effort FrontierCode cases with timeout or out-of-scope extra edits from expanded subagent review.

Supporting sources: [Claude Sonnet 5.5 independent analysis](https://artificialanalysis.ai/articles/claude-sonnet-5-5/) · [Introducing Claude Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: AA reports Terminal-Bench4.0 about64% at max and knowledge-work results near Opus5.5.; contradictory evidence: Anthropic FrontierCode: max46.2%, xhigh52.1%; extra subagent reviews caused timeout or out-of-scope edits.; Observation obs-3416d44a445c: Strong terminal/task benchmark performer; tune effort rather than assuming maximum is best.; Potential risk (not a measured failure): Overworking, scope expansion, timeouts and large reasoning bills.

### Coding.scoped_edit (low confidence)

For bounded changes, maximum effort can expand scope and reduce merge-readiness.

Scope: direct / warning. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.scoped_edit

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-cb9aeb423bbdc834

Conditions: Claude Code FrontierCode1.1; vendor comparison at max versus xhigh.

Failure modes / limitations: Two inspected cases linked expanded subagent review to timeout or extra edits.

Supporting sources: [Introducing Claude Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Inspected failure cases are direct scoped-edit evidence; aggregate FrontierCode is not reclassified into every coding task.; Confidence concerns this bounded claim, not a capability score.

### Coding.debugging (medium confidence)

Can repair a subset of hidden repository defects; use as an assisted audit, not a completeness guarantee.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-fb34061351983c89

Conditions: claude-sonnet-5-5[1m]; Claude Code2.1.283; compaction occurred.; Harness: Claude Code; effort: max; effort evidence: first_party.; 105 planted defects across TypeScript VS Code extension (~28K lines) and React/Supabase LMS (~60K lines).; One agentic round per repository; native CLI/tools; same task prompt but nonidentical harnesses, contexts and budgets.; Blind diff-based answer-key grading; extra unplanted fixes excluded; private corpus/judgments prevent full external reproduction.

Failure modes / limitations: Many planted defects remained unresolved in the measured runs.; Run variance and harness differences prevent fine-grained cross-model ranking.

Supporting sources: [Bug Hunt Bench frozen measurements](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/data/benchmark.json) · [Bug Hunt Bench receipts and boundaries](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/README.md) · [Bug Hunt Bench individual configuration caveats](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/run-notes.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Result measures finding AND implementing fixes; do not relabel it as code-review recall or test-generation quality.; No matched independent contradiction located; partial successes and misses coexist.; Confidence concerns this bounded claim, not a capability score.

### Coding.architecture (low confidence)

Promising for architecture audits, based on a selected customer report with undisclosed evaluation details.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.architecture

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-6a100733d93912cd

Conditions: Vendor-curated early-access testimonial; multi-hour work; effort, prompts, code and scoring unpublished.

Failure modes / limitations: No case-specific failures disclosed.

Supporting sources: [Introducing Claude Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Supports architecture analysis candidacy, not general architecture-design reliability.; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-6696d66817b015d5

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

### Coding.review (low confidence)

Promising faster review option, with weaker hard-case coverage than Opus 5.5 in the matched subset.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.review

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-116a3f541aaf26e7

Conditions: Quality conclusion limited to judged Signal cases.; Named release matches; preserve source-specific provider, snapshot and precision limitations.; Thinking toggles apply across a mixed-effort review pipeline; smaller models handle summaries and verification.; The larger OSS run supports latency and comment volume only while judge scoring is pending.

Failure modes / limitations: Do not treat unjudged OSS comment reductions as quality gains.

Supporting sources: [Claude Sonnet 5.5 for code review: More catches than Sonnet 5, in half the time](https://www.coderabbit.ai/blog/sonnet-5-5-model-review)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.; CodeRabbit judged 13 Signal cases; thinking-on caught 6 while thinking-off caught 5. The 44-PR OSS run still lacked quality scoring.; Low confidence reflects the inspected evaluator, corpus/pipeline dependence and unpublished replication inputs; it is not a low ability rating.

### Coding.refactoring (low confidence)

One small shipping-cost refactor preserved the tested behavior, including coercion edge cases; broader restructuring remains unvalidated.

Scope: direct / conditional. Direct conclusion is limited to this task and the stated published configuration; no transfer to neighboring tasks.

Direct task IDs: coding.refactoring

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-1d166a8ffd058c04

Conditions: OneSeptember 28 reply via llmwise/OpenRouter; eight Node.js fixture checks,8000-token cap; effort and downstream provider unknown.

Failure modes / limitations: Passing eight checks does not prove equivalence for all inputs or larger cross-module refactors.

Supporting sources: [AI prompts for coding, checked by running the code](https://llmwise.ai/prompts/for/coding)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: One task with eight checks, not eight independent samples. The marketing refactor sketch from Kunya is not treated as executed preservation evidence.

### Language.writing (medium confidence)

Produces fluent, well-structured German expositions, but substantive factual and lexical claims require checking despite favorable blind ratings.

Scope: direct / conditional. Exactly one supplied task rubric under the recorded setup.

Direct task IDs: language.writing

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-595a98b01c403e74

Conditions: Seventeen passages × English/German instruction variants =34 Sonnet outputs; exact claude-sonnet-5-5 traces datedOctober 3.; Author reports adaptive high effort; trace labels adaptive without a numeric budget; identical source packets, no web.

Failure modes / limitations: Judges flagged seven serious issues per prompt-language condition, including invented translator identity and incorrect word/family facts.; Two automated judges, private system prompts and one application constrain generalization.

Supporting sources: [Kolibri vs Claude Sonnet 5.5: A German LLM Benchmark](https://tej.as/blog/kolibri-vs-claude-german-llm-benchmark) · [Dewfall German study original generation traces](https://tej.as/blog/kolibri-vs-claude-german-llm-benchmark/traces/runs.jsonl) · [Dewfall German study judge verdicts](https://tej.as/blog/kolibri-vs-claude-german-llm-benchmark/traces/verdicts.jsonl)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: 8.7/10 rounded mean in each condition; 68 absolute Sonnet judgments.; 136 paired verdicts comprise17 inputs ×2 prompt variants ×2 judges ×2 presentation orders; they are not independent generation trials.

### Language.instruction_following (low confidence)

Retained all seven required section tags in the34 observed German expositions; broader semantic-constraint compliance remains unmeasured.

Scope: direct / conditional. Exactly one supplied task rubric under the recorded setup.

Direct task IDs: language.instruction_following

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-6158a48b2e47c111

Conditions: Same17 inputs with two prompt-language variants; exact seven tags verified in every Sonnet output.

Failure modes / limitations: Correct parsing does not establish every instruction or source-fidelity requirement; private system prompts prevent full contract checking.

Supporting sources: [Kolibri vs Claude Sonnet 5.5: A German LLM Benchmark](https://tej.as/blog/kolibri-vs-claude-german-llm-benchmark) · [Dewfall German study original generation traces](https://tej.as/blog/kolibri-vs-claude-german-llm-benchmark/traces/runs.jsonl) · [Dewfall German study judge verdicts](https://tej.as/blog/kolibri-vs-claude-german-llm-benchmark/traces/verdicts.jsonl)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: 17/17 outputs per prompt variant parsed; content errors remain despite format success.

### Coding.scoped_edit (low confidence)

Small specified JavaScript functions passed the publisher acceptance fixtures; use explicit acceptance tests before expanding to repository changes.

Scope: direct / conditional. Direct conclusion is limited to this task and the stated published configuration; no transfer to neighboring tasks.

Direct task IDs: coding.scoped_edit

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-6f5d23ad596ea68c

Conditions: One reply per fixture through llmwise/OpenRouter; ISBN-10 function8tests and hashtag function5tests; no effort disclosed.

Failure modes / limitations: Tiny isolated examples do not establish reliable edits across an existing repository.

Supporting sources: [AI prompts for coding, checked by running the code](https://llmwise.ai/prompts/for/coding)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Tests were executed by the publisher; this research inspected their original outputs and reported outcomes only.

### Vision.grounding (medium confidence)

Zero-shot boxes provide useful localization but need spatial correction; coarse-overlap success does not establish precise grounding.

Scope: direct / conditional. Exactly one supplied task rubric under the recorded setup.

Direct task IDs: vision.grounding

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-b96cb26fcff545d2

Conditions: Normalized y-min/x-min/y-max/x-max boxes and labels; three runs at each low/high native effort.

Failure modes / limitations: mAP@50 is74.3 low/76.8 high, while mAP@75 is60.0/63.1 and mAP@50: 95 is57.1/59.5.; Sample denominator and precise model route not disclosed; no GUI-action success inferred.

Supporting sources: [Object Detection Benchmark](https://playground.roboflow.com/evals/object-detection) · [Vision Evals methodology](https://playground.roboflow.com/evals)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: mAP metrics score object detection and overlap, not an all-objects-correct rate.

### Vision.question_answering (medium confidence)

Useful for image-grounded comparisons and spatial questions with material answer checking in both effort settings.

Scope: direct / conditional. Exactly one supplied task rubric under the recorded setup.

Direct task IDs: vision.question_answering

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-de743a67836582cd

Conditions: Three runs each at low/high native effort; same visual samples; Gemini 3.5 Flash temperature0 grades against ground truth.

Failure modes / limitations: Low judged accuracy76.4% versus strict11.9%; high83.9% versus strict72.8%; verbosity affects strict matching.; Sample denominator, exact endpoint and run dates not disclosed; range is not a confidence interval.

Supporting sources: [Visual Reasoning Benchmark](https://playground.roboflow.com/evals/visual-reasoning) · [Vision Evals methodology](https://playground.roboflow.com/evals)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Reported±0.7 low and±1.7 high are half-ranges over three runs, not standard deviations.

### Cost sensitive professional workflows (medium confidence)

Low per-token price is useful only when effort and total tokens are controlled.

Scope: performance / conditional. Cost, deployment or throughput observation; not a task capability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-d11bf2f6847f9b57

Conditions: Different effort/workload distributions explain divergent conclusions; max is not app-default medium.

Failure modes / limitations: AA max-effort run used approximately193k output tokens/task and higher benchmark cost than predecessor.

Supporting sources: [Introducing Claude Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5) · [Claude Sonnet 5.5 independent analysis](https://artificialanalysis.ai/articles/claude-sonnet-5-5/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Conservative baseline confidence: broader convergence has not been independently audited.; supporting evidence: Vendor reports up to30% less cost/task than Sonnet5 in its testing.; contradictory evidence: AA max uses approximately193k output tokens/task and costs$7.60/task, about50% above Sonnet5 on its suite.; Observation obs-8ed2b3f90f11: Low per-token price is useful only when effort and total tokens are controlled.; Potential risk (not a measured failure): Subscription allowance or API budget can be exhausted by long reasoning.

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

16 recorded access route(s); 2 model-specific price record(s).

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
| anthropic | Standard / current | input: 2 USD / per 1 million tokens; output: 10 USD / per 1 million tokens; cached_input: unknown USD / per 1 million tokens; cache_write_5m: 2.5 USD / per 1 million tokens; cache_write_1h: 4 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |
| anthropic | Batch / current | input: 1.0 USD / per 1 million tokens; output: 5.0 USD / per 1 million tokens | Not established in this pass | 2026-10-07 |

## Recorded access routes

- claude-platform-on-aws / Claude Platform on AWS: officially_documented_not_execution_tested. Not established in this pass
- aws-bedrock / Amazon Bedrock: officially_documented_not_execution_tested. Not established in this pass
- azure-foundry / Claude in Microsoft Foundry / Hosted on Anthropic: officially_documented_not_execution_tested. Message Batches, Models API and server-side fallback are unsupported on Foundry.; New computer/browser toolsets are unsupported; older beta computer tools are separate.
- anthropic / Usage-based Claude Enterprise: Conditional consumer/client product; exact account entitlement unverified. Seat fee plus usage at API rates; this is a separately evidenced metered client route.
- anthropic / Claude API: officially_documented_not_execution_tested. Not established in this pass
- google-cloud / Gemini Enterprise Agent Platform (formerly Vertex AI): officially_documented_not_execution_tested. Not established in this pass
- anthropic / Claude apps: Conditional consumer/client product; exact account entitlement unverified. 5.5 app model is documented; current plan table lists Sonnet for Free and paid plans. Exact Free picker routing/remaining allowance not verified.
- azure-foundry / Claude in Microsoft Foundry / Hosted on Azure: officially_documented_not_execution_tested. Message Batches, Models API and server-side fallback are unsupported on Foundry.; New computer/browser toolsets are unsupported; older beta computer tools are separate.; Code execution, Files API, Agent Skills and programmatic tool calling are unsupported on Azure hosting.; Azure hosting permits only basic web_search_20250305 and web_fetch_20250910 tools.; Sonnet 5.5 supports Global Standard only; US Data Zone is unavailable.
- anthropic / Claude Code terminal and IDE: Conditional consumer/client product; exact account entitlement unverified. Full model IDs can be selected subject to plan and organization permissions. Separate subscription sign-in from API-key/partner billing.
- anthropic / Claude API: Active. quota: Tier/account-specific; exact numeric public tier table not captured
- aws-bedrock / Amazon Bedrock: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- azure-foundry / Microsoft Foundry / Azure: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- google-cloud / Google Cloud: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- anthropic / Claude Code terminal: All paid Claude plans include Code; API-credit billing is a separate option. quota: Shared with web/desktop/mobile plan pool; IDE entitlement details not separately verified
- anthropic / Claude Code IDE integrations: documented route; account eligibility unverified. Not established in this pass
- anthropic / Claude apps: Sonnet/Haiku families on Free and paid plans; version selection can change. quota: Rolling5h window; paid plans additionally weekly caps; no fixed message count

## Sources

[Claude sonnet-5-5 specifications](https://platform.claude.com/docs/en/models/sonnet-5-5/overview) · [Claude current model overview](https://platform.claude.com/docs/en/models/overview) · [Claude Sonnet 5.5 independent analysis](https://artificialanalysis.ai/articles/claude-sonnet-5-5/) · [Introducing Claude Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5)
