# Methodology

## Decision unit

The unit of a useful conclusion is **model or variant × task × operating conditions × access route × evidence date**. A creator is not necessarily an inference provider. A client such as an IDE or CLI may expose several providers, accounts, and billing methods.

## Evidence types

- **Primary**: official model cards, technical reports, API references, pricing, licenses, and release/lifecycle notices. Appropriate for what is documented; vendor capability claims still require qualification.
- **Independent evaluation**: credible organizations or researchers with an identifiable task set, methodology, date, and configuration. Different harnesses and effort budgets are not interchangeable.
- **Practitioner**: attributable issues, discussions, deployment reports, technical blogs, and community experiences. Useful for hypotheses and failure modes; selection bias, prompting, provider variability, and unreported configuration limit generalization.

Source records preserve URL, title/description when known, publisher/type, publication date when known, access date, and limitations. Verification means the source was inspected; it does not mean every claim made by the source is objectively true.

## Task suitability policy v1

Assess each existing task in [`data/capability-taxonomy.yaml`](data/capability-taxonomy.yaml)
independently for each model or variant. An aggregate assessment concerns that
specific model/task pair under its stated operating conditions and access route.
Compare performance with the task's requirements, not a competitor's rank or an
average of benchmark scores. A finding about another task does not transfer.

| Suitability | Meaning |
| --- | --- |
| High | Handles the core task requirements well under the stated conditions; ordinary review is sufficient. |
| Medium | Produces useful results, with material checking, correction or workarounds required. |
| Low | Misses core requirements enough to undermine usefulness on a supported task. |
| Not supported | Documented capabilities rule out the task in the assessed model/setup. |
| Disputed | Credible evidence supports materially different suitability conclusions, with no single aggregate rating justified. |
| Unknown | Investigation has not established enough evidence to judge suitability. |

Explicit task requirements remain binding: ordinary review cannot excuse failing
a requirement for autonomous operation. Not supported needs positive evidence of
the capability boundary. Missing research or benchmarks do not establish
non-support or Low suitability. Distinguish native model capabilities from an
external tool workflow and preserve provider/setup limitations. An unassessed
model/task pair is distinct from an investigated Unknown.

An aggregate assessment explains its rating, conditions, relevant direct findings,
supporting and contrary evidence, actual source inspection dates and remaining
gaps. Task fit explains why the rating applies; Watch-outs retains material
limitations and disagreements, including in compact presentations. Compound or
unresolved findings linked through `related_task_ids` provide navigation and do
not establish a direct task endorsement. Legacy finding labels are not automatic
aggregate suitability assignments.

Task results include High, Medium, Low and Disputed by default,
with each selectable. Not supported is an optional filter, off by default.
Unknown and unassessed pairs are omitted from selected-task results for now;
direct model lookup retains their evidence and gaps. A result's presence does not
imply a positive recommendation. The application and future MCP layer use the
same canonical assessments and task IDs. The application selects only explicitly
curated aggregates; older findings remain available through model lookup and
evidence navigation while the remaining assessments are curated.

Task-result cards retain the model's access routes and API/subscription status,
provider-qualified prices with billing units and conditions, context, benchmark
highlights and dated post-launch observations alongside the task assessment.
Full specifications, licensing, local hardware and source evidence remain
available in the existing details view. Task suitability does not replace this
information or combine it into a universal model score.

## Evidence confidence

Evidence confidence describes the strength of evidence supporting a specific
bounded judgment. It is separate from suitability, source prestige and benchmark
score. High suitability with Low confidence and Low suitability with High
confidence are both valid. High, Medium, Low and Not supported assessments carry
an evidence-confidence label:

- **High**: strong evidence supports the specific conclusion, with relevant
  identity, setup, method, dates and contradictions addressed. Task-performance
  judgments require more than one independent evidence stream supporting the same
  bounded conclusion; independence alone is insufficient. Clear authoritative
  documentation for the exact model/setup can establish a capability boundary
  with High confidence without an independent performance evaluation.
- **Medium**: useful, relevant evidence supports the conclusion, with material
  methodological or generalization limits. Detailed, independently corroborated
  practitioner evidence can qualify within its documented conditions.
- **Low**: evidence is sparse, preliminary, vendor-heavy or limited by unclear
  identity, setup, methods or unresolved evidential weaknesses. An isolated
  anecdote remains Low and narrowly attributed.

Vendor-only evaluations may support a suitability assessment when they concern
the exact model and task with a documented setup; retain vendor attribution and
Low performance confidence. Unsupported marketing is insufficient. Copied reports
do not count as independent corroboration. Confidence in a documented modality
or specification does not transfer to task-quality claims.

Disputed has no aggregate confidence badge because there is no single justified
aggregate conclusion. Its underlying findings retain their evidence confidence.
When Disputed is selected, it remains in task results through an active evidence-
confidence filter. Explain that confidence belongs to its underlying findings;
its presence does not mean it satisfies a requested aggregate confidence level.
Excluding Disputed through the suitability filter still removes it.
Assess conflicts before choosing a rating: compare claim identity, task, setup,
methods, dates and limitations. A documented reason may justify one conclusion;
unresolved material divergence remains Disputed. Relevant setup differences can
justify a disputed aggregate even when each conditional finding is valid. Explain
the divergence and retain contrary evidence after resolution. Recency or publisher
prestige alone does not settle disagreement.

