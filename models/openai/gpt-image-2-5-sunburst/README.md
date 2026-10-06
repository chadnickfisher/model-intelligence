# GPT Image 2.5 Sunburst

**Creator:** OpenAI · **Family:** GPT Image2.5 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-08

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Image editing (medium confidence)

Precision-oriented editing choice.

Conditions: Quality, resolution, reference images and retries change consumption.

Failure modes / limitations: Not established in this pass

Supporting sources: [Introducing ChatGPT Images 2.5](https://openai.com/index/introducing-chatgpt-images-2-5/) · [gpt-image-2.5-sunburst model specifications](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst) · [Create image API reference](https://developers.openai.com/api/reference/resources/images/methods/generate)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: Vendor positions Sunburst for finer editing control and Flare for faster generation.; contradictory evidence: No independent model-specific head-to-head recovered in this bounded pass; equal token prices do not imply equal cost per image.; Observation obs-b01421e4dbca: Precision-oriented editing choice.; Potential risk (not a measured failure): Inspect text, local edits and identity consistency; these checks are prudent risk controls, not measured failure rates.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | Unknown / not established |
| maximum output | Unknown / not established |
| modalities | input: text; image; output: image |
| language support | Unknown / not established |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

2 recorded access route(s); 3 model-specific price record(s).

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
| openai | Standard / current | input: 5 USD / per 1 million text tokens; cached_input: 1.25 USD / per 1 million text tokens; output: unknown USD / per 1 million text tokens | Input image/text charges; actual output token consumption varies | 2026-10-06 |
| openai | Standard / current | input: 8 USD / per 1 million image tokens; cached_input: 2 USD / per 1 million image tokens; output: 30 USD / per 1 million image tokens | Input image/text charges; actual output token consumption varies | 2026-10-06 |
| openai | Batch / current | output: 15 USD / per 1 million image output tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- openai / Images API / Responses image-generation tool: Available. quota: Usage tier/account-specific; no fixed image count inferred
- openai / ChatGPT Images2.5 / Work / Codex: Images2.5 available across tiers; precise underlying API variant selection in each UI not established. Not established in this pass

## Sources

[gpt-image-2.5-sunburst model specifications](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst) · [Introducing ChatGPT Images 2.5](https://openai.com/index/introducing-chatgpt-images-2-5/) · [Create image API reference](https://developers.openai.com/api/reference/resources/images/methods/generate)
