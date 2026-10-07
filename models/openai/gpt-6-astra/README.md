# GPT-6 Astra

**Creator:** OpenAI · **Family:** GPT-6 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-03

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Complex coding and computer workflows (medium confidence)

Strong candidate when difficult end-to-end work justifies latency and token cost.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.repository_work; agent.computer_use

Judgment ID: judgment-fbf53a2171375503

Conditions: AA harness/version and reasoning effort are material; these are not success probabilities for an arbitrary user task.

Failure modes / limitations: AA terminal tasks still fail at high and max effort; OpenAI documents legitimate work being interrupted by safety monitoring.

Supporting sources: [Astra high versus max benchmark comparison](https://artificialanalysis.ai/models/comparisons/gpt-6-astra-high-vs-gpt-6-astra) · [GPT-6 Astra: A new generation of intelligence](https://openai.com/index/gpt-6-astra/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: AA Terminal-Bench4.0: high54%, max59%; AutomationBench-AA high67%, max68%.; contradictory evidence: Higher effort is not uniformly better: AA-Omniscience high44 versus max43; GDP.pdf31% for both.; Observation obs-a91fd388dc88: Strong candidate when difficult end-to-end work justifies latency and token cost.; Potential risk (not a measured failure): Incorrect or out-of-scope actions remain possible; production safety monitors can stop legitimate work.

### Scientific research (medium confidence)

A strong escalation model for hard scientific workflows.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: reasoning.scientific

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-4e7af644a89ef0a9

Conditions: Maximum effort; tool-enabled scientific terminal workflow.

Failure modes / limitations: Not established in this pass

Supporting sources: [Introducing GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: OpenAI reports68.1% on Terminal-Bench Science0.1 in the Sol comparison.; contradictory evidence: Substantial residual failures; vendor-run setting and benchmark version affect results.; Observation obs-8eab532ce0f9: A strong escalation model for hard scientific workflows.; Potential risk (not a measured failure): Confident wrong derivations or incomplete experiments require independent verification.

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

7 recorded access route(s); 6 model-specific price record(s).

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
| openai | Standard / current | input: 10 USD / per 1 million tokens; cached_input: 1 USD / per 1 million tokens; cache_write: 12.5 USD / per 1 million tokens; output: 50 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Batch / current | input: 5.0 USD / per 1 million tokens; cached_input: 0.5 USD / per 1 million tokens; cache_write: 6.25 USD / per 1 million tokens; output: 25.0 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Flex / current | input: 5.0 USD / per 1 million tokens; cached_input: 0.5 USD / per 1 million tokens; cache_write: 6.25 USD / per 1 million tokens; output: 25.0 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Fast / current | input: 20 USD / per 1 million tokens; cached_input: 2 USD / per 1 million tokens; cache_write: 25.0 USD / per 1 million tokens; output: 100 USD / per 1 million tokens | input <=272000 tokens; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Standard / current | input: 20 USD / per 1 million tokens; cached_input: 2 USD / per 1 million tokens; cache_write: 25.0 USD / per 1 million tokens; output: 75.0 USD / per 1 million tokens | input >272000 tokens; full request uses long-context rates; Tool fees and regional/FedRAMP uplift | 2026-10-06 |
| openai | Ultrafast / current | input: 60 USD / per 1 million tokens; cached_input: 6 USD / per 1 million tokens; cache_write: 75 USD / per 1 million tokens; output: 300 USD / per 1 million tokens | short context; Tool fees and regional/FedRAMP uplift | 2026-10-06 |

## Recorded access routes

- openai / Responses / Chat Completions: Available; endpoint feature differences apply. quota: Tier/account dependent; actual remaining quota unknown; subscription_includes_api: false
- openai / ChatGPT: Eligible Plus/Pro/Business/Enterprise access; workspace permissions and current picker govern. quota: Included allowance and model-specific availability vary; not an unlimited API entitlement
- openai / ChatGPT Work: Paid-plan access; Luna also documented for Free/Go desktop. quota: Shared plan usage; actual allowance/reset account-specific
- openai / Codex CLI: Codex product access; paid plan or separately billed API authentication depends on setup. quota: Plan allowances are not model/API token limits
- openai / Codex IDE extension: Codex IDE product documented; model access still depends on account and workspace settings. quota: Plan allowances are not model/API token limits
- azure-foundry / Microsoft Foundry / Azure: Official launch names these providers; region, contract and prices not independently verified. Not established in this pass
- aws-bedrock / Amazon Bedrock: Official launch names these providers; region, contract and prices not independently verified. Not established in this pass

## Sources

[gpt-6-astra model specifications](https://developers.openai.com/api/docs/models/gpt-6-astra) · [OpenAI current model catalog](https://developers.openai.com/api/docs/models) · [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) · [Astra high versus max benchmark comparison](https://artificialanalysis.ai/models/comparisons/gpt-6-astra-high-vs-gpt-6-astra) · [GPT-6 Astra: A new generation of intelligence](https://openai.com/index/gpt-6-astra/) · [Introducing GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol/)