Evidence age triggers review rather than an automatic confidence downgrade.
Inspect relevant sources before refreshing factual verification dates. Initial
profiles can contain few judgments rather than pretending every task was assessed.

## How to judge capabilities

Use the [task rubric](data/tasks.md) to determine whether the evidence concerns
the selected task. Each definition supplies inclusion rules, boundary exclusions,
examples and neighboring tasks. A task boundary is not a model exclusion: exclude
a model only with positive mismatch evidence. Applicable tasks need a bounded
assessment; investigated uncertainty remains explicit.

Coverage accounting records what was investigated and what remains unknown.
Accounting completion cannot establish that research was adequate or that a
conclusion is correct. Assess each claim against its cited evidence.

State a concrete task and a bounded conclusion. Include sources, important conditions, observed or credibly reported failure modes, and contradictory evidence. Distinguish observations from inference and recommendations. Example: strong scoped-edit performance in a tool-enabled benchmark does not establish reliable architecture decisions or multi-hour autonomous stability.

Do not average incompatible evaluations into a single score. Consider contamination, task selection, benchmark saturation, scoring sensitivity, model snapshots, tool access, context length, reasoning budget, quantization, and provider implementation. Model comparisons require matched conditions or explicit caveats.

“No contradiction located” is a search limitation. It is not consensus. An isolated anecdote can be recorded as a low-confidence warning, with narrow attribution; it cannot establish a general failure rate.

## Costs

Represent each offer separately with provider/product/model, billing method, currency, unit, region, tier, effective date when known, verification date, and sources. Separate input, output, cached reads/writes, batch, reasoning, image/audio/video, tool charges, credits, subscriptions, and overages. Preserve conditional tiers and thresholds. Null prices are not free. Subscription prices without stable public quotas cannot be converted into per-task costs reliably.

Token prices do not establish task cost. Reasoning output, retries, tool calls, context reuse, service tiers, and useful-result rate can dominate. Local hardware estimates are planning estimates tied to precision, context, concurrency, and offload; parameter count alone is insufficient. Do not confuse total MoE parameters with active compute parameters or weight-memory requirements.

## Access and licensing

Record first-party products and third-party routes independently. Availability in a catalog does not prove an individual account has access. Preserve preview, waitlist, enterprise, region, acceptable-use, quota, and reset restrictions. Do not assert unlimited usage from marketing language without the applicable policy.

Use “open weights” for downloadable parameters unless the broader open-source claim is specifically justified. Preserve model-specific license terms and exceptions; never assume a family shares one license. License summaries are navigational aids, not legal advice.

## Freshness and changes

Every research update accounts for **every catalog model** across four permanent
domains: task-specific capabilities, benchmarks and confidence rationale,
verified access/pricing/limits, and post-launch behavior. This scope applies to
each research package, not just an initial backfill. Record the pass in
[`data/research-coverage.yaml`](data/research-coverage.yaml), with one entry per
model/domain, actual source or search references, actual check date, result,
scope and remaining gaps. Results are changed, unchanged, unknown, blocked, or
explicitly not checked. A structural inventory is not a completed source audit.
Unchecked domains have null check dates; blocked checks identify their blocker.
No source found or no report located is unknown, not unavailable or weak.

Retain existing verification timestamps on carry-forward facts. Change a source
access date or factual verification date only after actually inspecting the
relevant source. A newly added judgment can have today's observation date while
its measured/effective date is older or unknown. Record official and attributable
practitioner behavior separately, preserving configuration, contradictions and
fix history. A published fix does not establish measured recovery.

Benchmark records in [`data/benchmarks.yaml`](data/benchmarks.yaml) retain test
name/version, metric/unit/direction, exact checkpoint, harness/effort/tools/provider,
measurement and observation dates, source class and limitations. Keep independent
quality tests, preference rankings and vendor claims distinct. Missing measurements
stay unknown. Shared names with incompatible or missing configurations do not
establish comparable results. High scores do not establish high confidence;
confidence rationales trace the relevant evidence, corroboration, freshness,
conditions and contradictions for each judgment.

Validation enforces coverage accounting, dates and references. It cannot prove
that source investigation was adequate or that a conclusion is true. Publication
reports must distinguish actual checks from unchanged carry-forward data and list
unresolved gaps. The coverage ledger does not enable a recurring schedule.

Every record carries an access/verification date. Pricing, availability, and lifecycle are high-volatility; capability evidence ages by task and model change. Suggested review windows are 7 days for price/access/status, 30 days for capability synthesis, and 90 days for unchanged checkpoint licenses. These are review targets, not claims that a scheduler is running.

Material changes include releases, retirements, price or entitlement changes, altered licenses, reproducible regressions, and evidence that changes a recommendation. Tiny leaderboard movement, duplicated announcements, and isolated hype do not require a changelog entry. The initial baseline is not a history of events personally observed as they occurred.

## Limitations and corrections

The project uses public evidence and performs no paid or subscription-funded model benchmarking. Independent hands-on validation by users may later be contributed with configuration and reproducible evidence. Maintain disagreements and correction history. Research dates, release dates, effective dates, and repository commit dates are different fields.
