# DeepSeek-V4-Pro-0813

**Creator:** DeepSeek · **Family:** DeepSeek V4 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-08-13

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Text coding and reasoning (low confidence)

Officially supersedes Preview and remains a capable text-agent option.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.repository_work; reasoning.general

Judgment ID: judgment-790070519743c4cd

Conditions: Use 0813 evidence, not April preview scores; reasoning low/high/max changes behavior.

Failure modes / limitations: Text-only; system-level results depend on DeepSeek Harness; no independent checkpoint-matched test established here.

Supporting sources: [DeepSeek-V4-Pro-0813 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813) · [DeepSeek live pricing and alias mapping](https://api-docs.deepseek.com/quick_start/pricing/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence limited by vendor-heavy task evidence and missing exact-task independent replication; documented interface support alone is not task quality.

### Coding.debugging (low confidence)

A supplied fix plan can make this snapshot useful for supervised repair; independent bug discovery remains less certain.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-abdefeccf40296a5

Conditions: One private Python/PySide6 project;15-item plan with locations and expected behavior; opencode1.18.16,MCP,LSP.

Failure modes / limitations: Earlier read-only hunt found1/3known latent bugs.; Follow-up implementation omitted a portability fallback and expanded one parameter across17call sites.

Supporting sources: [DeepSeek V4 Pro 0813 implementation follow-up](https://www.reddit.com/r/DeepSeek/comments/1vnhvka/deepseek_v4_flash_0731_vs_deepseek_v4_pro_0813/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Author reports unchanged preexisting failures and no new static errors. No public code independently checked; do not inherit oldFlash0731results intoV4.1.; The analysis report bounds independent bug discovery; it does not contradict repair after locations are supplied.; Confidence concerns this bounded claim, not a capability score.

### Coding.architecture (low confidence)

Useful structural-review/planning candidate, with materially variable coverage requiring verification.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.architecture

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-69601f8f65af2a8c

Conditions: Opencode 1.18.16, identical fresh read-only sessions, code graph/search/history, MCP/LSP; six task types; architecture review targeted 7k-line module. Claims checked by another model and verifier.

Failure modes / limitations: Depth varied 2.7x across repeated architecture runs; Pro missed 2 of 3 known latent bugs.

Supporting sources: [DeepSeek V4 Pro 0813 code-analysis experiment](https://www.reddit.com/r/DeepSeek/comments/1vnc7u7/deepseek_v4_flash_0731_vs_deepseek_v4_pro_0813_i/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: No public code/logs; cross-task 95.9% claim accuracy is not architecture-specific. Reject author's inference that references are safe without verification.; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-ebf0fffcc7897fe9

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

### Coding.review (medium confidence)

Candidate for focused diff review with parser validation and independent checking.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.review

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-ab69f47538efa196

Conditions: Use exact 0813 endpoint; no transfer to moving deepseek-chat alias.; Named release matches; preserve source-specific provider, snapshot and precision limitations.

Failure modes / limitations: Missed planted issues and deceptive tests; malformed responses can silently approve.

Supporting sources: [Living AI code review benchmark](https://diffdojo.com/benchmark.html)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

### Coding.tests (low confidence)

One controlled private-project report supports regression-test generation from explicit fix plans.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.tests

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-2dc5f95e9caa652e

Conditions: OpenCode 1.18.16; Python/PySide 6; required tests specified.; Named release matches; preserve source-specific provider, snapshot and precision limitations.

Failure modes / limitations: Concurrency case omitted.

Supporting sources: [DeepSeek V4 Pro 0813 implementation follow-up](https://www.reddit.com/r/DeepSeek/comments/1vnhvka/deepseek_v4_flash_0731_vs_deepseek_v4_pro_0813/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Sparse-attention MoE V4 backbone plus DSpark speculative decoder |
| parameters | total billion: 1600; active billion: 49; scope: 1.6T backbone; HF full artifact rounds to 1.7T; exact all-component total not verified.; exact parameter count: Unknown / not established |
| context window | native tokens: 1000000; extended tokens: Unknown / not established; max output tokens: 384000; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | 384000 |
| modalities | input: text; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

4 recorded access route(s); 3 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: MIT

Restrictions: Retain copyright/license notices; comply with the license.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: allowed

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Datacenter-scale multi-GPU/multi-node; ideal 4-bit backbone alone roughly 800GB.; HF serialized artifact rounds to 1.7T due to auxiliary modules; real storage floor is higher than the headline-backbone calculation.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.
- Independent 0813-only reproducible comparison not verified.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| together | Standard / current | input: 1.32 USD / per 1 million tokens; output: 3.96 USD / per 1 million tokens; cached_input: 0.13 USD / per 1 million tokens | Together cache pricing is provider-specific; do not copy DeepSeek cache tariff. | 2026-10-07 |
| deepseek-api | off_peak / current | input: 0.66 USD / per_1000000_tokens; output: 1.98 USD / per_1000000_tokens; cached_input: 0.022 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Peak weekdays 01:00–04:00 and 06:00–10:00 UTC, excluding Chinese public holidays. Off-peak all other times. Reasoning and final tokens contribute to output billing. | 2026-10-06 |
| deepseek-api | peak / current | input: 1.32 USD / per_1000000_tokens; output: 3.96 USD / per_1000000_tokens; cached_input: 0.044 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Peak weekdays 01:00–04:00 and 06:00–10:00 UTC, excluding Chinese public holidays. Off-peak all other times. Reasoning and final tokens contribute to output billing. | 2026-10-06 |

## Recorded access routes

- together / hosted metered api: documented_not_execution_tested. Not established in this pass
- deepseek-api / DeepSeek API: documented_not_execution_tested. Not established in this pass
- deepseek-api / hosted_api: documented route; account eligibility unverified. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is DeepSeek

## Sources

[huggingface.co](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813/blob/main/LICENSE) · [DeepSeek-V4-Pro-0813 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813) · [DeepSeek live pricing and alias mapping](https://api-docs.deepseek.com/quick_start/pricing/) · [DeepSeek V4 architecture introduction](https://deepseek.com/en/news/v4-preview/)
