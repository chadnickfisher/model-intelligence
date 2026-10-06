# Future query contract

The future MCP layer reads canonical records and returns stable IDs, source references, verification dates, uncertainty, and applicable conditions. Implementation is deferred.

Queries: get_model(id), get_provider(id), compare_models(ids, task, conditions), find_models(task, minimum_confidence, modalities, local), list_access(model_id), compare_prices(model_id, region, billing_method, unit), recent_releases(since), recent_changes(since), and stale_records(as_of).

Price-threshold queries must require a billing unit and route. Never compare $/month to $/million tokens. A request for local models must distinguish downloadable weights, license compatibility, required precision/memory/context, and runtime compatibility. Capability queries return evidence-backed judgments, not invented scalar ranks. Unknown is a first-class result, not a negative match.

Reject ambiguous model aliases when materially different variants exist. Preserve separate prices/availability for hosts of the same model. Return evidence disagreements and freshness rather than hiding them in a synthesized recommendation.
