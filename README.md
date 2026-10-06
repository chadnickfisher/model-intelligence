# Model Intelligence

A vendor-neutral, evidence-backed guide to AI models, their access routes, costs, and conditional strengths and weaknesses.

**Research → Judge → Record → Maintain.**

This is a public-evidence knowledge base, not a universal leaderboard. It does not run paid inference or coding-agent benchmarks. A model can be useful for one workload and unsuitable for another; provider, effort, harness, quantization, context size, and price tier can change the conclusion.

Initial snapshot: **53 model profiles**, **39 provider/client/access-product profiles**, **122 pricing records**, **140 access routes**, and **225 public sources**, checked on **2026-10-06**. Counts indicate coverage, not completeness or equal evidence strength.

## Start here

- [Model catalog](data/models.md): current coverage and links to profiles
- [Provider catalog](data/providers.md): creators, hosts, gateways, and access products
- [Capability index](data/capabilities.yaml): task-specific judgments and confidence
- [Pricing](data/pricing.md): dated offers, units, conditions, and provenance
- [Access](data/access.md): subscription, API, download, local, and other routes
- [Releases](data/releases.yaml) and [change history](changelog/2026-10.md)
- [Methodology](methodology.md), [coverage gaps](research/coverage.md), and [maintenance plan](MAINTENANCE.md)
- For agents: [AGENTS.md](AGENTS.md) and [repo-map.yaml](repo-map.yaml)

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

## Reuse and licensing

No project-wide redistribution license has been selected for this initial baseline. Public visibility alone is not an open-source license. Upstream model licenses remain attached to their respective models and are not changed by this repository. Original research paraphrases sources and links to them rather than redistributing source documents or model weights.
