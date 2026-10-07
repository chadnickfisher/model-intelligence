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

7 recorded access route(s); 2 model-specific price record(s).

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

- anthropic / Claude API: Active. quota: Tier/account-specific; exact numeric public tier table not captured
- aws-bedrock / Amazon Bedrock: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- google-cloud / Google Cloud: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- azure-foundry / Microsoft Foundry / Azure: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- anthropic / Claude Code terminal: All paid Claude plans include Code; API-credit billing is a separate option. quota: Shared with web/desktop/mobile plan pool; IDE entitlement details not separately verified
- anthropic / Claude Code IDE integrations: documented route; account eligibility unverified. Not established in this pass
- anthropic / Claude apps: Sonnet/Haiku families on Free and paid plans; version selection can change. quota: Rolling5h window; paid plans additionally weekly caps; no fixed message count

## Sources

[Claude sonnet-5-5 specifications](https://platform.claude.com/docs/en/models/sonnet-5-5/overview) · [Claude current model overview](https://platform.claude.com/docs/en/models/overview) · [Claude Sonnet 5.5 independent analysis](https://artificialanalysis.ai/articles/claude-sonnet-5-5/) · [Introducing Claude Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5)
