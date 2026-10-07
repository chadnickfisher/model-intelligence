# GPT-Live 1

**Creator:** OpenAI · **Family:** GPT-Live · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-07-08

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Natural simultaneous listening and speaking (medium confidence)

Use for conversational flow with a separately configured reasoning backend.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: audio.conversation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-cc90e4fddce2d650

Conditions: Total cost includes both session duration and backend calls.

Failure modes / limitations: Not established in this pass

Supporting sources: [gpt-live-1 model specifications](https://developers.openai.com/api/docs/models/gpt-live-1) · [Introducing GPT-Live](https://openai.com/index/introducing-gpt-live/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: Official full-duplex design supports overlapping listen/speak and backend delegation.; contradictory evidence: Strong reasoning may come from the backend, not this voice model; no independent task evaluation recovered.; Observation obs-4797f27441f5: Use for conversational flow with a separately configured reasoning backend.; Potential risk (not a measured failure): Noise, interruptions and backend failure can still impair interaction; exact accuracy unknown.

### Agent.tool_use (low confidence)

Independent voice customer-support task results vary with the connected reasoning model and effort. They support the combined agent configurations, not GPT-Live alone.

Scope: direct / conditional. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: agent.tool_use

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-6fc6e6b6589624e3

Conditions: AA tau-Voice database end-state scoring with policies/tools; one trial per listed GPT-Live configuration.

Failure modes / limitations: Not established in this pass

Supporting sources: [Speech-to-speech benchmark configurations](https://artificialanalysis.ai/speech-to-speech?api-benchmarks=agentic-performance-vs-cost-to-run) · [gpt-live-1 model specifications](https://developers.openai.com/api/docs/models/gpt-live-1) · [Introducing GPT-Live](https://openai.com/index/introducing-gpt-live/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence beyond these systems: one trial, configuration dependence, not a controlled causal frontend comparison.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Full-duplex voice architecture; internal parameterization undisclosed |
| parameters | Unknown / not established |
| context window | Unknown / not established |
| maximum output | Unknown / not established |
| modalities | input: text; audio; output: text; audio |
| language support | Unknown / not established |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

5 recorded access route(s); 1 model-specific price record(s).

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
| openai | Standard / current | session: 0.05 USD / per session minute | Backend model and tool charges; per second; no whole-minute rounding | 2026-10-06 |

## Recorded access routes

- openai / ChatGPT Voice Live: Conditional consumer/client product; exact account entitlement unverified. GPT-Live-1: Plus 3h; Pro $100 15h; Pro $200 unlimited; Business Standard 3h and Premium 15h. Rolling 24 hours. Free and Go use mini.
- openai / Live sessions API: officially_documented_not_execution_tested. Not established in this pass
- azure-foundry / Azure GPT-Live: official_route_numeric_price_unverified. Not established in this pass
- openai / Live sessions API: Generally available. Not established in this pass
- openai / ChatGPT Voice: GPT-Live family powers Voice; exact routing and plan allotment may vary. Not established in this pass

## Sources

[gpt-live-1 model specifications](https://developers.openai.com/api/docs/models/gpt-live-1) · [Introducing GPT-Live](https://openai.com/index/introducing-gpt-live/) · [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) · [Speech-to-speech benchmark configurations](https://artificialanalysis.ai/speech-to-speech?api-benchmarks=agentic-performance-vs-cost-to-run)
