# Mistral Large 3 675B Instruct

**Creator:** Mistral AI · **Family:** Mistral Large · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2025-12-02

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Non reasoning multilingual rag (medium confidence)

A permissively licensed non-thinking option for enterprise document/chat pipelines with datacenter resources.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: knowledge.rag

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-98414fc2b50374ec

Conditions: Keep tool schemas bounded and validate image aspect-ratio handling.

Failure modes / limitations: Card explicitly notes weaker strict reasoning than reasoning specialists and weaker vision than vision-first models.

Supporting sources: [Mistral Large 3 675B Instruct model card](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512) · [Mistral Large3 independently profiled](https://artificialanalysis.ai/models/mistral-large-3)

Contradictory or limiting sources: [Mistral Large3 independently profiled](https://artificialanalysis.ai/models/mistral-large-3)

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-70b7c0b4e8adbe58

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Granular MoE language model plus 2.5B vision encoder |
| parameters | total billion: 675; active billion: 41; scope: creator-declared count; see notes; exact parameter count: Unknown / not established |
| context window | native tokens: 262144; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

5 recorded access route(s); 2 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Apache-2.0

Restrictions: Retain copyright/license notices; comply with the license.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: allowed

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Vendor: FP8 on one 8×H200 node; NVFP4 on one node of H100s/A100s.; 675B/41B headline combines language/vision; card separately lists 673B/39B LM plus 2.5B vision encoder, rounded differently.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| mistral-api | Standard / current | input: 0.5 USD / per 1 million tokens; output: 1.5 USD / per 1 million tokens; cached_input: 0.05 USD / per 1 million tokens | Rates are standard. Batch/priority/regional tiers distinct; do not infer a default account tier. | 2026-10-07 |
| mistral-api | standard / historical | input: 0.5 USD / per_1000000_tokens; output: 1.5 USD / per_1000000_tokens; cached_input: 0.05 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Default standard tier; regional inference, batch and priority may have different rates. | 2026-10-06 |

## Recorded access routes

- mistral-api / Mistral API Standard: documented_not_execution_tested. Not established in this pass
- mistral-api / Mistral plan included API usage: documented_not_execution_tested. Not established in this pass
- fireworks / On-demand GPU deployment: documented_not_execution_tested. Not established in this pass
- mistral-api / hosted_api: documented route; account eligibility unverified. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Mistral AI

## Sources

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) · [Mistral Large 3 675B Instruct model card](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512) · [Mistral Large3 independently profiled](https://artificialanalysis.ai/models/mistral-large-3)
