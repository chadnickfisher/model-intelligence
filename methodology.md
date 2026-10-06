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

Every record carries an access/verification date. Pricing, availability, and lifecycle are high-volatility; capability evidence ages by task and model change. Suggested review windows are 7 days for price/access/status, 30 days for capability synthesis, and 90 days for unchanged checkpoint licenses. These are review targets, not claims that a scheduler is running.

Material changes include releases, retirements, price or entitlement changes, altered licenses, reproducible regressions, and evidence that changes a recommendation. Tiny leaderboard movement, duplicated announcements, and isolated hype do not require a changelog entry. The initial baseline is not a history of events personally observed as they occurred.

## Limitations and corrections

The project uses public evidence and performs no paid or subscription-funded model benchmarking. Independent hands-on validation by users may later be contributed with configuration and reproducible evidence. Maintain disagreements and correction history. Research dates, release dates, effective dates, and repository commit dates are different fields.
