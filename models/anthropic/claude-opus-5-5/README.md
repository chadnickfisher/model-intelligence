# Claude Opus 5.5

**Creator:** Anthropic · **Family:** Claude 5 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-22

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Agentic coding and knowledge work (medium confidence)

Strong balanced candidate for sustained open-ended professional work.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.repository_work; research.synthesis

Judgment ID: judgment-a58a16e37a99fdcb

Conditions: Independent benchmark harness; default fallback makes this a served configuration, not isolated weights.

Failure modes / limitations: Cited Terminal-Bench4.0 all-tests-pass result leaves about40% of tasks unsuccessful.

Supporting sources: [Claude Opus 5.5 independent analysis](https://artificialanalysis.ai/articles/claude-opus-5-5) · [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5) · [Claude opus-5-5 specifications](https://platform.claude.com/docs/en/models/opus-5-5/overview)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: AA max/default fallback: Terminal-Bench4.0 59.6%; SciCode66.9%; HLE61.4%.; contradictory evidence: About40% of terminal benchmark tasks still fail; task-specific leaders differ.; Observation obs-ec41174a4588: Strong balanced candidate for sustained open-ended professional work.; Potential risk (not a measured failure): Residual prompt-injection vulnerability and out-of-scope actions; always-on thinking affects latency.

### Coding.debugging (medium confidence)

Can repair a subset of hidden repository defects; use as an assisted audit, not a completeness guarantee.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-e494146b5a163111

Conditions: Claude Code;1M window; zero compactions in this run group.; Harness: Claude Code; effort: max; effort evidence: first_party.; 105 planted defects across TypeScript VS Code extension (~28K lines) and React/Supabase LMS (~60K lines).; One agentic round per repository; native CLI/tools; same task prompt but nonidentical harnesses, contexts and budgets.; Blind diff-based answer-key grading; extra unplanted fixes excluded; private corpus/judgments prevent full external reproduction.

Failure modes / limitations: Many planted defects remained unresolved in the measured runs.; Run variance and harness differences prevent fine-grained cross-model ranking.

Supporting sources: [Bug Hunt Bench frozen measurements](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/data/benchmark.json) · [Bug Hunt Bench receipts and boundaries](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/README.md) · [Bug Hunt Bench individual configuration caveats](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/run-notes.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Result measures finding AND implementing fixes; do not relabel it as code-review recall or test-generation quality.; No matched independent contradiction located; partial successes and misses coexist.; Confidence concerns this bounded claim, not a capability score.

### Coding.architecture (low confidence)

Candidate for cross-service design work; support remains vendor-curated practitioner evidence.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.architecture

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-f5926189f36cd899

Conditions: Vendor-curated early-access account; effort and acceptance checks unspecified.

Failure modes / limitations: No concrete failure case disclosed.

Supporting sources: [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: One selected testimonial. Anthropic's HAProxy C-to-Rust migration report is adjacent migration evidence, not a same-language behavior-preserving refactoring benchmark.; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-cd273215e58beb5c

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

### Coding.review (medium confidence)

Useful validated-review candidate; more effort changes recall and noise rather than improving both.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.review

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-7992397f38f55c00

Conditions: Use the recorded CodeRabbit pipeline mixes; verify on representative PRs.; Named release matches; preserve source-specific provider, snapshot and precision limitations.

Failure modes / limitations: Known bugs missed; many actionable comments did not pass the judge.

Supporting sources: [Claude Opus 5.5 for code review: More catches, different misses](https://www.coderabbit.ai/blog/opus-5-5-model-review)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

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
| anthropic | Standard / current | input: 4 USD / per 1 million tokens; output: 20 USD / per 1 million tokens; cached_input: 0.2 USD / per 1 million tokens; cache_write_5m: 5.0 USD / per 1 million tokens; cache_write_1h: 8 USD / per 1 million tokens | Not established in this pass | 2026-10-06 |
| anthropic | Batch / current | input: 2.0 USD / per 1 million tokens; output: 10.0 USD / per 1 million tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- google-cloud / Gemini Enterprise Agent Platform (formerly Vertex AI): officially_documented_not_execution_tested. Not established in this pass
- azure-foundry / Claude in Microsoft Foundry: officially_documented_not_execution_tested. Not established in this pass
- aws-bedrock / Amazon Bedrock: officially_documented_not_execution_tested. Not established in this pass
- anthropic / Claude API: officially_documented_not_execution_tested. Not established in this pass
- anthropic / Claude apps: Conditional consumer/client product; exact account entitlement unverified. Pro, Max, Team and Enterprise; no Free Opus entitlement.
- claude-platform-on-aws / Claude Platform on AWS: officially_documented_not_execution_tested. Not established in this pass
- anthropic / Claude Code terminal and IDE: Conditional consumer/client product; exact account entitlement unverified. Full model IDs can be selected subject to plan and organization permissions. Separate subscription sign-in from API-key/partner billing.
- anthropic / Usage-based Claude Enterprise: Conditional consumer/client product; exact account entitlement unverified. Seat fee plus usage at API rates; this is a separately evidenced metered client route.
- anthropic / Claude API: Active. quota: Tier/account-specific; exact numeric public tier table not captured
- aws-bedrock / Amazon Bedrock: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- azure-foundry / Microsoft Foundry / Azure: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- google-cloud / Google Cloud: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- anthropic / Claude Code terminal: All paid Claude plans include Code; API-credit billing is a separate option. quota: Shared with web/desktop/mobile plan pool; IDE entitlement details not separately verified
- anthropic / Claude Code IDE integrations: documented route; account eligibility unverified. Not established in this pass
- anthropic / Claude apps: Opus family on paid plans. quota: Same shared usage pool; model weighting/actual remainder account-specific

## Sources

[Claude opus-5-5 specifications](https://platform.claude.com/docs/en/models/opus-5-5/overview) · [Claude current model overview](https://platform.claude.com/docs/en/models/overview) · [Claude Opus 5.5 independent analysis](https://artificialanalysis.ai/articles/claude-opus-5-5) · [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5)
