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

Generated tests require semantic checks after code changes, even when original-program tests pass.

Scope: direct / warning. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.tests

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-19237c319f0876ad

Conditions: Two-shot snippet workflow; dated API experiment; not ClaudeCode.; Named release matches; preserve source-specific provider, snapshot and precision limitations.

Failure modes / limitations: Behavioral changes materially reduced test pass rate.

Supporting sources: [Evaluating LLM-Based Test Generation Under Software Evolution](https://arxiv.org/html/2603.23443v1)

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

Conditions: Temperature zero; 200 single-turn literary prompts and 100 three-turn conversations.

Failure modes / limitations: Rule-based constraint compliance does not establish factual literary correctness or all-language instruction quality.

Supporting sources: [CAPITU: Instruction-Following in Brazilian Portuguese](https://arxiv.org/html/2603.22576v1)

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

A small business summarization evaluation supports a limited, conditional conclusion; verify retained facts and qualifications for the target material.

Scope: direct / conditional. The measured task fits this rubric boundary; no transfer to adjacent tasks.

Direct task IDs: language.summarization

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-d14d5e6960fa913c

Conditions: May 10 cohort; English single-turn text; five cases in this category, four LLM judges.

Failure modes / limitations: No public full response traces, immutable serving revision or independent replication.

Supporting sources: [Claude Haiku 4.5 May 10 benchmark](https://www.orcflo.com/orcflo-index/benchmarks/claude-haiku-4-5-2026-05-10) · [ORCFLO Index methodology](https://www.orcflo.com/orcflo-index/methodology)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence reflects limited tasks, source/setup uncertainty and lack of independent replication; scores do not define confidence. Empty contradictory evidence means none was located in this bounded pass.

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

Conditions: Anthropic API, temperature zero, eight-shot examples, tuned format and reasoning prefill; no code execution in CoT.

Failure modes / limitations: Immutable revision unknown; prompt tuning and familiar corpus; two collection runs; numerical answer matching does not evaluate proofs.

Supporting sources: [Reasoning, Code, or Both? Variations in Math Questions](https://arxiv.org/html/2605.26414v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Direct task scope follows the reported output and metric; confidence is low because this is one bounded study with the stated setup limitations.

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

[Claude haiku-4-5 specifications](https://platform.claude.com/docs/en/models/haiku-4-5/overview) · [Claude current model overview](https://platform.claude.com/docs/en/models/overview) · [Introducing Claude Haiku 4.5](https://www.anthropic.com/news/claude-haiku-4-5) · [Haiku non-reasoning benchmark comparison](https://artificialanalysis.ai/models/comparisons/hy3-vs-claude-4-5-haiku)
