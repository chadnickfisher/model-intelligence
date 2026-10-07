# Contributing

Submit focused public-evidence changes. Identify the model checkpoint or alias, provider, task, configuration, source, and dates. Include conflicting evidence and limitations. Prefer exact documented values to inferred ones; use null for unknowns.

Never include private conversations, personal account limits, secrets, proprietary prompts, or data without publication rights. Do not copy entire articles, benchmarks, or licensed model cards. Paraphrase relevant findings and cite sources.

Edit canonical YAML, run validation and generation, and inspect the diff. Explain whether the change is factual, a judgment revision, or a correction. Do not interpret test success as proof of model capability. Keep research logs concise and material changes in the dated changelog.
## Contribution license and migration rules

Research packages use the permanent four-domain contract in
[methodology.md](methodology.md): account for every catalog model's capabilities,
benchmarks/confidence rationale, access/pricing/limits and post-launch behavior.
Update the [coverage ledger](data/research-coverage.yaml) with actual source/search
checks, dates, results and remaining gaps. Focused corrections may leave other
domains explicitly not checked; do not represent them as complete research passes.
Carry-forward facts retain their verification dates. Record failed checks and
unknowns explicitly. Automated validation checks accounting, not research adequacy.


By submitting original dataset or documentation contributions, you agree to
license them under CC BY 4.0; original software contributions use MIT. Submit only
material you have permission to contribute. Preserve third-party notices and
source provenance; these licenses do not relicense upstream models or evidence.
See [LICENSE.md](LICENSE.md) and [NOTICE.md](NOTICE.md).

Use the curated task registry. New task IDs require an explicit reviewed registry
edit; the renderer never registers labels. Keep broad evidence as a compound or
unresolved judgment, with related task IDs for navigation only. Retain stable
judgment IDs, warnings, unknowns and contradictory evidence. Do not equate
confidence with capability strength. Record canonical changes with the
[compact change workflow](docs/change-tracking.md) before regenerating and validating views.
