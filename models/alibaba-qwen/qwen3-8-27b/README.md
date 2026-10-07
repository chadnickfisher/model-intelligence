# Qwen3.8-27B

**Creator:** Alibaba / Qwen · **Family:** Qwen3.8 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-08-14

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Local multimodal coding (medium confidence)

A credible compact candidate for iterative code editing and image-grounded workflows.

Scope: compound / conditional. Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): coding.scoped_edit; vision.question_answering

Judgment ID: judgment-dadec61aa2e25c5d

Conditions: Use supported thinking/template settings; compare medium and xhigh by whole-task cost.

Failure modes / limitations: Dependent tool-call ordering failures and runtime grammar issues were reported in one local setup.

Supporting sources: [Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B) · [Qwen3.8 27B xhigh independently profiled](https://artificialanalysis.ai/models/qwen3-8-27b) · [Single-R9700 Qwen3.8 comparison](https://www.reddit.com/r/Qwen_AI/comments/1wxshto/qwen3827b_vs_qwen38flashnext_as_agent_workers_on/)

Contradictory or limiting sources: [Single-R9700 Qwen3.8 comparison](https://www.reddit.com/r/Qwen_AI/comments/1wxshto/qwen3827b_vs_qwen38flashnext_as_agent_workers_on/)

### Long context reasoning (low confidence)

Treat million-token mode as an extension to validate, rather than a proven local operating point.

Scope: unresolved / warning. Scope needs review; the original claim does not establish a specific task ability.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): context.reasoning

Judgment ID: judgment-6db95607e291642c

Conditions: Native 262,144; extension requires appropriate runtime configuration and memory.

Failure modes / limitations: Long reasoning traces, context pressure, retrieval misses.

Supporting sources: [Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B)

Contradictory or limiting sources: [Qwen3.8 27B xhigh independently profiled](https://artificialanalysis.ai/models/qwen3-8-27b)

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Dense hybrid Gated DeltaNet / gated-attention decoder with vision encoder |
| parameters | total billion: 27; active billion: 27; scope: 27B language model; official HF tensor metadata rounds complete artifact to 28B.; exact parameter count: Unknown / not established |
| context window | native tokens: 262144; extended tokens: 1000000; max output tokens: Unknown / not established; notes: Input plus generated output share capacity. Endpoint limits can differ. |
| maximum output | Unknown / not established |
| modalities | input: text; image; video; output: text |
| language support | supported: Unknown / not established; notes: Exact supported-language list not verified in this bounded pass. |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

1 recorded access route(s); 0 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Apache-2.0

Restrictions: Retain copyright/license notices; comply with the license.; A license summary, not legal advice. Open weights does not by itself establish a fully open-source AI system.

Commercial use: allowed

Redistribution: true

Hosted service: true

Local weights/runtime availability: available

Hardware: Planning estimate: 24–32GB GPU or 32–48GB unified memory with 4-bit weights, modest context; BF16 usually needs 64–80GB class memory.; 27B is the language-model declaration; HF serialized model is approximately 28B including additional components.

Local conditions: Batch 1, short/moderate context unless otherwise stated.; Weight-only floors exclude quantization metadata, KV cache, activations, vision encoder if outside the stated count, runtime, OS and temporary loading buffers.; Offloading changes RAM/VRAM allocation and throughput; low active parameter count does not eliminate storage of inactive experts.; Published maximum context is not a guarantee it fits on the suggested local machine.

## Gaps and caveats

- No model inference or benchmark was run in this research pass.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|

## Recorded access routes

- hugging-face / weight_distribution: documented route; account eligibility unverified. identity_note: Hugging Face hosts artifacts; the creator is Alibaba / Qwen

## Sources

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) · [Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B) · [Single-R9700 Qwen3.8 comparison](https://www.reddit.com/r/Qwen_AI/comments/1wxshto/qwen3827b_vs_qwen38flashnext_as_agent_workers_on/) · [Qwen3.8 27B xhigh independently profiled](https://artificialanalysis.ai/models/qwen3-8-27b)
