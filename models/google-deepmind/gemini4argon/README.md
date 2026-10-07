# Gemini 4 Argon

**Creator:** Google DeepMind · **Family:** Gemini · **Status:** preview
**Verified:** 2026-10-06 · **Release:** 2026-09-30

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Long horizon coding and enterprise agent workflows when access is available (medium confidence)

Promising early-access candidate; independent task results support coding potential but do not establish broad deployment reliability.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): agent.long_horizon; coding.repository_work; agent.tool_use

Judgment ID: judgment-fa3a1a5a01173cf2

Conditions: Google; high reasoning; temperature 1; output cap 262144; Vals used $4/$20 regular token pricing, high effort; costs differ from announced promo

Failure modes / limitations: Not established in this pass

Supporting sources: [Vals AI Gemini 4 Argon](https://www.vals.ai/models/google_gemini-4-argon)

Contradictory or limiting sources: [Vals AI Gemini 4 Argon](https://www.vals.ai/models/google_gemini-4-argon) · [Introducing Gemini 4 Argon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) · [Gemini API model catalog](https://ai.google.dev/gemini-api/docs/models) · [Artificial Analysis Gemini 4 Argon High](https://artificialanalysis.ai/models/gemini-4-argon)

Evidence notes: Public-source synthesis; no inference runs.; Observation obs-ac88874e3783: Independent early-access results are strong on code migration and terminal tasks but much weaker on CUA-bench and fully resolved ProgramBench.; Observation obs-917f279500bc: Announced Sep 30 for selected Fairwind defenders; general developer/consumer access described as forthcoming.; Observation obs-f5e1684ef252: Long tasks can be costly; independent evaluator reports high costs for CUA and code migration, using regular prices.

### Coding.frontend (low confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-0134f7d02c624e6b

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Research provenance: history/research/2026-10-07/coding-input.json :: review_tests_frontend:frontend-arena-gemini4argon; Confidence concerns this bounded claim, not a capability score.

### Measured generation behavior (medium confidence)

Long tasks can be costly; independent evaluator reports high costs for CUA and code migration, using regular prices. Measurements: {"AA_output_tokens_index": 110000000, "AA_output_tokens_per_second": null}. These describe the cited benchmark configuration only.

Scope: performance / conditional. Cost, deployment or throughput observation; not a task capability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-eeb7184ebb549554

Conditions: Vals used $4/$20 regular token pricing, high effort; costs differ from announced promo

Failure modes / limitations: Not established in this pass

Supporting sources: [Vals AI Gemini 4 Argon](https://www.vals.ai/models/google_gemini-4-argon) · [Artificial Analysis Gemini 4 Argon High](https://artificialanalysis.ai/models/gemini-4-argon)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Benchmark costs are not typical user costs or provider tariffs.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | Unknown / not established |
| maximum output | Unknown / not established |
| modalities | input: text; image; output: text |
| language support | Unknown / not established |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

4 recorded access route(s); 2 model-specific price record(s).

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

- Public API endpoint identifier and GA date
- Architecture and parameters
- Exact deployable context and output limits
- Public latency and quota
- Complete input modalities and languages
- Exact introductory price expiry in main English announcement

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| google-developer-api | announced_intro / unknown | input: 2 USD / per_1M_tokens; output: 10 USD / per_1M_tokens; cache_read: 0.1 USD / per_1M_tokens | Announced future introductory API price; cached input derived from explicit 95% discount. No exact public endpoint or effective date verified. | 2026-10-06 |
| google-developer-api | announced_regular / unknown | input: 4 USD / per_1M_tokens; output: 20 USD / per_1M_tokens | Announced price after introductory period; expiry date is not specified in the fetched main English announcement. | 2026-10-06 |

## Recorded access routes

- google-developer-api / Gemini 4 Argon: restricted_rollout_announced_broad_API_not_verified. Not established in this pass
- google-ai / Google AI Ultra: Conditional consumer/client product; exact account entitlement unverified. Named for future broad rollout. Current general subscriber entitlement not established.
- google-developer-api / first-party-api: documented route; account eligibility unverified. Not established in this pass
- google-ai-studio / Google AI Studio: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass

## Sources

[Introducing Gemini 4 Argon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) · [Artificial Analysis Gemini 4 Argon High](https://artificialanalysis.ai/models/gemini-4-argon) · [Vals AI Gemini 4 Argon](https://www.vals.ai/models/google_gemini-4-argon)
