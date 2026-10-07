# Kimi K3

**Creator:** Moonshot AI · **Family:** Kimi · **Status:** active
**Verified:** 2026-10-06 · **Release:** Unknown

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Long horizon multimodal agents (medium confidence)

Strong candidate for large-scale visual coding and tool-based knowledge work if cost and license are acceptable.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): agent.long_horizon; coding.repository_work; research.synthesis

Judgment ID: judgment-ce599538fb19f653

Conditions: Thinking is always on; preserve complete returned assistant messages including reasoning and tool fields.

Failure modes / limitations: Harness-dependent benchmark results; visual tasks still fail; preserving long histories increases costs.

Supporting sources: [Kimi K3 model card](https://huggingface.co/moonshotai/Kimi-K3) · [Kimi K3 max independently profiled](https://artificialanalysis.ai/models/kimi-k3)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Coding.debugging (low confidence)

Can repair a subset of hidden repository defects; use as an assisted audit, not a completeness guarantee.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-b00034cf95cef727

Conditions: Route's effort field inert; do not describe this as Kimi maximum effort.; Harness: Claude Code / OpenRouter; effort: default; effort evidence: inert_default.; 105 planted defects across TypeScript VS Code extension (~28K lines) and React/Supabase LMS (~60K lines).; One agentic round per repository; native CLI/tools; same task prompt but nonidentical harnesses, contexts and budgets.; Blind diff-based answer-key grading; extra unplanted fixes excluded; private corpus/judgments prevent full external reproduction.

Failure modes / limitations: Many planted defects remained unresolved in the measured runs.; Run variance and harness differences prevent fine-grained cross-model ranking.

Supporting sources: [Bug Hunt Bench frozen measurements](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/data/benchmark.json) · [Bug Hunt Bench receipts and boundaries](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/README.md) · [Bug Hunt Bench individual configuration caveats](https://github.com/phuryn/bug-hunt-bench/blob/1217192a6d04e89da3f6106ca3a304d2734882eb/results/run-notes.md)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Result measures finding AND implementing fixes; do not relabel it as code-review recall or test-generation quality.; No matched independent contradiction located; partial successes and misses coexist.; Research provenance: history/research/2026-10-07/coding-input.json :: scoped_debugging:kimi-k3-debug-bughunt; Confidence concerns this bounded claim, not a capability score.

### Coding.debugging (low confidence)

Evidence supports some issue-directed Odin repairs under a fixed, patch-only protocol.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-8402332de3c5429b

Conditions: 168eligible public Odin issues; supplied source scope; one scored patch; no execution feedback to generator.; Exact request budget/API run date not independently audited.

Failure modes / limitations: A patch applying or reproducing an issue does not ensure complete repair.

Supporting sources: [OdinEval program repair](https://arxiv.org/html/2608.18595v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Preprint; check released manifest before stronger confidence. No universal language or harness transfer.; Research provenance: history/research/2026-10-07/coding-input.json :: scoped_debugging:kimi-k3-debug-odin; Confidence concerns this bounded claim, not a capability score.

### Coding.architecture (low confidence)

Hosted Kimi K3 produced useful integration/lifecycle design, but unsupported assumptions required factual correction.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.architecture

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-31ebdfe3ee9bd0f7

Conditions: Two frozen projects, 269 files; OpenCode 1.17.13, max effort, 60 minute limit,65,536 completion cap; read-only, no web/plugins/subagents.

Failure modes / limitations: Seven unsupported claim groups; incomplete revision authority/merge/storage rules and replay metadata.

Supporting sources: [Qwen 3.8 Max Benchmark: How It Compares With Kimi K3](https://trilogyai.substack.com/p/qwen-38-max-benchmark-how-it-compares)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: One run, unpublished full score artifacts; serving effects not isolated. qwen3.8-max-preview comparator cannot transfer to qwen3-8-2-4t-a95b weights.; Research provenance: history/research/2026-10-07/coding-input.json :: architecture_refactoring:A06; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-3bf0eb4fca39134c

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Research provenance: history/research/2026-10-07/coding-input.json :: review_tests_frontend:frontend-arena-kimi-k3; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Credible one-shot UI candidate, with dated visual-comparison support and current preference evidence.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-1d36ed42dd3a5b03

Conditions: Single HTML prototypes; launch-week endpoint conditions are not current service guarantees.; Named release matches; preserve source-specific provider, snapshot and precision limitations.

Failure modes / limitations: Calendar overlap and checkout polish trailed the tested older comparator.

Supporting sources: [Kimi K3 versus Claude Fable 5 on ten UIs](https://blog.kilo.ai/p/kimi-k3) · [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Research provenance: history/research/2026-10-07/coding-input.json :: review_tests_frontend:frontend-kimi-practitioner; Confidence concerns this bounded claim, not a capability score.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | MoE with Kimi Delta Attention, gated MLA, Attention Residuals, Stable LatentMoE; MoonViT-V2 vision encoder |
| parameters | total billion: 2800; active billion: 104; scope: creator-declared count; see notes; exact parameter count: Unknown / not established; components billion: vision encoder: 0.401 |
| context window | native tokens: 1048576; extended tokens: Unknown / not established; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; video; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

6 recorded access route(s); 3 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Kimi K3 License

Restrictions: Retain notices.; MaaS business above $20M aggregate trailing-12-month revenue requires agreement.; UI branding above 100M MAU or $20M monthly revenue.; Internal-only use and official products/certified inference partners exempt from preceding commercial/branding conditions.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: conditional

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Datacenter scale: native MXFP4 weights alone roughly 1.4TB plus quantization/runtime/cache; multi-node high-memory deployment.; Quantization-aware trained MXFP4 weights / MXFP8 activations; do not substitute a 104B-active memory estimate.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| fireworks | Standard / current | input: 3 USD / per 1M tokens; cached_input: 0.3 USD / per 1M tokens; output: 15 USD / per 1M tokens | Not established in this pass | 2026-10-06 |
| fireworks | Priority / current | input: 3.75 USD / per 1M tokens; cached_input: 0.375 USD / per 1M tokens; output: 18.75 USD / per 1M tokens | Not established in this pass | 2026-10-06 |
| together | standard displayed serverless / current | input: 2.7 USD / per 1M tokens; cached_input: 0.27 USD / per 1M tokens; output: 13.5 USD / per 1M tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- together / hosted metered api: documented_not_execution_tested. Not established in this pass
- kimi-api / Kimi consumer app/Work: documented_not_execution_tested. Not established in this pass
- kimi-api / hosted metered api: documented_not_execution_tested. Not established in this pass
- kimi-api / Kimi Code: documented_not_execution_tested. Not established in this pass
- kimi-api / hosted_api: documented route; account eligibility unverified. Not established in this pass
- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Moonshot AI

## Sources

[Kimi K3 License](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE) · [Kimi K3 model card](https://huggingface.co/moonshotai/Kimi-K3) · [Kimi K3 max independently profiled](https://artificialanalysis.ai/models/kimi-k3)
