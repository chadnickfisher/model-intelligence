# Future query contract

The future MCP layer reads canonical records and returns stable IDs, source references, verification dates, uncertainty, and applicable conditions. Implementation is deferred.

Queries: get_model(id), get_provider(id), compare_models(ids, task, conditions), find_models(task, minimum_confidence, modalities, local), list_access(model_id), compare_prices(model_id, region, billing_method, unit), recent_releases(since), recent_changes(since), and stale_records(as_of).

Use `data/capability-taxonomy.yaml` for stable task IDs. A judgment has its own
stable ID and keeps its conclusion, confidence, assessment, conditions, support,
contradictions, failure modes and provenance. `task_ids` denotes direct scope;
`related_task_ids` is navigation for compound or unresolved evidence. Returning a
bundle for a related task must clearly retain its scope; never manufacture an
individual conclusion. Performance observations are not task endorsements.

Historical entity, capability and date-snapshot query APIs are outside scope.
Recent changes return concise summaries from the changelog. Git retains previous
versions; current records retain their original source, inspection and effective
dates. See [current state and changes](../docs/change-tracking.md).

Price-threshold queries must require a billing unit and route. Never compare $/month to $/million tokens. A request for local models must distinguish downloadable weights, license compatibility, required precision/memory/context, and runtime compatibility. Capability queries return evidence-backed judgments, not invented scalar ranks. Unknown is a first-class result, not a negative match.

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
