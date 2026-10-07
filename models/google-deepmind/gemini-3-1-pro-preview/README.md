# Gemini 3.1 Pro Preview

**Creator:** Google DeepMind · **Family:** Gemini · **Status:** preview
**Verified:** 2026-10-06 · **Release:** 2026-02-19

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Difficult science visual qa and long documents (medium confidence)

Strong QA candidate; selectively retrieve evidence rather than fill the entire context indiscriminately.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): reasoning.scientific; vision.question_answering; context.reasoning

Judgment ID: judgment-6272f2a3a37dd45c

Conditions: high; temperature 1; Google API; output 65,536; high; Google API

Failure modes / limitations: Not established in this pass

Supporting sources: [Vals AI gemini-3.1-pro-preview](https://www.vals.ai/models/google_gemini-3.1-pro-preview)

Contradictory or limiting sources: [Gemini 3.1 Pro model card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [Vals AI gemini-3.1-pro-preview](https://www.vals.ai/models/google_gemini-3.1-pro-preview)

Evidence notes: task-conditioned synthesis; no inference runs performed; Observation obs-2ee68e334fde: Strong closed-form science and multimodal QA in current Vals snapshot.; Observation obs-dc03c35a1b80: Effective long-context retrieval degrades near the advertised maximum.; Observation obs-e8f1075592de: Strong QA does not transfer uniformly to open-ended agents.

### Coding.architecture (low confidence)

Budgeted architectural reconstruction showed incomplete dependency coverage; require independent map/constraint checks.

Scope: direct / warning. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.architecture

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-a2765fe12608a3e5

Conditions: Three procedurally generated Python pipeline codebases; one run each, 20-action budget, JSON belief probes every three actions; temperature 0. Tests architectural reconstruction, not greenfield design.

Failure modes / limitations: Sparse exploration limited recall. All models scored zero on invariant matching; structured externalization confounds comprehension.

Supporting sources: [Theory of Code Space: Do Code Agents Understand Software Architecture?](https://arxiv.org/html/2603.00601v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Preliminary small synthetic corpus; no variance estimate. Authors attribute the Gemini result mainly to exploration, not inability to understand code.; Confidence concerns this bounded claim, not a capability score.

### Coding.refactoring (medium confidence)

Can reduce targeted Java smells in a guided workflow; API preservation needs separate validation.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.refactoring

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-1d266c9e048c900c

Conditions: REFINE static-analysis/planning/transformation/verification workflow, PMD 7.10.0, Java 17; file-only context, no dependencies/tests/build configuration; 160k estimated input preflight cap.

Failure modes / limitations: Deletion-heavy outputs; 71 public-method-removal cases. Critical assert/fail preservation only 57.1%, shared across all evaluated models.

Supporting sources: [REFINE: A Multi-Agent LLM Approach for Evidence-Guided Code Refactoring](https://arxiv.org/html/2608.23611v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Static proxies do not prove executable equivalence. Broader quality metrics inconsistent; generated candidates were not integrated into repositories. Exact reasoning/sampling settings not established.; Confidence concerns this bounded claim, not a capability score.

### Coding.frontend (medium confidence)

Use relative preference evidence to shortlist this exact configuration for frontend trials; do not infer tests or review strength.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-56301dccb85b54ac

Conditions: Frontend generation under hosted Arena configurations; Relative user-preference evidence only; production acceptance requires executable behavior, accessibility, security and maintenance checks.; Reported model/version and effort retained in arena_rows. Public model labels are not immutable provider checkpoint hashes.; exact_named_release_effort_retained

Failure modes / limitations: Not established in this pass

Supporting sources: [Code Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend) · [Arena FAQ](https://arena.ai/faq)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

### Coding.review (medium confidence)

Strong result on compact Java refactoring defect identification, bounded to the April API snapshot.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.review

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-04629f12518519a6

Conditions: Default API; behavior-change findings require executable witnesses.; Named release matches; preserve source-specific provider, snapshot and precision limitations.

Failure modes / limitations: One generated witness failed to compile; main dataset lacks clean negatives.

Supporting sources: [Foundation Models as Oracles for Refactoring Correctness Detection](https://arxiv.org/html/2605.02096v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

### Coding.tests (medium confidence)

Useful for focused executable distinguishing tests on tiny Java changes.

Scope: direct / conditional. Task-specific source claim under documented conditions; no transfer to other coding tasks.

Direct task IDs: coding.tests

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-05030fb3bfa6c2e7

Conditions: April API snapshot; 41 behavioral-change examples.; Named release matches; preserve source-specific provider, snapshot and precision limitations.

Failure modes / limitations: Not evidence of complete repository regression coverage.

Supporting sources: [Foundation Models as Oracles for Refactoring Correctness Detection](https://arxiv.org/html/2605.02096v1)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Confidence concerns this bounded claim, not a capability score.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Gemini 3 Pro-derived sparse mixture-of-experts transformer; exact 3.1 modifications undisclosed |
| parameters | Unknown / not established |
| context window | 1048576 |
| maximum output | 65536 |
| modalities | input: text; image; video; audio; PDF; output: text |
| language support | Unknown / not established |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

9 recorded access route(s); 2 model-specific price record(s).

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

- Parameter counts
- Complete language list
- Exact 3.1-specific knowledge cutoff

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| google-developer-api | paid_standard / current | input: 2 USD / per_1M_tokens; output_including_thinking: 12 USD / per_1M_tokens; cache_read: 0.2 USD / per_1M_tokens | prompt <= 200,000 tokens | 2026-10-06 |
| google-developer-api | paid_standard / current | input: 4 USD / per_1M_tokens; output_including_thinking: 18 USD / per_1M_tokens; cache_read: 0.4 USD / per_1M_tokens | prompt > 200,000 tokens | 2026-10-06 |

## Recorded access routes

- google-developer-api / Gemini Developer API / Google AI Studio: officially_documented_not_execution_tested. Not established in this pass
- google-ai / Gemini app / NotebookLM: Conditional consumer/client product; exact account entitlement unverified. 3.1 Pro rollout documented in app with higher Pro/Ultra limits; NotebookLM launch exclusive to Pro/Ultra. Current app help uses Pro family label, not preview API alias. API has no free tier.
- google-cloud / Gemini Enterprise Agent Platform: official_preview. Not established in this pass
- google-ai / Gemini CLI / Antigravity / Android Studio: Conditional consumer/client product; exact account entitlement unverified. Launch explicitly names these clients. Authentication, plan allowances and exact live defaults must be separated from paid API tariff.
- google-developer-api / first-party-api: documented route; account eligibility unverified. Not established in this pass
- google-ai-studio / Google AI Studio: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass
- google-antigravity / Google Antigravity: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass
- google-cli / Gemini CLI: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass
- google-consumer / Gemini app / Google AI plans: Distribution documented; exact model selector, rollout, regional and subscription entitlement may vary.. Not established in this pass

## Sources

[Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Gemini 3.1 Pro Preview API model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview) · [Gemini API release notes](https://ai.google.dev/gemini-api/docs/changelog) · [Gemini 3.1 Pro model card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [Gemini 3 Pro base model card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf)
