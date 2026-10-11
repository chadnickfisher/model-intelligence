# Eleven v4

**Creator:** ElevenLabs · **Family:** Eleven · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-28

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Expressive multilingual narration and dialogue (low confidence)

Current documented flagship for expressive/cloned voices; credible shortlist candidate, but independent v4 preference/accuracy results not verified.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: audio.speech_generation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-e6e019022a901615

Conditions: Not established in this pass

Failure modes / limitations: Not established in this pass

Supporting sources: [Models](https://elevenlabs.io/docs/overview/models)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Observation obs-7f1696b1081e: Current flagship multilingual synthesis and dialogue features.

### Audio.speech_generation (low confidence)

Eleven v4 has independent provider-voice preference evidence. This supports listening-quality evaluation, not guaranteed pronunciation or accuracy across every supported language.

Scope: direct / conditional. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: audio.speech_generation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-96525c869cedff6c

Conditions: AA Provider Voice Arena; representative provider voices, not the controlled cloned-voice arena.

Failure modes / limitations: Not established in this pass

Supporting sources: [Eleven v4 Provider Voice Arena](https://artificialanalysis.ai/text-to-speech/models/eleven-v4) · [Text-to-speech evaluation methodology](https://artificialanalysis.ai/methodology/text-to-speech) · [Models](https://elevenlabs.io/docs/overview/models)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence in broad task generalization: one dynamic preference evaluation with incomplete voice/language configuration.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | Unknown / not established |
| maximum output | Unknown / not established |
| modalities | input: text; output: speech; multi-speaker dialogue |
| language support | 90+ |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

3 recorded access route(s); 1 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: commercial service terms and voice-rights restrictions

Restrictions: Not established in this pass

Commercial use: Unknown / not established

Redistribution: Unknown / not established

Hosted service: Unknown / not established

Local weights/runtime availability: unavailable

Hardware: Not established in this pass

Local conditions: Not established in this pass

## Gaps and caveats

- Voice likeness/consent rights are separate from technical cloning capability.
- API promo expires Oct12; pricing should not be treated as stable.
- Latency claims for Turbo exclude application/network overhead.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| elevenlabs | Free / PayGo displayed / current | text: 0.022 USD / per 1,000 characters | Displayed temporary $0.022 per 1000 characters promotion until October 12, 2026; undiscounted displayed rate $0.08. Exact ending instant is not specified.; Prices exclude taxes, levies and duties; subscription allowances remain separate. | 2026-10-11 |

## Recorded access routes

- elevenlabs / ElevenCreative speech playground: documented_public_route; account_entitlement_not_execution_tested. Applicable regional terms require age 18 or local legal majority and necessary voice/input rights; the v4 FAQ requires verified voice-owner consent.; Free use is noncommercial; commercial rights under paid subscriptions remain subject to policies. A PayGo purchase alone is not treated as a commercial-use grant.; Regional sensitive-input restrictions and applicable Creative terms govern this UI route; API-specific exceptions are not treated as UI permissions.
- elevenlabs / ElevenAPI Starter: documented_public_route; account_entitlement_not_execution_tested. Applicable regional terms require age 18 or local legal majority and necessary voice/input rights; the v4 FAQ requires verified voice-owner consent.; Free use is noncommercial; commercial rights under paid subscriptions remain subject to policies. A PayGo purchase alone is not treated as a commercial-use grant.; Health and other sensitive inputs have regional and service-specific restrictions. API section 4.2 has scoped exceptions; no general eligibility is inferred.
- elevenlabs / ElevenAPI PayGo: documented_public_route; account_entitlement_not_execution_tested. Applicable regional terms require age 18 or local legal majority and necessary voice/input rights; the v4 FAQ requires verified voice-owner consent.; Free use is noncommercial; commercial rights under paid subscriptions remain subject to policies. A PayGo purchase alone is not treated as a commercial-use grant.; Health and other sensitive inputs have regional and service-specific restrictions. API section 4.2 has scoped exceptions; no general eligibility is inferred.

## Sources

[Models](https://elevenlabs.io/docs/overview/models) · [ElevenAPI Pricing](https://elevenlabs.io/pricing/api) · [Eleven v4 Provider Voice Arena](https://artificialanalysis.ai/text-to-speech/models/eleven-v4) · [Text-to-speech evaluation methodology](https://artificialanalysis.ai/methodology/text-to-speech) · [September 28, 2026 changelog](https://elevenlabs.io/docs/changelog/2026/9/28)
