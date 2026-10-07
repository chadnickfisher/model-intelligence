# DeepSeek-V4.1-Flash

**Creator:** DeepSeek · **Family:** DeepSeek V4.1 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-10

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Input heavy tool agents (medium confidence)

Promising cost-oriented candidate for long-context coding/review and image-grounded tool tasks.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.repository_work; coding.review; agent.tool_use

Judgment ID: judgment-c78023ee7891bfab

Conditions: Check maximum reasoning effort versus task cost; preserve correct prompt encoding.

Failure modes / limitations: Creator DeepSWE results vary materially by harness; long traces, tool mistakes and invalid edits remain possible.

Supporting sources: [DeepSeek-V4.1-Flash model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) · [DeepSeek V4.1 Flash max independently profiled](https://artificialanalysis.ai/models/deepseek-v4-1-flash) · [DeepSeek live pricing and alias mapping](https://api-docs.deepseek.com/quick_start/pricing/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Coding.scoped_edit (low confidence)

Useful evidence for exact, fully specified file changes in the measured tooling; semantic edits remain unestablished.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.scoped_edit

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-9f7fdd9b0567b2b5

Conditions: Provider route: deepseek; 11 contributing harness families; detailed effort mix not extracted.; API/checkpoint identity follows source's exact named model; underlying quantization not supplied.; 226 tasks; shell/native editing tools allowed.; Score combines 75% initial exactness and 25% final exactness after permitted recovery.; Record describes a model route with mixed harnesses; do not interpret as pass@1 or a causal model ranking.

Failure modes / limitations: Some initial or final file trees failed exact comparison; this aggregate does not isolate the failure mechanism.

Supporting sources: [Explicit Edit Benchmark public data](https://huggingface.co/datasets/alexshpunt/explicit-edit-benchmark) · [Explicit Edit methodology](https://github.com/alexshpunt/explicit-edit-benchmark/blob/main/docs/methodology.md) · [Explicit Edit task definitions](https://github.com/alexshpunt/explicit-edit-benchmark/blob/main/docs/tasks.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: No matched independent contradictory evaluation located. This source establishes a narrow measured route, not a general ability ranking.; Potential transfer risk, not measured semantic failure: test-free byte matching does not establish a correct code change.; Confidence concerns this bounded claim, not a capability score.

### Coding.debugging (medium confidence)

Can repair a subset of hidden repository defects; use as an assisted audit, not a completeness guarantee.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-353d8b48d93065c6

Conditions: deepseek-flash served as V4.1;1M; no compactions; Claude Code2.1.267 then2.1.270.; Harness: Claude Code / DeepSeek API; effort: max; effort evidence: verified_ceiling.; 105 planted defects across TypeScript VS Code extension (~28K lines) and React/Supabase LMS (~60K lines).; One agentic round per repository; native CLI/tools; same task prompt but nonidentical harnesses, contexts and budgets.; Blind diff-based answer-key grading; extra unplanted fixes excluded; private corpus/judgments prevent full external reproduction.

Failure modes / limitations: Many planted defects remained unresolved in the measured runs.; Run variance and harness differences prevent fine-grained cross-model ranking.

Supporting sources: [Bug Hunt Bench frozen measurements](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/data/benchmark.json) · [Bug Hunt Bench receipts and boundaries](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/README.md) · [Bug Hunt Bench individual configuration caveats](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/run-notes.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Result measures finding AND implementing fixes; do not relabel it as code-review recall or test-generation quality.; No matched independent contradiction located; partial successes and misses coexist.; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-11ff03d00788ced6

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

### Self host cost savings (low confidence)

No automatic savings from open weights; utilization and infrastructure dominate.

Scope: performance / warning. Cost, deployment or throughput observation; not a task capability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-71e1895294a2759d

Conditions: Compare full GPU/RAM/operator cost with actual cached API token mix.

Failure modes / limitations: Underutilized hardware can cost more than API access.

Supporting sources: [DeepSeek-V4.1-Flash model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Causal encoder-decoder MoE with CSA2, sparse indexing, mHC, Engram lookup memory and DSpark draft module |
| parameters | total billion: 763; active billion: 16; scope: 763B serialized HF artifact; creator headline is 552B backbone, plus conditional memory and auxiliaries.; exact parameter count: Unknown / not established; backbone billion: 552; conditional memory billion: 196; active prefill billion: 8; active decode billion: 16 |
| context window | native tokens: 1000000; extended tokens: Unknown / not established; max output tokens: 384000; notes: 384K is first-party API limit; weight-card generation example recommends >=256K budget, not a separate model hard limit. |
| maximum output | 384000 |
| modalities | input: text; image; output: text |
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

Hardware: Datacenter or specialized workstation: 4-bit floor about 382GB for all serialized parameters; reserve substantially more RAM/HBM and confirm support.; 552B backbone + 196B Engram conditional memory; HF artifact reports 763B including auxiliary components. 8B active prefill / 16B decode excludes a simple universal active-count interpretation. Engram can be placed separately; no minimum verified.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| together | Standard / current | input: 0.3 USD / per 1 million tokens; output: 1.2 USD / per 1 million tokens; cached_input: 0.006 USD / per 1 million tokens | Together cache pricing is provider-specific; do not copy DeepSeek cache tariff. | 2026-10-07 |
| deepseek-api | peak / current | input: 0.3 USD / per_1000000_tokens; output: 1.2 USD / per_1000000_tokens; cached_input: 0.006 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Peak weekdays 01:00–04:00 and 06:00–10:00 UTC, excluding Chinese public holidays. Off-peak all other times. Reasoning and final tokens contribute to output billing. | 2026-10-06 |
| deepseek-api | off_peak / current | input: 0.15 USD / per_1000000_tokens; output: 0.6 USD / per_1000000_tokens; cached_input: 0.003 USD / per_1000000_tokens; cache_write: unknown USD / per_1000000_tokens | Peak weekdays 01:00–04:00 and 06:00–10:00 UTC, excluding Chinese public holidays. Off-peak all other times. Reasoning and final tokens contribute to output billing. | 2026-10-06 |

## Recorded access routes

- deepseek-api / DeepSeek API: documented_not_execution_tested. Not established in this pass
- together / hosted metered api: documented_not_execution_tested. Not established in this pass
- deepseek-api / hosted_api: documented route; account eligibility unverified. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is DeepSeek

## Sources

[huggingface.co](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/LICENSE) · [DeepSeek-V4.1-Flash model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) · [DeepSeek V4.1 Flash max independently profiled](https://artificialanalysis.ai/models/deepseek-v4-1-flash) · [DeepSeek live pricing and alias mapping](https://api-docs.deepseek.com/quick_start/pricing/)
