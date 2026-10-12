# GPT Image 2.5 Flare

**Creator:** OpenAI · **Family:** GPT Image2.5 · **Status:** active
**Verified:** 2026-10-06 · **Release:** 2026-09-08

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Everyday image generation (low confidence)

Latency-oriented image generation choice.

Scope: direct / conditional. One task reference; conclusion remains conditional, not an ability score.

Direct task IDs: image.generation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-399c0b738f152d10

Conditions: Quality, resolution, reference images and retries change consumption.

Failure modes / limitations: Not established in this pass

Supporting sources: [Introducing ChatGPT Images 2.5](https://openai.com/index/introducing-chatgpt-images-2-5/) · [gpt-image-2.5-flare model specifications](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare) · [Create image API reference](https://developers.openai.com/api/reference/resources/images/methods/generate)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: supporting evidence: Vendor positions Sunburst for finer editing control and Flare for faster generation.; contradictory evidence: No independent model-specific head-to-head recovered in this bounded pass; equal token prices do not imply equal cost per image.; Observation obs-144443616836: Latency-oriented image generation choice.; Potential risk (not a measured failure): Inspect text, local edits and identity consistency; these checks are prudent risk controls, not measured failure rates.; Confidence limited by vendor-heavy task evidence and missing exact-task independent replication; documented interface support alone is not task quality.

### Image.editing (low confidence)

Independent registered-OCR checks find fewer surrounding receipt-text changes, without an established target-field correctness improvement. Faithful repeated editing remains conditional.

Scope: direct / warning. Task-specific source investigation; original migration bundles remain unchanged.

Direct task IDs: image.editing

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-2ca135b74c458093

Conditions: E1 199 receipt edits at medium quality; exact named Flare/Sunburst API; registered OCR, not human visual fidelity.

Failure modes / limitations: Collateral text changes persist; improved surrounding-text OCR preservation is not precise target editing.

Supporting sources: [Task-specific Images 2.5 evaluation](https://arxiv.org/html/2609.13617v1) · [Introducing ChatGPT Images 2.5](https://openai.com/index/introducing-chatgpt-images-2-5/) · [gpt-image-2.5-flare model specifications](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare)

Contradictory or limiting sources: [Task-specific Images 2.5 evaluation](https://arxiv.org/html/2609.13617v1)

Evidence notes: Low confidence in broad fidelity: one independent automatic scorer, post-hoc alignment sensitivity and no human replication.; No located contrary source is not proof of agreement; search scope and remaining gaps are recorded in the coverage ledger.

### Image.generation (low confidence)

Higher quality helped large portrait texture, but upper-tier repeats did not show a reliable high-to-max improvement.

Scope: direct / conditional. Limited to the named task and reported source configuration; no transfer to neighboring tasks.

Direct task IDs: image.generation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-022e710d0ee58887

Conditions: Four prompts, 29 images; three 1024x1024 prompts and a 2880x2880 portrait; four samples at each upper tier.

Failure modes / limitations: Clock-hand constraints were not reliably fixed by higher settings.

Supporting sources: [What GPT Image 2.5 Flare quality actually buys you](https://sanand0.github.io/llmevals/gpt-image-flare-quality/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Qualitative first-person review; exact date, route and immutable served revision undisclosed.

### Image.generation (low confidence)

Repeated image prompts reveal useful composition with persistent spatial and exact-constraint errors.

Scope: direct / conditional. Limited to the named task and reported source configuration; no transfer to neighboring tasks.

Direct task IDs: image.generation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-298dd9fed2153242

Conditions: AIMLAPI, named undated Flare, medium quality, 1536x1024; September 9, 2026; three runs per test.

Failure modes / limitations: All three mirror and refraction trials failed; fruit constraints scored 3/7, 4/7 and 4/7.

Supporting sources: [GPT Image 2.5 vs GPT Image 2: the same tests, re-run](https://www.promptfrenzy.com/benchmark/gpt-image-2-5-vs-gpt-image-2)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Hand scoring on a small published prompt set; historical baseline not concurrently rerun.

### Image.editing (low confidence)

An eight-edit duck sequence usually satisfied the rubric but introduced an unwanted color change in one run.

Scope: direct / conditional. Limited to the named task and reported source configuration; no transfer to neighboring tasks.

Direct task IDs: image.editing

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-fa6ad43224ee39c4

Conditions: AIMLAPI, medium quality, 1536x1024; three repetitions of eight edits on September 9, 2026.

Failure modes / limitations: First run scored 7/8 after an unrequested yellow duck; two runs scored 8/8.

Supporting sources: [GPT Image 2.5 vs GPT Image 2: the same tests, re-run](https://www.promptfrenzy.com/benchmark/gpt-image-2-5-vs-gpt-image-2)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Narrow synthetic sequence; cannot establish production identity or document fidelity.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | Unknown / not established |
| maximum output | Unknown / not established |
| modalities | input: text; image; output: image |
| language support | Unknown / not established |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

5 recorded access route(s); 3 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: OpenAI proprietary hosted service; OpenAI Services Agreement and Service Terms

Restrictions: Comply with applicable law, input rights, OpenAI policies and documented API limits.; No service reverse engineering or safeguard/rate-limit circumvention.; Visual likeness reproduction requires express consent and necessary rights.

Commercial use: API integration in customer applications is permitted subject to applicable terms, rights and policies; output rights are assigned as between OpenAI and customer.

Redistribution: Unknown / not established

Hosted service: API-backed customer applications may be provided to end users; account resale or credential sharing is prohibited.

Local weights/runtime availability: unavailable

Hardware: Not established in this pass

Local conditions: Not established in this pass

## Gaps and caveats

- Undisclosed architecture and parameter count
- Exact supported-language inventory and per-language quality not verified

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| openai | Standard / current | input: 8 USD / per 1 million image tokens; cached_input: 2 USD / per 1 million image tokens; output: 30 USD / per 1 million image tokens | Input image/text charges; actual output token consumption varies | 2026-10-06 |
| openai | Standard / current | input: 5 USD / per 1 million text tokens; cached_input: 1.25 USD / per 1 million text tokens; output: unknown USD / per 1 million text tokens | Input image/text charges; actual output token consumption varies | 2026-10-06 |
| openai | Batch / current | output: 15 USD / per 1 million image output tokens | Not established in this pass | 2026-10-06 |

## Recorded access routes

- azure-foundry / Azure OpenAI image generation: GA_documented_numeric_price_unverified. Not established in this pass
- openai / ChatGPT Images 2.5 / Work / Codex: Conditional consumer/client product; exact account entitlement unverified. Images product is available across tiers; thinking image mode Plus/Pro/Business, Enterprise/Edu described as coming soon.
- openai / Images API / Responses image-generation tool: officially_documented_not_execution_tested. Not established in this pass
- openai / ChatGPT Images2.5 / Work / Codex: Images2.5 available across tiers; precise underlying API variant selection in each UI not established. Not established in this pass
- openai / Images API / Responses image-generation tool: Available. quota: Usage tier/account-specific; no fixed image count inferred

## Sources

[gpt-image-2.5-flare model specifications](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare) · [Introducing ChatGPT Images 2.5](https://openai.com/index/introducing-chatgpt-images-2-5/) · [Create image API reference](https://developers.openai.com/api/reference/resources/images/methods/generate) · [Task-specific Images 2.5 evaluation](https://arxiv.org/html/2609.13617v1)
