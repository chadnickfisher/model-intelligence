# Devstral Small 2 24B

**Creator:** Mistral AI · **Family:** Devstral · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2025-12-09

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Local coding agent (medium confidence)

A sensible local SWE candidate with image input and Apache terms.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: coding.repository_work

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-c9e6063835fd4526

Conditions: Use tested scaffold/tool parser; code changes still need tests and review.

Failure modes / limitations: Creator reports 68% SWE-bench Verified but only 22.5% Terminal Bench2; task breadth is uneven.

Supporting sources: [Devstral Small 2 24B model card](https://huggingface.co/mistralai/Devstral-Small-2-24B-Instruct-2512) · [Devstral Small2 independently profiled](https://artificialanalysis.ai/models/devstral-small-2)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Dense Ministral3-style decoder with vision |
| parameters | total billion: 24; active billion: 24; scope: creator-declared count; see notes; exact parameter count: Unknown / not established |
| context window | native tokens: 262144; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

1 recorded access route(s); 0 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Apache-2.0

Restrictions: Retain copyright/license notices; comply with the license.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: allowed

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Vendor positions single RTX4090 / 32GB-RAM Mac; use quantization for practical headroom.; 24B FP8 weights alone can exhaust a 24GB card; do not assume full-context fit from the marketing hardware statement. Planning 24–32GB with 4-bit, modest context.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|

## Recorded access routes

- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Mistral AI

## Sources

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) · [Devstral Small 2 24B model card](https://huggingface.co/mistralai/Devstral-Small-2-24B-Instruct-2512) · [Devstral Small2 independently profiled](https://artificialanalysis.ai/models/devstral-small-2)
