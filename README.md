# Model Intelligence

A vendor-neutral, evidence-backed guide to AI models, their access routes, costs, and conditional strengths and weaknesses.

**[Open the interactive Model Intelligence explorer](https://model-intelligence-9fqyzge2aqwzqx93aqbkn5.streamlit.app/)**

**Research → Judge → Record → Maintain.**

This is a public-evidence knowledge base, not a universal leaderboard. It does not run paid inference or coding-agent benchmarks. A model can be useful for one workload and unsuitable for another; provider, effort, harness, quantization, context size, and price tier can change the conclusion.

Initial snapshot: **53 model profiles**, **39 provider/client/access-product profiles**, **122 pricing records**, **140 access routes**, and **225 public sources**, checked on **2026-10-06**. Counts indicate coverage, not completeness or equal evidence strength.

## Start here

- [Model catalog](data/models.md): current coverage and links to profiles
- [Provider catalog](data/providers.md): creators, hosts, gateways, and access products
- [Capability index](data/capabilities.yaml): complete judgments, direct/related scope, evidence, conditions and confidence; [curated tasks](data/capability-taxonomy.yaml)
- [Pricing](data/pricing.md): dated offers, units, conditions, and provenance
- [Access](data/access.md): subscription, API, download, local, and other routes
- [Releases](data/releases.yaml) and [change history](changelog/2026-10.md)
- [Methodology](methodology.md), [coverage gaps](research/coverage.md), and [maintenance plan](MAINTENANCE.md)
- For agents: [AGENTS.md](AGENTS.md) and [repo-map.yaml](repo-map.yaml)
- [Explicit observation history](history/README.md): preserved values and evidence; no invented earlier state

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
requirements, validates canonical records and history, regenerates derived
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
Compare 2-5 Models, Capability Explorer, Cost Explorer, and Recent Changes. The
Field Guide uses task-first search, readable cards, aligned comparisons, evidence
expanders and coverage counts. Confidence belongs to individual findings, not a
model score. Missing access research is “not yet documented,” never a false
unavailability claim. Source and canonical GitHub links accompany the records.
All facts retain their verification dates; the app does not refresh external data.

Recorded benchmark highlights appear on cards and in aligned comparison rows.
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
Pending work remains explicitly not checked. Validation checks ledger consistency,
not the adequacy of source research. Research maintenance remains paused.

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

Research maintenance is **PAUSED as of 2026-10-06**. No daily research is scheduled or promised. The manually supplied October 7 research update retains actual source inspection dates; carry-forward facts retain their earlier verification dates. Repository observation dates do not imply fresh fact verification.

The migration preserves 64 original capability records: 19 direct mappings, 34 compound bundles, 5 unresolved scope reviews and 6 relocated performance/deployment observations. Seven existing performance observations are also preserved. October 7 research adds 84 bounded direct judgments, for 142 complete capability claims and 13 performance observations. Confidence measures evidence support, not ability. A compound claim is never split into per-task endorsements; related tasks are navigation only. Warnings and missing evidence remain visible.

The update includes 53 access audits, 176 new route observations, 68 structured benchmark measurements and 86 post-launch behavior records. Three identity-gated capability candidates remain archived without direct enrollment. All 53 models have four-domain coverage accounting; 52 capability/benchmark domain checks remain explicitly pending. Conditional tariffs and non-token units are preserved as route details when estimation is unsupported. See the [research integration report](research/2026-10-07-integration.md).

For manual research handoffs, use the [project importer and publisher](docs/package-workflow.md) and the [project update skill](.agents/skills/model-intelligence-update/SKILL.md). The helper defaults to dry run, separates raw research from reviewed data updates, and restricts repository, base commit and intended paths. It does not schedule work or repair unavailable download permissions.
