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

Evidence notes: Research provenance: history/research/2026-10-07/coding-input.json :: review_tests_frontend:frontend-arena-claude-haiku-4-5; Confidence concerns this bounded claim, not a capability score.

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

Evidence notes: Research provenance: history/research/2026-10-07/coding-input.json :: review_tests_frontend:tests-haiku; Confidence concerns this bounded claim, not a capability score.

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
| anthropic | Standard / current | input: 1 USD / per 1 million tokens; output: 5 USD / per 1 million tokens; cached_input: 0.1 USD / per 1 million tokens; cache_write_5m: 1.25 USD / per 1 million tokens; cache_write_1h: 2 USD / per 1 million tokens | Not established in this pass | 2026-10-06 |
| anthropic | Batch / current | input: 0.5 USD / per 1 million tokens; output: 2.5 USD / per 1 million tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- anthropic / Claude API: officially_documented_not_execution_tested. Not established in this pass
- anthropic / Usage-based Claude Enterprise: Conditional consumer/client product; exact account entitlement unverified. Seat fee plus usage at API rates; this is a separately evidenced metered client route.
- google-cloud / Gemini Enterprise Agent Platform (formerly Vertex AI): officially_documented_not_execution_tested. Not established in this pass
- claude-platform-on-aws / Claude Platform on AWS: officially_documented_not_execution_tested. Not established in this pass
- azure-foundry / Claude in Microsoft Foundry: officially_documented_not_execution_tested. Not established in this pass
- anthropic / Claude apps: Conditional consumer/client product; exact account entitlement unverified. Official model launch says all users; current plan table lists Haiku on Free and paid plans. Quotas apply; no per-token consumer free tariff.
- aws-bedrock / Amazon Bedrock: officially_documented_not_execution_tested. Not established in this pass
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
