# Claude Opus 5.5

**Creator:** Anthropic · **Family:** Claude 5 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-22

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Agentic coding and knowledge work (medium confidence)

Strong balanced candidate for sustained open-ended professional work.

Conditions: Independent benchmark harness; default fallback makes this a served configuration, not isolated weights.

Failure modes / limitations: Cited Terminal-Bench4.0 all-tests-pass result leaves about40% of tasks unsuccessful.

Supporting sources: [Claude Opus 5.5 independent analysis](https://artificialanalysis.ai/articles/claude-opus-5-5) · [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5) · [Claude opus-5-5 specifications](https://platform.claude.com/docs/en/models/opus-5-5/overview)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: AA max/default fallback: Terminal-Bench4.0 59.6%; SciCode66.9%; HLE61.4%.; contradictory evidence: About40% of terminal benchmark tasks still fail; task-specific leaders differ.; Observation obs-ec41174a4588: Strong balanced candidate for sustained open-ended professional work.; Potential risk (not a measured failure): Residual prompt-injection vulnerability and out-of-scope actions; always-on thinking affects latency.

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
| anthropic | Standard / current | input: 4 USD / per 1 million tokens; output: 20 USD / per 1 million tokens; cached_input: 0.2 USD / per 1 million tokens; cache_write_5m: 5.0 USD / per 1 million tokens; cache_write_1h: 8 USD / per 1 million tokens | Not established in this pass | 2026-10-06 |
| anthropic | Batch / current | input: 2.0 USD / per 1 million tokens; output: 10.0 USD / per 1 million tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- anthropic / Claude API: Active. quota: Tier/account-specific; exact numeric public tier table not captured
- aws-bedrock / Amazon Bedrock: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- google-cloud / Google Cloud: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- azure-foundry / Microsoft Foundry / Azure: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- anthropic / Claude Code terminal: All paid Claude plans include Code; API-credit billing is a separate option. quota: Shared with web/desktop/mobile plan pool; IDE entitlement details not separately verified
- anthropic / Claude Code IDE integrations: documented route; account eligibility unverified. Not established in this pass
- anthropic / Claude apps: Opus family on paid plans. quota: Same shared usage pool; model weighting/actual remainder account-specific

## Sources

[Claude opus-5-5 specifications](https://platform.claude.com/docs/en/models/opus-5-5/overview) · [Claude current model overview](https://platform.claude.com/docs/en/models/overview) · [Claude Opus 5.5 independent analysis](https://artificialanalysis.ai/articles/claude-opus-5-5) · [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5)
