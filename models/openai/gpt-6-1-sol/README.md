# GPT-6.1 Sol

**Creator:** OpenAI · **Family:** GPT-6 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-29

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Coding and document reasoning at constrained spend (medium confidence)

Useful first comparison against Astra for routine complex work.

Conditions: Same named max effort; harness and token usage differ across models.

Failure modes / limitations: Lower SciCode and AA-LCR results than GPT-6 Sol in the cited max-effort comparison.

Supporting sources: [GPT-6.1 Sol versus GPT-6 Sol, max effort](https://artificialanalysis.ai/models/comparisons/gpt-6-1-sol-vs-gpt-6-sol)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: AA max: Terminal-Bench4.0 rises44% to56% versus GPT-6 Sol; GDP.pdf25% to31%.; contradictory evidence: SciCode declines58% to54%; AA-LCR84% to83%. Newer is not better on every task.; Observation obs-e5d2a15ea501: Useful first comparison against Astra for routine complex work.; Potential risk (not a measured failure): Long-context misses and task-specific coding regressions.

### Factual answers and tool backed research (medium confidence)

Improved but requires checking sources and tool failures.

Conditions: Use current retrieval for changing facts.

Failure modes / limitations: Vendor selected error-inducing prompts still produce factual errors; this is not typical-use prevalence.

Supporting sources: [Introducing GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: OpenAI difficult-prompt factual error rate:7.7% versus11.4% for GPT-6 Sol at low effort.; contradictory evidence: This is a selected error-inducing set, not ordinary-use prevalence.; Observation obs-c5c416a3125b: Improved but requires checking sources and tool failures.; Potential risk (not a measured failure): Undisclosed search failure remains possible; fabricated certainty.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 1050000 |
| maximum output | 128000 |
| modalities | input: text; image; output: text |
| language support | Multilingual; exact inventory not specified |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

5 recorded access route(s); 5 model-specific price record(s).

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
| openai | Standard / current | input: 2 USD / per 1 million tokens; cached_input: 0.1 USD / per 1 million tokens; cache_write: 2.5 USD / per 1 million tokens; output: 10 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Batch / current | input: 1.0 USD / per 1 million tokens; cached_input: 0.05 USD / per 1 million tokens; cache_write: 1.25 USD / per 1 million tokens; output: 5.0 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Flex / current | input: 1.0 USD / per 1 million tokens; cached_input: 0.05 USD / per 1 million tokens; cache_write: 1.25 USD / per 1 million tokens; output: 5.0 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Fast / current | input: 4 USD / per 1 million tokens; cached_input: 0.2 USD / per 1 million tokens; cache_write: 5.0 USD / per 1 million tokens; output: 20 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Standard / current | input: 4 USD / per 1 million tokens; cached_input: 0.2 USD / per 1 million tokens; cache_write: 5.0 USD / per 1 million tokens; output: 15.0 USD / per 1 million tokens | input >272000 tokens; full request uses long-context rates; Tool fees and regional/FedRAMP uplift | 2026-10-06 |

## Recorded access routes

- openai / Responses / Chat Completions: Available; endpoint feature differences apply. quota: Tier/account dependent; actual remaining quota unknown; subscription_includes_api: false
- openai / ChatGPT Work: Paid-plan access; Luna also documented for Free/Go desktop. quota: Shared plan usage; actual allowance/reset account-specific
- openai / Codex CLI: Codex product access; paid plan or separately billed API authentication depends on setup. quota: Plan allowances are not model/API token limits
- openai / Codex IDE extension: Codex IDE product documented; model access still depends on account and workspace settings. quota: Plan allowances are not model/API token limits
- openai / ChatGPT Chat: Not yet available in Chat according to current launch/help documentation. Not established in this pass

## Sources

[gpt-6.1-sol model specifications](https://developers.openai.com/api/docs/models/gpt-6.1-sol) · [OpenAI current model catalog](https://developers.openai.com/api/docs/models) · [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) · [GPT-6.1 Sol versus GPT-6 Sol, max effort](https://artificialanalysis.ai/models/comparisons/gpt-6-1-sol-vs-gpt-6-sol) · [Introducing GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol/)
