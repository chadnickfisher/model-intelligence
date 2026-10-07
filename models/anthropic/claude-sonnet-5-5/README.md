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

Evidence notes: Inspected failure cases are direct scoped-edit evidence; aggregate FrontierCode is not reclassified into every coding task.; Research provenance: history/research/2026-10-07/coding-input.json :: scoped_debugging:claude-sonnet-5-5-scoped-max-warning; Confidence concerns this bounded claim, not a capability score.

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

Evidence notes: Result measures finding AND implementing fixes; do not relabel it as code-review recall or test-generation quality.; No matched independent contradiction located; partial successes and misses coexist.; Research provenance: history/research/2026-10-07/coding-input.json :: scoped_debugging:claude-sonnet-5-5-debug-bughunt; Confidence concerns this bounded claim, not a capability score.

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

Evidence notes: Supports architecture analysis candidacy, not general architecture-design reliability.; Research provenance: history/research/2026-10-07/coding-input.json :: architecture_refactoring:A02; Confidence concerns this bounded claim, not a capability score.

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

Evidence notes: Research provenance: history/research/2026-10-07/coding-input.json :: review_tests_frontend:frontend-arena-claude-sonnet-5-5; Confidence concerns this bounded claim, not a capability score.

### Coding.review (medium confidence)

Promising faster review option, with weaker hard-case coverage than Opus 5.5 in the matched subset.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.review

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-116a3f541aaf26e7

Conditions: Quality conclusion limited to judged Signal cases.; Named release matches; preserve source-specific provider, snapshot and precision limitations.

Failure modes / limitations: Do not treat unjudged OSS comment reductions as quality gains.

Supporting sources: [Claude Sonnet 5.5 for code review: More catches than Sonnet 5, in half the time](https://www.coderabbit.ai/blog/sonnet-5-5-model-review)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Research provenance: history/research/2026-10-07/coding-input.json :: review_tests_frontend:review-sonnet55; Confidence concerns this bounded claim, not a capability score.

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
| anthropic | Standard / current | input: 2 USD / per 1 million tokens; output: 10 USD / per 1 million tokens; cached_input: 0.2 USD / per 1 million tokens; cache_write_5m: 2.5 USD / per 1 million tokens; cache_write_1h: 4 USD / per 1 million tokens | Not established in this pass | 2026-10-06 |
| anthropic | Batch / current | input: 1.0 USD / per 1 million tokens; output: 5.0 USD / per 1 million tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- claude-platform-on-aws / Claude Platform on AWS: officially_documented_not_execution_tested. Not established in this pass
- aws-bedrock / Amazon Bedrock: officially_documented_not_execution_tested. Not established in this pass
- anthropic / Usage-based Claude Enterprise: Conditional consumer/client product; exact account entitlement unverified. Seat fee plus usage at API rates; this is a separately evidenced metered client route.
- anthropic / Claude API: officially_documented_not_execution_tested. Not established in this pass
- google-cloud / Gemini Enterprise Agent Platform (formerly Vertex AI): officially_documented_not_execution_tested. Not established in this pass
- anthropic / Claude apps: Conditional consumer/client product; exact account entitlement unverified. 5.5 app model is documented; current plan table lists Sonnet for Free and paid plans. Exact Free picker routing/remaining allowance not verified.
- azure-foundry / Claude in Microsoft Foundry: officially_documented_not_execution_tested. Not established in this pass
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
