# Claude Fable 5.1

**Creator:** Anthropic · **Family:** Claude 5 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-01

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Long horizon reasoning and coding (medium confidence)

Escalation candidate with strong evidence but expensive effort-sensitive operation.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): agent.long_horizon; reasoning.general; coding.repository_work

Judgment ID: judgment-7416a8c0468f622a

Conditions: Evaluated service includes safety fallback to other Claude models.

Failure modes / limitations: Cited GDP.pdf all-pass result is26%; failed cases are not categorized in the retrieved comparison.

Supporting sources: [Fable5.1 versus Fable5 benchmark comparison](https://artificialanalysis.ai/models/comparisons/claude-fable-5-1-vs-claude-fable-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: AA max/default fallback: Terminal-Bench4.0 52%, HLE59%, AA-LCR85%; all improve over Fable5 except some nearly flat tasks.; contradictory evidence: GDP.pdf only26%; these results do not make Fable universally preferable to newer Opus/Sonnet.; Observation obs-8614ee721f1d: Escalation candidate with strong evidence but expensive effort-sensitive operation.; Potential risk (not a measured failure): Fallback changes model provenance; errors persist on document reasoning.

### Cache heavy agents (medium confidence)

Cache price cut can help context-heavy workflows, but task cost is workload-dependent.

Scope: performance / conditional. Cost, deployment or throughput observation; not a task capability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-b82fd561ee151f9f

Conditions: Vendor default-effort August traffic and AA max benchmark are different workloads, not directly contradictory arithmetic.

Failure modes / limitations: AA reports higher benchmark task cost despite lower cached-token rates.

Supporting sources: [Introducing Claude Fable 5.1 and Mythos 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1) · [Fable 5.1 launch measurement](https://artificialanalysis.ai/zh/articles/claude-fable-5-1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Conservative baseline confidence: broader convergence has not been independently audited.; supporting evidence: Vendor reports25% typical and up to45% highly agentic savings versus Fable5.; contradictory evidence: AA launch measurement reports20% higher cost/task despite cheaper cache reads.; Observation obs-c5fa019c8d8a: Cache price cut can help context-heavy workflows, but task cost is workload-dependent.; Potential risk (not a measured failure): Longer reasoning can erase cache savings.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 1000000 |
| maximum output | 128000 |
| modalities | input: text; image; output: text |
| language support | Multilingual; exact inventory not specified |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

7 recorded access route(s); 2 model-specific price record(s).

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
| anthropic | Standard / current | input: 10 USD / per 1 million tokens; output: 50 USD / per 1 million tokens; cached_input: 0.25 USD / per 1 million tokens; cache_write_5m: 12.5 USD / per 1 million tokens; cache_write_1h: 20 USD / per 1 million tokens | Not established in this pass | 2026-10-06 |
| anthropic | Batch / current | input: 5.0 USD / per 1 million tokens; output: 25.0 USD / per 1 million tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- anthropic / Claude API: Active. quota: Tier/account-specific; exact numeric public tier table not captured
- aws-bedrock / Amazon Bedrock: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- google-cloud / Google Cloud: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- azure-foundry / Microsoft Foundry / Azure: Listed by creator; independent provider pricing and regional entitlement not verified. Not established in this pass
- anthropic / Claude Code terminal: All paid Claude plans include Code; API-credit billing is a separate option. quota: Shared with web/desktop/mobile plan pool; IDE entitlement details not separately verified
- anthropic / Claude Code IDE integrations: documented route; account eligibility unverified. Not established in this pass
- anthropic / Claude apps: Pro uses usage credits; Max has Fable access within50% of weekly limits. quota: Not equivalent to unlimited subscription access

## Sources

[Claude fable-5-1 specifications](https://platform.claude.com/docs/en/models/fable-5-1/overview) · [Claude current model overview](https://platform.claude.com/docs/en/models/overview) · [Fable5.1 versus Fable5 benchmark comparison](https://artificialanalysis.ai/models/comparisons/claude-fable-5-1-vs-claude-fable-5) · [Introducing Claude Fable 5.1 and Mythos 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1) · [Fable 5.1 launch measurement](https://artificialanalysis.ai/zh/articles/claude-fable-5-1)
