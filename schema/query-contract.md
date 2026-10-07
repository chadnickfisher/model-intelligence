# Future query contract

The future MCP layer reads canonical records and returns stable IDs, source references, verification dates, uncertainty, and applicable conditions. Implementation is deferred.

Queries: get_model(id), get_provider(id), compare_models(ids, task, conditions), find_models(task, minimum_confidence, modalities, local), list_access(model_id), compare_prices(model_id, region, billing_method, unit), recent_releases(since), recent_changes(since), and stale_records(as_of).

Use `data/capability-taxonomy.yaml` for stable task IDs. A judgment has its own
stable ID and keeps its conclusion, confidence, assessment, conditions, support,
contradictions, failure modes and provenance. `task_ids` denotes direct scope;
`related_task_ids` is navigation for compound or unresolved evidence. Returning a
bundle for a related task must clearly retain its scope; never manufacture an
individual conclusion. Performance observations are not task endorsements.

Local history functions in `tools.knowledge` provide model/price entity history,
capability history, `snapshot(date)` (ecosystem knowledge observed by that date),
and `changes_between(start, end)`. See [history semantics](../history/README.md).
No values are reconstructed before the October 7 observation baseline. Preserve
documented effective dates within each value separately from observation dates.

Price-threshold queries must require a billing unit and route. Never compare $/month to $/million tokens. A request for local models must distinguish downloadable weights, license compatibility, required precision/memory/context, and runtime compatibility. Capability queries return evidence-backed judgments, not invented scalar ranks. Unknown is a first-class result, not a negative match.

Reject ambiguous model aliases when materially different variants exist. Preserve separate prices/availability for hosts of the same model. Return evidence disagreements and freshness rather than hiding them in a synthesized recommendation.
