# GPT-Realtime 2.1

**Creator:** OpenAI · **Family:** GPT-Realtime · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-07-06

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Tool using speech agents (medium confidence)

Consider when reasoning and tools must operate in a realtime speech session.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: audio.conversation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-cf3c0c86e40306ed

Conditions: Audio-token pricing cannot be compared directly with Live session-minute pricing.

Failure modes / limitations: Not established in this pass

Supporting sources: [gpt-realtime-2.1 model specifications](https://developers.openai.com/api/docs/models/gpt-realtime-2.1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: Vendor documents stronger alphanumeric recognition, noise/silence and interruption behavior over Realtime2.; contradictory evidence: No independent version-matched evidence recovered; higher reasoning effort increases latency and output consumption.; Observation obs-d95f95883e10: Consider when reasoning and tools must operate in a realtime speech session.; Potential risk (not a measured failure): Recognition errors in identifiers; latency-sensitive turn-taking; tool error recovery.

### Agent.tool_use (low confidence)

Independent voice customer-support task completion depends on reasoning effort; use the exact 2.1 High and Minimal configurations, without borrowing Mini results.

Scope: direct / conditional. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: agent.tool_use

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-8d4fb0af2cb7e4fe

Conditions: AA tau-Voice simulated customer support with domain tools and policies; High uses two trials.

Failure modes / limitations: Not established in this pass

Supporting sources: [Speech-to-speech benchmark configurations](https://artificialanalysis.ai/speech-to-speech?api-benchmarks=agentic-performance-vs-cost-to-run) · [gpt-realtime-2.1 model specifications](https://developers.openai.com/api/docs/models/gpt-realtime-2.1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence beyond the measured agent systems: few trials, rolling alias and incomplete configuration.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 128000 |
| maximum output | 32000 |
| modalities | input: text; image; audio; output: text; audio |
| language support | Unknown / not established |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

4 recorded access route(s); 3 model-specific price record(s).

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
| openai | Standard / current | input: 4 USD / per 1 million text tokens; cached_input: 0.4 USD / per 1 million text tokens; output: 24 USD / per 1 million text tokens | Not established in this pass | 2026-10-06 |
| openai | Standard / current | input: 32 USD / per 1 million audio tokens; cached_input: 0.4 USD / per 1 million audio tokens; output: 64 USD / per 1 million audio tokens | Not established in this pass | 2026-10-06 |
| openai | Standard / current | input: 5 USD / per 1 million image tokens; cached_input: 0.5 USD / per 1 million image tokens; output: unknown USD / per 1 million image tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- azure-foundry / Azure Realtime API: official_route_numeric_price_unverified. Not established in this pass
- openai / Realtime API: officially_documented_not_execution_tested. Not established in this pass
- openai / ChatGPT Voice: Conditional consumer/client product; exact account entitlement unverified. No exact GPT-Realtime-2.1 consumer entitlement established; Advanced mode presence is not a model-alias mapping.
- openai / Realtime API: Available. quota: {"actual_account_remaining": null, "free": "not supported", "tier1": {"RPD": 1000, "RPM": 200, "TPM": 40000}}

## Sources

[gpt-realtime-2.1 model specifications](https://developers.openai.com/api/docs/models/gpt-realtime-2.1) · [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) · [developers.openai.com](https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini) · [Speech-to-speech benchmark configurations](https://artificialanalysis.ai/speech-to-speech?api-benchmarks=agentic-performance-vs-cost-to-run)
