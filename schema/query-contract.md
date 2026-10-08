# Future query contract

The future MCP layer reads canonical records and returns stable IDs, source references, verification dates, uncertainty, and applicable conditions. Implementation is deferred.

Queries: get_model(id), get_provider(id), compare_models(ids, task, conditions), find_models(task, suitability, minimum_confidence, modalities, local), list_access(model_id), compare_prices(model_id, region, billing_method, unit), recent_releases(since), recent_changes(since), and stale_records(as_of).

Use `data/capability-taxonomy.yaml` for stable task IDs. A judgment has its own
stable ID and keeps its conclusion, confidence, assessment, conditions, support,
contradictions, failure modes and provenance. `task_ids` denotes direct scope;
`related_task_ids` is navigation for compound or unresolved evidence. Returning a
bundle for a related task must clearly retain its scope; never manufacture an
individual conclusion. Performance observations are not task endorsements.

## Task-specific assessment queries

Task queries follow [task suitability policy v1](../methodology.md#task-suitability-policy-v1).
The application and future MCP query the same canonical assessments in
`data/task-assessments.yaml`. Resolve the exact model/variant and existing task ID;
for example, a debugging query requests `coding.debugging`, not general coding or
agent ability. Assess each dropdown task independently. Raw matching findings or
`related_task_ids` alone cannot admit a model to selected-task results.

The [task-assessment schema](task-assessment-record.schema.json) permits an explicit
`aggregate` with policy version `1`, suitability, evidence confidence and its
rationale, an assessment date, supporting/contrary evidence, conflict reasoning,
watch-outs and assessed access-route IDs. Parent conditions apply to the aggregate.
The source-check date (`checked_at`) remains distinct from the judgment date
(`aggregate.assessed_at`). An absent aggregate is not a rating and must not be
inferred from an older finding, assessment result or exclusion. Legacy records
remain readable while explicit aggregates are curated in bounded updates.

The suitability vocabulary is High, Medium, Low, Not supported, Disputed and
Unknown. With no explicit suitability selection, task results include High,
Medium, Low and Disputed. Each can be filtered out. Not supported is available
by explicit selection and off by default; it requires documented evidence of a
capability boundary for the assessed setup. Unknown and unassessed pairs remain
outside selected-task results for now. Direct model lookup preserves uncertainty,
evidence, warnings and gaps. Inclusion alone is not a positive recommendation.

Return the task's aggregate suitability, rating rationale, operating conditions,
applicable access route, direct supporting finding IDs, supporting and contrary
source references, actual inspection dates, limitations and gaps. Task fit and
Watch-outs explain the level and material caveats. Keep finding-level confidence
distinct from aggregate evidence confidence. High, Medium, Low and Not supported
carry aggregate evidence confidence and its reasoning. Disputed has no aggregate
confidence badge; return its unresolved divergence and the underlying findings'
confidence. An explicit evidence-confidence restriction retains Disputed results
when that suitability state is selected. Explain that confidence applies to the
underlying findings, not an aggregate conclusion; preserve material conflicting
evidence. A suitability selection excluding Disputed still removes those results.
Do not derive confidence from score, rank, copied source counts or
unrelated specification facts. Unknown is uncertainty, not demonstrated weakness;
unassessed work remains distinguishable in model lookup.

The shared selection helper is `tools.task_assessments.select_task_assessments`.
The application's selected-task search uses this helper through
`explorer.data.filter_models`. The MCP server remains deferred; its future
implementation must use the same selection semantics and canonical records.

Historical entity, capability and date-snapshot query APIs are outside scope.
Recent changes return concise summaries from the changelog. Git retains previous
versions; current records retain their original source, inspection and effective
dates. See [current state and changes](../docs/change-tracking.md).

Price-threshold queries must require a billing unit and route. Never compare $/month to $/million tokens. A request for local models must distinguish downloadable weights, license compatibility, required precision/memory/context, and runtime compatibility. Capability queries return evidence-backed judgments, not invented scalar ranks. Preserve Unknown explicitly in model lookup and assessment records; it is not a negative match.

Reject ambiguous model aliases when materially different variants exist. Preserve separate prices/availability for hosts of the same model. Return evidence disagreements and freshness rather than hiding them in a synthesized recommendation.
## Additional evidence queries

`data/access-coverage.yaml` records access research status separately from actual
routes. Missing API or subscription routes return unknown, not false. Explicit
unavailability requires negative evidence. Route billing, account eligibility,
included credits and subscription API entitlement remain separate facts.

`data/behavior.yaml` contains dated public behavior findings qualified by model
version, provider/product, harness/effort, metric, source, confidence and lifecycle.
Reported, acknowledged and measured changes are distinct; a published fix does
not establish measured recovery. TTFT, generation throughput and total agent time
are separate metrics. Relevant dated findings remain in current records; Git preserves previous versions.

New capability judgments use research provenance (`origin: research`, batch ID
and method). The migration provenance variant remains reserved for preserved
original records. Neither origin implies endorsement or a universal ability score.

`data/benchmarks.yaml` supports benchmark results by model or linked judgment.
Return test/version, metric/unit/direction, exact checkpoint, setup, dates,
sources, evidence class and limitations. Missing results remain unknown.
Comparison must expose incompatible or incomplete setups; shared benchmark names
do not permit universal scoring or aggregation of quality and preference results.

`data/research-coverage.yaml` accounts for each catalog model across capabilities,
benchmarks, access/pricing and behavior. Return actual check dates, result,
source/search references and remaining gaps. Pending checks have null dates;
source absence is unknown. Accounting validation does not certify research quality.
Both record types retain evidence and dates; previous versions are retained by Git.

Current task applicability and assessment conclusions are in data/task-assessments.yaml. Return their actual dates, rationale, direct judgment references and gaps. Missing assessment records remain unknown; local research/checklist files are outside the query layer.
