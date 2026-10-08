# Model Intelligence

A vendor-neutral, evidence-backed guide to AI models, their access routes, costs, and conditional strengths and weaknesses.

**[Open the interactive Model Intelligence explorer](https://model-intelligence-9fqyzge2aqwzqx93aqbkn5.streamlit.app/)**

**Research → Judge → Record → Maintain.**

This is a public-evidence knowledge base, not a universal leaderboard. It does not run paid inference or coding-agent benchmarks. A model can be useful for one workload and unsuitable for another; provider, effort, harness, quantization, context size, and price tier can change the conclusion.

Current counts are in the [generated inventory](data/coverage.yaml). Counts indicate coverage, not completeness or equal evidence strength; each fact retains its own inspection date.

## Start here

- [Model catalog](data/models.md): current coverage and links to profiles
- [Provider catalog](data/providers.md): creators, hosts, gateways, and access products
- [Capability index](data/capabilities.yaml): complete judgments, direct/related scope, evidence, conditions and confidence; [task rubric](data/tasks.md)
- [Pricing](data/pricing.md): dated offers, units, conditions, and provenance
- [Access](data/access.md): subscription, API, download, local, and other routes
- [Releases](data/releases.yaml) and [change history](changelog/2026-10.md)
- [Methodology](methodology.md) and [coverage gaps](research/coverage.md)
- [Repository map](repo-map.yaml): canonical records and query entry points
- [Current state and concise changes](docs/change-tracking.md): source-backed records, changelog and reproducible Git baselines
- [Current task assessments](data/task-assessments.yaml): applicability, evidence and uncertainty
- [Research schedule](docs/research-schedule.md): planned weekly groups and daily research tracks; recurring execution is paused

## What is canonical?

Structured YAML is authoritative. Per-model and per-provider README files are generated views. Indexes point to stable IDs; they do not create a second version of a model's specifications or judgments. Pricing and access records have their own identities because a model can have several providers and several commercial routes.

A missing value means **unknown or not established**, not zero, free, unlimited, unavailable, or unsupported. Read the conditions and verification date before using any price or capability judgment. `active` means a source describes the release as available; it does not guarantee access to a particular account or country.

## Coverage and limits

The initial baseline prioritizes materially relevant proprietary, open-weight, local, reasoning, coding, multimodal, and efficient models. It is deliberately incomplete. Profiles state which facts and judgments are well supported and which are provisional. Announced availability, published benchmark performance, and independently demonstrated real-world reliability are different evidence classes.

Provider listings and first-party prices can change independently. Commercial licensing and geographic availability need checking for a specific deployment. This project is research, not legal advice or a guarantee of service availability.

## Contributing

Use public sources only. Propose a small change with evidence, exact model/provider identity, conditions, and verification date. Preserve conflicting evidence. See [CONTRIBUTING.md](CONTRIBUTING.md). Do not submit secrets, private workloads, personal account quotas, or unconsented user data.

## Validation

Run `python tools/validate.py` to check schemas, IDs, references, and dated evidence. Run `python tools/render.py` to rebuild readable catalogs and profiles. These utilities validate and format local data only; they make no model calls or external network requests.

[GitHub Actions CI](.github/workflows/ci.yml) runs on every push and pull request
with Python 3.12 on an Ubuntu runner. It installs the runtime and development
requirements, validates canonical records and current checksums, regenerates derived
outputs, runs tests, and requires `git diff --exit-code` to pass. Unexpected
untracked files also fail the job. Commit regenerated outputs with the canonical
changes that caused them. CI uses read-only repository permissions and needs no
secrets or external services; research maintenance remains paused.

## Local interactive explorer

Use Python 3.12 (the tested runtime), from the repository root:

```sh
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py --browser.gatherUsageStats false
```

The explorer reads the same canonical YAML, with no database, copied app dataset,
credentials, model endpoints or inference charges. It provides Model Explorer,
Provider Explorer, Compare 2-5 Models, Capability Explorer, Cost Explorer, and Recent Changes. The
Field Guide uses task-first search, readable cards, visual comparisons, evidence
expanders and coverage counts. Confidence belongs to individual findings, not a
model score. Missing access research is “not yet documented,” never a false
unavailability claim. Source and canonical GitHub links accompany the records.
All facts retain their verification dates; the app does not refresh external data.

Cards show Task fit only after selecting a task, using that task's actual findings
and matching benchmark evidence. Watch-outs remain visible; missing documented
limits remain unknown. Access and price lists use bullets and distinct labels.
Observation summaries preserve complete sentences and limiting statements, with
full text and evidence in expanders; a published fix does not imply measured recovery.

The comparison grid shows task fit, evidence confidence, documented access and
provider-qualified costs for a shared text workload. Without a selected task,
counts include only explicit High/Medium task judgments; clicking a count reveals
those tasks and separate Low/Disputed findings. Confidence counts refer to the
included tasks, not a model-wide rating. Missing or incompatible prices remain
unestimated; cost option selection preserves billing conditions and exact routes.
Blocked request estimates still show published API rates and a readable reason.
Explicitly linked subscription plans and hosted compute retain their billing units
and usage conditions; local routes show variable compute cost. Only compatible USD
request estimates appear on the shared bar scale.

Recorded benchmark highlights appear on cards and in expandable comparison details.
Details retain metric/unit/direction, exact checkpoint, harness/effort/tools/provider,
dates, sources and limitations. Independent quality tests, preference rankings and
vendor claims remain distinct. Incompatible or incomplete setups are labeled;
missing results stay unknown. Each judgment exposes its evidence, freshness,
conditions, contradictions and recorded confidence rationale. A high benchmark
score does not establish high confidence or a universal model score.

Every research package accounts for all catalog models across capabilities,
benchmarks/confidence rationale, access/pricing/limits and post-launch behavior in
the [research coverage ledger](data/research-coverage.yaml). Actual check dates and
source/search references are separate from carry-forward verification dates.
Investigated unknowns and configuration gaps remain explicit. Validation checks record consistency, not the adequacy of source research. Research maintenance remains paused.

Cost Explorer estimates **text-token subtotals** only when an exact current price
record has an explicit matching model/provider API route. Total input includes
cached reads and cache writes; those are disjoint subsets, charged once. Output
includes billable thinking. Select the actual offer/tier; no automatic batch/flex
discount is applied. Documented context bands apply to the full request. Five-minute
and one-hour cache writes use separate rates. Peak/off-peak offers require UTC time
and holiday status where relevant. No currency exchange or subscription/token-price
conversion is made. Unknown rates, unsupported units/conditions and missing route
links explain why calculation is unavailable. Taxes, tools, storage, payment fees,
regional uplifts, retries and additional modalities are outside the subtotal.
The simple form accepts input/output tokens per run and a run count. Runs are
identical independent requests: each request is priced against its own context
band before multiplication. Cache reuse is never inferred. Only compatible offers
in the same currency and billing mode appear together; account credits and
subscriptions are displayed separately. Relevant cache and peak/off-peak settings
are available under request details.

Dated behavior findings live in `data/behavior.yaml`, with affected model/product/
harness, reporting and observation dates, support and contradictions, confidence,
and any official statement or published fix. Reports are distinguished from
acknowledged or measured changes. Published fixes do not establish measured
end-to-end improvement. `data/access-coverage.yaml` records research coverage and
remaining unknowns; it is not an inventory of guaranteed account entitlements.

Run the development checks after installing `requirements-dev.txt`:

```sh
python -m pip install -r requirements-dev.txt
python tools/validate.py
python tools/render.py
python -m pytest -q
```

## Hosted explorer and Community Cloud deployment

The [public explorer](https://model-intelligence-9fqyzge2aqwzqx93aqbkn5.streamlit.app/)
is hosted on Streamlit Community Cloud. The local setup instructions above remain
available. For deployment setup, follow the
[official Streamlit Community Cloud guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app):
choose this public repository, branch `main`, entrypoint `streamlit_app.py`, and
Python 3.12. Root `requirements.txt` supplies dependencies; no secrets or external
services are needed. The repository is self-contained. Verify that all five views
load after deployment changes. MCP remains a future query layer.

## Reuse and licensing

Original data and documentation use **CC BY 4.0**; original software uses **MIT**. See [license scope and full texts](LICENSE.md) and [attribution and third-party exclusions](NOTICE.md). Upstream model licenses remain attached to their respective models. Original research paraphrases sources and links to them rather than redistributing source documents or model weights.

Published records retain their own inspection and verification dates. The explorer does not automatically refresh external sources. Stable judgments preserve evidence, conditions, uncertainty and contradictory findings.

See the [research coverage ledger](data/research-coverage.yaml), [task assessments](data/task-assessments.yaml) and [material changes](changelog/changes.yaml). Coverage accounting does not certify research adequacy.

The public repository contains application code, curated public-source data, methodology, schemas and tests. Local agent instructions, working plans, handoffs and operator runbooks are excluded from the published product.
