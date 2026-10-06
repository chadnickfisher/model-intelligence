# Grok 4.7

**Creator:** xAI / SpaceXAI · **Family:** Grok · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-21

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Agentic coding and knowledge workflows (medium confidence)

Credible candidate; medium confidence for task-fit. AA's xhigh snapshot improves Terminal-Bench 4.0 from 21% (4.6 high) to 26%, but costs roughly twice per evaluated task.

Conditions: Grok4.7 xhigh vs Grok4.6 high, first-party API

Failure modes / limitations: Not established in this pass

Supporting sources: [artificialanalysis.ai](https://artificialanalysis.ai/models/comparisons/grok-4-7-vs-grok-4-6)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Observation obs-281c2bae7ad0: AA Intelligence Index v4.3.2 and component tasks

### Low latency assistance (medium confidence)

Not a latency-first default at high reasoning effort; evaluate low effort or alternatives.

Conditions: Grok4.7 xhigh vs Grok4.6 high, first-party API

Failure modes / limitations: Not established in this pass

Supporting sources: [artificialanalysis.ai](https://artificialanalysis.ai/models/comparisons/grok-4-7-vs-grok-4-6)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Observation obs-281c2bae7ad0: AA Intelligence Index v4.3.2 and component tasks

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 500000 |
| maximum output | Unknown / not established |
| modalities | input: text; image; output: text |
| language support | Unknown / not established |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

0 recorded access route(s); 3 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: proprietary service terms

Restrictions: Not established in this pass

Commercial use: Unknown / not established

Redistribution: Unknown / not established

Hosted service: Unknown / not established

Local weights/runtime availability: unavailable

Hardware: Not established in this pass

Local conditions: Not established in this pass

## Gaps and caveats

- Real-time facts require search tools; model alone has no live event access.
- Do not equate published context capacity with perfect long-context recall.
- Price depends on prompt length, tool charges and actual reasoning-token usage.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| xai | standard, short context / current | input: 2 USD / per 1M tokens; cached_input: 0.5 USD / per 1M tokens; output: 6 USD / per 1M tokens | Higher-context pricing exists above 200k; exact boundary/rates require reconciliation with general page. These are base displayed rates.; not stated | 2026-10-06 |
| opencode-zen | prompt <=200k / current | input: 2 USD / per 1M tokens; cached_input: 0.5 USD / per 1M tokens; output: 6 USD / per 1M tokens | Not established in this pass | 2026-10-06 |
| opencode-zen | prompt >200k / current | input: 4 USD / per 1M tokens; cached_input: 1 USD / per 1M tokens; output: 12 USD / per 1M tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes


## Sources

[artificialanalysis.ai](https://artificialanalysis.ai/models/grok-4-7-high) · [docs.x.ai](https://docs.x.ai/developers/models/grok-4.7) · [docs.x.ai](https://docs.x.ai/developers/models) · [artificialanalysis.ai](https://artificialanalysis.ai/models/comparisons/grok-4-7-vs-grok-4-6)
