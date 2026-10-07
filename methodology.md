# Methodology

## Decision unit

The unit of a useful conclusion is **model or variant × task × operating conditions × access route × evidence date**. A creator is not necessarily an inference provider. A client such as an IDE or CLI may expose several providers, accounts, and billing methods.

## Evidence types

- **Primary**: official model cards, technical reports, API references, pricing, licenses, and release/lifecycle notices. Appropriate for what is documented; vendor capability claims still require qualification.
- **Independent evaluation**: credible organizations or researchers with an identifiable task set, methodology, date, and configuration. Different harnesses and effort budgets are not interchangeable.
- **Practitioner**: attributable issues, discussions, deployment reports, technical blogs, and community experiences. Useful for hypotheses and failure modes; selection bias, prompting, provider variability, and unreported configuration limit generalization.

Source records preserve URL, title/description when known, publisher/type, publication date when known, access date, and limitations. Verification means the source was inspected; it does not mean every claim made by the source is objectively true.

## Confidence

- **High**: multiple credible, reasonably recent sources converge on the specific conclusion, with little material contradictory evidence.
- **Medium**: useful evidence, but incomplete, configuration-specific, or meaningfully mixed.
- **Low**: sparse, preliminary, old, vendor-heavy, benchmark-dependent, or contradictory evidence.

These labels attach to individual task judgments, not the model as a whole. A documented specification may be reliable while practical capability remains uncertain. Initial profiles can contain few judgments rather than pretending all task categories have been evaluated.

## How to judge capabilities

Use the [task rubric](data/tasks.md) to determine whether the evidence concerns
the selected task. Each definition supplies inclusion rules, boundary exclusions,
examples and neighboring tasks. A task boundary is not a model exclusion: exclude
a model only with positive mismatch evidence. Applicable tasks need a bounded
assessment; investigated uncertainty remains explicit.

New batches use the [bounded contract](docs/bounded-research.md) and separate
local bounded-run accounting. Completion is derived from required
field checks, task decisions and source-category checks against a pinned baseline.
Earlier four-domain coverage does not establish completion under this contract.

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
