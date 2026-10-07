# GPT-6 Luna

**Creator:** OpenAI · **Family:** GPT-6 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-22

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Focused high volume tasks (medium confidence)

Good low-token-price option for bounded, validated subtasks.

Scope: unresolved / conditional. Scope needs review; the original claim does not establish a specific task ability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.scoped_edit; language.instruction_following

Judgment ID: judgment-0c281701a4185869

Conditions: Reasoning settings and harness matter; DeepSWE and Terminal-Bench are different tests.

Failure modes / limitations: Only13% all-tests-pass on cited AA Terminal-Bench4.0 at max effort.

Supporting sources: [GPT-6 Luna max benchmark comparison](https://artificialanalysis.ai/models/comparisons/gpt-6-luna-vs-gpt-5-3-codex) · [Introducing GPT-6 Sol and Luna](https://openai.com/index/introducing-gpt-6-sol-and-luna/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: AA max AA-LCR83%; vendor DeepSWE66.6% in its own setup.; contradictory evidence: AA max Terminal-Bench4.0 only13%, GDP.pdf23%; narrower competence than price marketing suggests.; Observation obs-18449a135e8c: Good low-token-price option for bounded, validated subtasks.; Potential risk (not a measured failure): Brittle long-horizon work; weak factual calibration; use deterministic checks.

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
| openai | Standard / current | input: 0.1 USD / per 1 million tokens; cached_input: 0.01 USD / per 1 million tokens; cache_write: 0.125 USD / per 1 million tokens; output: 0.5 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Batch / current | input: 0.05 USD / per 1 million tokens; cached_input: 0.005 USD / per 1 million tokens; cache_write: 0.0625 USD / per 1 million tokens; output: 0.25 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Flex / current | input: 0.05 USD / per 1 million tokens; cached_input: 0.005 USD / per 1 million tokens; cache_write: 0.0625 USD / per 1 million tokens; output: 0.25 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Fast / current | input: 0.2 USD / per 1 million tokens; cached_input: 0.02 USD / per 1 million tokens; cache_write: 0.25 USD / per 1 million tokens; output: 1.0 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Standard / current | input: 0.2 USD / per 1 million tokens; cached_input: 0.02 USD / per 1 million tokens; cache_write: 0.25 USD / per 1 million tokens; output: 0.75 USD / per 1 million tokens | input >272000 tokens; full request uses long-context rates; Tool fees and regional/FedRAMP uplift | 2026-10-06 |

## Recorded access routes

- openai / Responses / Chat Completions: Available; endpoint feature differences apply. quota: Tier/account dependent; actual remaining quota unknown; subscription_includes_api: false
- openai / ChatGPT Work: Paid-plan access; Luna also documented for Free/Go desktop. quota: Shared plan usage; actual allowance/reset account-specific
- openai / Codex CLI: Codex product access; paid plan or separately billed API authentication depends on setup. quota: Plan allowances are not model/API token limits
- openai / Codex IDE extension: Codex IDE product documented; model access still depends on account and workspace settings. quota: Plan allowances are not model/API token limits
- openai / ChatGPT Chat: Not yet available in Chat according to current launch/help documentation. Not established in this pass

## Sources

[gpt-6-luna model specifications](https://developers.openai.com/api/docs/models/gpt-6-luna) · [OpenAI current model catalog](https://developers.openai.com/api/docs/models) · [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) · [GPT-6 Luna max benchmark comparison](https://artificialanalysis.ai/models/comparisons/gpt-6-luna-vs-gpt-5-3-codex) · [Introducing GPT-6 Sol and Luna](https://openai.com/index/introducing-gpt-6-sol-and-luna/)
