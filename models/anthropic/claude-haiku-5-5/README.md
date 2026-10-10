# Claude Haiku 5.5

**Creator:** Anthropic · **Family:** Claude 5.5 · **Status:** active
**Verified:** 2026-10-07 · **Release:** 2026-10-07

[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)

## Task judgments

### Knowledge.classification (low confidence)

Candidate for short label-assignment requests; creator positioning supports a conditional trial, not measured accuracy across label sets.

Scope: direct / conditional. Limited to the stated task and inspected evidence; no universal ranking.

Direct task IDs: knowledge.classification

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-27ba5595ff0f118f

Conditions: Launch-day public evidence; exact deployment must match the recorded setup.

Failure modes / limitations: Independent task-specific replication and production acceptance remain unknown.

Supporting sources: [Claude Haiku 5.5 overview](https://platform.claude.com/docs/en/models/haiku-5-5/overview)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence because source/setup support is sparse or vendor-heavy; no contrary result located in this bounded pass is not agreement.

### Knowledge.extraction (low confidence)

Candidate for bounded extraction from supplied material; no independently inspected extraction dataset establishes general reliability.

Scope: direct / conditional. Limited to the stated task and inspected evidence; no universal ranking.

Direct task IDs: knowledge.extraction

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-fad82c58efab1580

Conditions: Launch-day public evidence; exact deployment must match the recorded setup.

Failure modes / limitations: Independent task-specific replication and production acceptance remain unknown.

Supporting sources: [Claude Haiku 5.5 overview](https://platform.claude.com/docs/en/models/haiku-5-5/overview)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence because source/setup support is sparse or vendor-heavy; no contrary result located in this bounded pass is not agreement.

### Language.summarization (low confidence)

Candidate for short summaries; creator launch claims remain unreplicated under a specified fidelity evaluation.

Scope: direct / conditional. Limited to the stated task and inspected evidence; no universal ranking.

Direct task IDs: language.summarization

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-8550661dd3250cd7

Conditions: Launch-day public evidence; exact deployment must match the recorded setup.

Failure modes / limitations: Independent task-specific replication and production acceptance remain unknown.

Supporting sources: [Haiku 5.5 launch](https://www.anthropic.com/claude-haiku-5-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence because source/setup support is sparse or vendor-heavy; no contrary result located in this bounded pass is not agreement.

### Agent.computer_use (low confidence)

Vendor OSWorld 2.1 offline results show 72.4% partial checkpoint credit but 37.1% strict all-checkpoint completion. Supervised GUI work can be useful; reliable final-state verification and recovery remain material requirements.

Scope: direct / conditional. Limited to the stated task and inspected evidence; no universal ranking.

Direct task IDs: agent.computer_use

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-b1c7dd3088dba162

Conditions: 82 offline tasks, five independent attempts each, 1080 p, max 500 actions, max effort, no VM internet.

Failure modes / limitations: Most attempts did not satisfy every checkpoint; partial score is not complete workflow success.

Supporting sources: [Haiku 5.5 launch](https://www.anthropic.com/claude-haiku-5-5) · [Claude Haiku 5.5 System Card](https://www.anthropic.com/document/claude-haiku-5-5-system-card)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Original system-card text and rendered figure freshly inspected; vendor-only confidence remains low.

### Reasoning.general (low confidence)

HLE 45.9% no-tools and 57.4% tool-assisted are multidisciplinary academic results. They do not isolate the general logical-reasoning rubric.

Scope: direct / conditional. Limited to the stated task and inspected evidence; no universal ranking.

Direct task IDs: reasoning.general

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-2a8d07b5d42de50a

Conditions: Max adaptive thinking, 980k task budget, no compaction; Opus 4.6 grader; tool-enabled search/fetch/code configuration kept separate.

Failure modes / limitations: No exact general-logic score can be derived from this mixed benchmark.

Supporting sources: [Haiku 5.5 launch](https://www.anthropic.com/claude-haiku-5-5) · [Claude Haiku 5.5 System Card](https://www.anthropic.com/document/claude-haiku-5-5-system-card)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Existing direct finding identity/scope preserved; this legacy link is not treated as a direct general-reasoning endorsement.

### Vision.question_answering (low confidence)

Vendor Chartography gives 46.4% without tools and 86.2% with a container/image cropping. Both are conditional specialized-chart QA results; tool assistance changes the assessed setup.

Scope: direct / conditional. Limited to the stated task and inspected evidence; no universal ranking.

Direct task IDs: vision.question_answering

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-f7c3002252f74a20

Conditions: 100 specialized chart tasks, mean of five runs, max adaptive thinking; Gemini 3.5 Flash grader with expert acceptable ranges.

Failure modes / limitations: Unassisted chart answers remain frequently incorrect; no transfer to precise visual grounding.

Supporting sources: [Haiku 5.5 launch](https://www.anthropic.com/claude-haiku-5-5) · [Claude Haiku 5.5 System Card](https://www.anthropic.com/document/claude-haiku-5-5-system-card)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: One vendor study across two configurations; confidence remains low. Independent Roboflow task evidence is a separate new finding.

### Agent.tool_use (low confidence)

Warning: structured JSON with thinking disabled can skip a required tool; creator suggests adaptive thinking or explicit tool choice.

Scope: direct / warning. Limited to the stated task and inspected evidence; no universal ranking.

Direct task IDs: agent.tool_use

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-5c1cc68fa486d6fe

Conditions: Effort and prompt length matter; no transfer to arbitrary harnesses.

Failure modes / limitations: Creator-reported limitation; frequency and independent recovery unknown.

Supporting sources: [Haiku 5.5 prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence because source/setup support is sparse or vendor-heavy; no contrary result located in this bounded pass is not agreement.

### Agent.long_horizon (low confidence)

Warning: long agent prompts at low effort can stop early; creator mitigation is prompting or higher effort, without independently measured recovery.

Scope: direct / warning. Limited to the stated task and inspected evidence; no universal ranking.

Direct task IDs: agent.long_horizon

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-92f36cfb1da4e0f4

Conditions: Effort and prompt length matter; no transfer to arbitrary harnesses.

Failure modes / limitations: Creator-reported limitation; frequency and independent recovery unknown.

Supporting sources: [Haiku 5.5 prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Low confidence because source/setup support is sparse or vendor-heavy; no contrary result located in this bounded pass is not agreement.

### Coding.repository_work (low confidence)

Creator documents that low/medium-effort code changes can be reported complete without an exercising check. A verification prompt reportedly helps, but frequency and independent recovery are unmeasured.

Scope: direct / warning. Limited to the stated task and inspected evidence; no universal ranking.

Direct task IDs: coding.repository_work

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-d5a912ae74e8e488

Conditions: Exact Haiku 5.5 prompting guide; effort, prompt length and harness affect behavior.

Failure modes / limitations: Skipped testing or early stopping; no quantified broad repository-failure rate.

Supporting sources: [Haiku 5.5 prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Fresh original guide inspection; retain low-confidence warning alongside independently measured repository work.

### Coding.debugging (low confidence)

A single range-merging repair diagnosed and corrected mutation, boundary, nesting and invalid-range defects. One generated program passed 19, 448 valid executions and 16 invalid inputs, but mixed list/tuple pairs still raised TypeError.

Scope: direct / conditional. Limited to the named task and the stated setup; no transfer from a mixed score or grader identity.

Direct task IDs: coding.debugging

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-011a2b23f886e43e

Conditions: Claude.ai Free, Medium effort, fresh chat, no tools; Python 3 function and four requested assertions.; Execution count tests one generated program, not 19, 448 independent model trials.

Failure modes / limitations: Input-container assumption was unresolved; one function cannot establish repository-wide debugging reliability.

Supporting sources: [Claude Haiku 5.5 review: four editorial tasks](https://joinoasis.com/blog/claude-haiku-5-5-review)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Agent.tool_use (low confidence)

Crazyrouter reports 3/3 successful two-turn read-only order lookups, including tool selection, arguments and use of the fixed simulated result.

Scope: direct / conditional. Only the source-described task and setup; no transfer to unrelated tasks or routes.

Direct task IDs: agent.tool_use

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-0e2407bb0e5c40df

Conditions: Chinese prompts, thinking disabled, max_tokens=2048, fixed undisclosed upstream using native Anthropic protocol.; One order-lookup task repeated three times; final JSON formatting scored separately.

Failure modes / limitations: No permissions, writes, multi-tool planning or sustained error recovery tested.; Unknown upstream implementation limits transfer to first-party API or other clients.

Supporting sources: [Claude Haiku 5.5 vs Sonnet 4.6: An Everyday Benchmark](https://crazyrouter.com/en/blog/claude-haiku-5-5-vs-sonnet-4-6-everyday-benchmark-2026-en)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Original public body inspected on 2026-10-08; attribution and setup preserved.

### Language.instruction_following (low confidence)

AINews demonstrates that a label-only instruction is insufficient for some migrated short-output requests; disabled thinking or a low-effort enum schema recovered valid label formatting in its selected test.

Scope: direct / conditional. Only the source-described task and setup; no transfer to unrelated tasks or routes.

Direct task IDs: language.instruction_following

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-13c2b90c21a358d4

Conditions: Fifteen selected tickets, three attempts each per configuration on the Claude API.; Default cap 10 returned 38/45 valid labels; disabled-thinking cap 10 and low+schema cap 32 each 45/45.

Failure modes / limitations: Unchanged small token caps can end in thinking before any text; prose can violate label-only instructions.; Valid label format does not establish correct label semantics or general instruction following.

Supporting sources: [Haiku 5.5 classifier migration: hardest tickets and output recovery](https://www.ainews.tech/blog/haiku-5-5-classifier-drops-the-hardest-tickets)

Contradictory or limiting sources: [Haiku 5.5 prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5)

Evidence notes: Source reports a local exception to the guide’s visible-reasoning tendency: disabled thinking produced no prose here. Prompt/setup differences prevent a general conflict claim.

### Language.writing (low confidence)

Polish client-email, LinkedIn and story samples were judged natural and useful; editing remains necessary for constraint-sensitive prose.

Scope: direct / conditional. Only the stated task and source-described setup; no universal model ranking.

Direct task IDs: language.writing

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-14b370d8ea21baf6

Conditions: Piotr Olszewski; OpenRouter low effort; one output per task; GPT-6 Sol and Gemini 3.1 Pro judges.

Failure modes / limitations: Small heterogeneous sample; model judges and undisclosed downstream serving route; no human calibration for this exact model.

Supporting sources: [Claude Haiku 5.5: Polish-language original laboratory test](https://promptowy.com/claude-haiku-5-5/) · [Laboratorium Promptowe: independent Polish AI test methodology](https://promptowy.com/laboratorium-promptowego/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Reported task scores 8.2–8.3/10 are judge ratings, not correctness rates; composite 76.8 is not assigned to writing.

### Knowledge.classification (low confidence)

One eight-ticket routing response matched the supplied policy and JSON contract, including a conflicting ticket instruction.

Scope: direct / conditional. Only the stated task and source-described setup; no universal model ranking.

Direct task IDs: knowledge.classification

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-167a64ec15f54fe0

Conditions: Claude.ai Free, Medium effort, fresh chat, no tools; eight fictional tickets.

Failure modes / limitations: Only one response; all-users outage scope ambiguous; no general injection-resistance conclusion.

Supporting sources: [Claude Haiku 5.5 review: four editorial tasks](https://joinoasis.com/blog/claude-haiku-5-5-review)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Author Karthikeya Meesala checked the eight expected labels and four-field JSON structure.

### Language.writing (low confidence)

The author reports chat titles sometimes answer the message rather than naming it, requiring checking before automatic use.

Scope: direct / warning. Only the stated task and source-described setup; no universal model ranking.

Direct task IDs: language.writing

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-1ab53d0b016215de

Conditions: Fifty-two application messages; reasoning off; one run per setup; blind Opus judge in both A/B orders.

Failure modes / limitations: Provider and precise prompt undisclosed; 28 comparator wins, 8 Haiku wins, 9 order-disagreement ties, 7 identical titles.

Supporting sources: [Haiku 5.5 versus DeepSeek V4.1 Flash on two application jobs](https://www.reddit.com/r/ClaudeAI/comments/1x0iu5x/haiku_55_vs_deepseek_v41_flash_on_my_2_boring/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Preference counts are not a semantic accuracy rate; one injected message became a title.

### Language.instruction_following (low confidence)

u/dergachoff reports that Haiku 5.5 often answered messages rather than naming the chat, and copied one prompt-injection test message into the title.

Scope: direct / warning. Only the source-described task and setup; no transfer to unrelated tasks or routes.

Direct task IDs: language.instruction_following

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-2eeb54292ab8e544

Conditions: 52 messages; reasoning disabled; one run per setup; app route/provider not disclosed.; Blind Opus judges used both A/B orders; order disagreement counted as a tie.

Failure modes / limitations: The frequency of answer-instead-of-title failures is not enumerated.; Preference counts against another model are not a correctness pass rate.

Supporting sources: [Haiku 5.5 versus DeepSeek V4.1 Flash on two application jobs](https://www.reddit.com/r/ClaudeAI/comments/1x0iu5x/haiku_55_vs_deepseek_v41_flash_on_my_2_boring/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Retain this thinking-disabled title workflow separately from low/medium-effort Polish and Claude.ai examples.

### Coding.repository_work (medium confidence)

Cognition’s repository tasks show useful but incomplete merge-ready work in Claude Code:medium Main composite 41.63 and max 46.36, with separate correctness rates 46.2% and 51.65%. Repository conventions and hidden checks remain necessary.

Scope: direct / conditional. Limited to the named task and the stated setup; no transfer from a mixed score or grader identity.

Direct task IDs: coding.repository_work

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-3b72450649afcdb5

Conditions: Main 100 tasks, Extended 150; five runs per task; fair internet use allowed with solution-bearing access zeroed.; Composite combines functionality and code-quality criteria; no direct architecture/refactoring/test-design rating from its total.

Failure modes / limitations: Roughly half of Main functional outcomes fail in these configurations; complete prompt/runtime/provider and run dates undisclosed.

Supporting sources: [FrontierCode public result data v 1.1](https://cognition.com/data/frontiercode-leaderboard/data.json) · [FrontierCode 1.1](https://cognition.com/blog/frontier-code-1.1) · [FrontierCode Leaderboard](https://cognition.com/frontiercode) · [Claude Haiku 5.5 System Card](https://www.anthropic.com/document/claude-haiku-5-5-system-card)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Reasoning.scientific (low confidence)

In five statistical-inference traps, the Plotly agent passed 2 and failed 3. It omitted a confounder check, used the wrong observational unit, and abandoned a supported causal explanation; these are core limits for this bounded causal-analysis workflow.

Scope: direct / warning. Limited to the named task and the stated setup; no transfer from a mixed score or grader identity.

Direct task IDs: reasoning.scientific

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-426b1ceddfdc7b59

Conditions: Plotly Studio Embedded over a private synthetic wind-fleet warehouse; each question requires a correct answer or the relevant catch, no partial credit.

Failure modes / limitations: Effort, run date, provider and replication undisclosed; 2/5 is a small subset and does not characterize all science.

Supporting sources: [Claude Haiku 5.5 Data Analytics Benchmark Results](https://plotly.com/blog/claude-haiku-5-5-plotly-data-analytics-bench/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Knowledge.rag (low confidence)

Anthropic’s modified WANDR evaluates cited fact collections retrieved from a frozen index, with Haiku 5.5 soft F1 rising from 3.5% at low to 49.9% at max effort.

Scope: direct / conditional. Only the source-described task and setup; no transfer to unrelated tasks or routes.

Direct task IDs: knowledge.rag

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-4907576ea352b1d3

Conditions: 500 tasks requiring tens to hundreds of entities and facts; frozen-index web search/fetch, programmatic tool calling and code execution with 980k-token task budget.; Opus 4.6 re-fetches cited URLs to judge whether they support each fact; invalid-format entity rows are dropped.; Visual graph inspection p123:low 3.5%,medium 12.9%,high 37.3%,xhigh 45.9%,max 49.9%.

Failure modes / limitations: Soft F1 mixes verified fact precision and requested collection recall; it is not an all-correct answer or retrieval-ranking rate.; Frozen index and judge differ from Perplexity’s live-web/GPT-5.4 setup; no cross-harness score equivalence.

Supporting sources: [Claude Haiku 5.5 System Card](https://www.anthropic.com/document/claude-haiku-5-5-system-card)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: A documented external-retrieval and answer-support workflow is established, unlike the preselected-document OfficeQA configuration. General application RAG fit remains unestablished.

### Coding.tests (low confidence)

The same reply supplied four meaningful assertions for touching boundaries, nesting, input preservation and invalid ranges. Their visible expected outcomes distinguish the supplied defects, but the suite omitted mixed pair-container inputs.

Scope: direct / conditional. Limited to the named task and the stated setup; no transfer from a mixed score or grader identity.

Direct task IDs: coding.tests

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-4d393d5034eb0aee

Conditions: Original screenshot inspected: assertions include expected outputs and explicit ValueError flag; reviewer reports execution unchanged.; Test categories were supplied in the prompt; one generated suite for one function.

Failure modes / limitations: No mutation-testing/coverage study; homogeneous tuple input cannot test nested mutable-input preservation or heterogeneous-container behavior.

Supporting sources: [Claude Haiku 5.5 review: four editorial tasks](https://joinoasis.com/blog/claude-haiku-5-5-review)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Coding.scoped_edit (low confidence)

Eight selected Python functions passed hidden assertions at low, medium and high effort; max failed to emit one implementation before its output cap. This supports bounded implementation work with executable acceptance checks.

Scope: direct / conditional. Limited to the named task and the stated setup; no transfer from a mixed score or grader identity.

Direct task IDs: coding.scoped_edit

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-4edd9c57ae9dfb08

Conditions: Direct Claude API, 32k output cap; one generation for each task/effort; corrected SemVer rerun replaces original attempt.

Failure modes / limitations: Small selected corpus; unreported full artifacts and a max-effort budget failure limit repeatability.

Supporting sources: [Claude Haiku 5.5 Released: Pricing, Benchmarks, vs Haiku 4.5](https://computingforgeeks.com/claude-haiku-5-5-released-features-benchmarks/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Agent.long_horizon (medium confidence)

The system card reports 43.8% mean fractional reward on FrontierSWE v2:34 ultra-long-horizon tasks with five 20-hour-budget trials each under Proximus at max effort.

Scope: direct / conditional. Only the source-described task and setup; no transfer to unrelated tasks or routes.

Direct task IDs: agent.long_horizon

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-5a56884ee5c3c4a1

Conditions: Proximus supplies compaction, progress logging, self-check feedback and checkpointed submissions; no native-client equivalence is assumed.; Original public Proximal data identifies Haiku 5.5 with 43.76868294117648% mean@5,52.753011764705896%best@5 and34.486967647058805%worst@5; reported mean duration is 44698.909 seconds.

Failure modes / limitations: Mean fractional reward does not reveal the share of fully completed goals, intervention needs or sustained success for a specific user workflow.; No independent reproduction of the low-effort early-stopping mitigation is established.

Supporting sources: [FrontierSWE v2 leaderboard](https://www.frontierswe.com/) · [FrontierSWE v2](https://www.frontierswe.com/blog/v2) · [Claude Haiku 5.5 System Card](https://www.anthropic.com/document/claude-haiku-5-5-system-card) · [FrontierSWE changelog](https://www.frontierswe.com/changelog)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Original Proximal data and methodology establish the bounded result; the card repeats the same study and does not provide independent replication.; Per-task trajectories and provider deployment details remain uninspected or undisclosed.

### Language.writing (low confidence)

Short writing is useful with editing: three of five constrained prompts pass, but a plain-language rewrite retains jargon and one argument exceeds the paragraph limit.

Scope: direct / conditional. Only the stated task and source-described setup; no universal model ranking.

Direct task IDs: language.writing

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-5db6d8e9c5912ec9

Conditions: llmwise app prompt via OpenRouter, host Anthropic; no tools; max output 8,000; actual response rows October 7, 2026; effort undisclosed.

Failure modes / limitations: Corporate rewrite graded 3.3/5 with lowest criterion 2; bus argument passes quality but 103 words exceeds a 90-word paragraph cap.

Supporting sources: [llmwise Haiku 5.5 writing task results](https://llmwise.ai/best-llm-for-writing) · [llmwise fixed fifty-prompt test methods](https://llmwise.ai/our-test-runs) · [llmwise published prompt and Haiku output: announce a second bakery shop on linkedin](https://llmwise.ai/prompts/announce-a-second-bakery-shop-on-linkedin) · [llmwise published prompt and Haiku output: rewrite corporate jargon in plain words](https://llmwise.ai/prompts/rewrite-corporate-jargon-in-plain-words) · [llmwise published prompt and Haiku output: decline a meeting and offer two times](https://llmwise.ai/prompts/decline-a-meeting-and-offer-two-times) · [llmwise published prompt and Haiku output: a product announcement with five rules](https://llmwise.ai/prompts/a-product-announcement-with-five-rules) · [llmwise published prompt and Haiku output: argue both sides of free buses](https://llmwise.ai/prompts/argue-both-sides-of-free-buses)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Claude Opus 5.5 low-effort judge; one attempt per prompt. Failed-provider replies are excluded by method.

### Language.summarization (low confidence)

Short summaries preserve useful content but require length and salience checks: three of five pass, while the other two exceed their hard word limits.

Scope: direct / conditional. Only the stated task and source-described setup; no universal model ranking.

Direct task IDs: language.summarization

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-5e8af0f7fabe963e

Conditions: llmwise app prompt via OpenRouter, host Anthropic; no tools; max output 8,000; actual response rows October 7, 2026; effort undisclosed.

Failure modes / limitations: Article summary 61 words versus 60 and quality 3.7/5; email summary 39 versus 30 despite quality 4.3/5.

Supporting sources: [llmwise Haiku 5.5 summarization task results](https://llmwise.ai/best-llm-for-summarization) · [llmwise fixed fifty-prompt test methods](https://llmwise.ai/our-test-runs) · [llmwise published prompt and Haiku output: an article in three bullets](https://llmwise.ai/prompts/an-article-in-three-bullets) · [llmwise published prompt and Haiku output: an email thread in one sentence](https://llmwise.ai/prompts/an-email-thread-in-one-sentence) · [llmwise published prompt and Haiku output: decisions and action items from a meeting](https://llmwise.ai/prompts/decisions-and-action-items-from-a-meeting) · [llmwise published prompt and Haiku output: a quarterly memo for the ceo](https://llmwise.ai/prompts/a-quarterly-memo-for-the-ceo) · [llmwise published prompt and Haiku output: a study with a negative result](https://llmwise.ai/prompts/a-study-with-a-negative-result)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Claude Opus 5.5 low-effort judge; one attempt per prompt. Failed-provider replies are excluded by method.

### Context.retrieval, context.reasoning, knowledge.rag, knowledge.retrieval, knowledge.extraction (low confidence)

Anthropic’s selected launch testimonials describe AlphaSense document-question answering and Rogo 10-K lookups, but do not isolate extended-context retrieval, reasoning, or a documented RAG retriever.

Scope: compound / unknown. Only the source-described task and setup; no transfer to unrelated tasks or routes.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): context.retrieval; context.reasoning; knowledge.rag; knowledge.retrieval; knowledge.extraction

Judgment ID: judgment-67aa3dd593d907df

Conditions: AlphaSense’s Daniel Campos describes400questions over one or a few documents and an unspecified score0.84 versus0.76 for Haiku 4.5.; Rogo’s Alex Wang describes retrieving a segment-revenue line for a larger-model deck workflow.

Failure modes / limitations: Input lengths, placement, corpus/retriever setup, grading, effort and provider route are undisclosed.; Selected customer testimony is not independent original evaluation publication.

Supporting sources: [Haiku 5.5 launch](https://www.anthropic.com/claude-haiku-5-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: One launch source independence group; no direct task endorsement or transfer of another model’s result.

### Language.instruction_following (low confidence)

Piotr Olszewski reports 23/26 explicit instruction rules satisfied in his 13-prompt Polish test; the five-point summary exceeded its 80-word limit.

Scope: direct / conditional. Only the source-described task and setup; no transfer to unrelated tasks or routes.

Direct task IDs: language.instruction_following

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-774b4c9c38835241

Conditions: OpenRouter anthropic/claude-haiku-5.5; low reasoning; tested 2026-10-08.; GPT-6 Sol and Gemini 3.1 Pro judged the writing suite; exact token caps and repeat count are not disclosed in the article.

Failure modes / limitations: Hard length limits require checking; 26 rule checks are not 26 independent prompts.

Supporting sources: [Claude Haiku 5.5: Polish-language original laboratory test](https://promptowy.com/claude-haiku-5-5/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: This direct instruction score is separate from the mixed writing composite and factual quiz.

### Language.translation (low confidence)

Five short English-to-Spanish/French/German/Japanese/Portuguese examples pass the publisher meaning-retention screen; lenient back-translation and absent human checking limit the conclusion.

Scope: direct / conditional. Only the stated task and source-described setup; no universal model ranking.

Direct task IDs: language.translation

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-836668f2db6aac0b

Conditions: llmwise app prompt via OpenRouter, host Anthropic; no tools; max output 8,000; actual response rows October 7, 2026; effort undisclosed.

Failure modes / limitations: Back-translation can miss target-language awkwardness or untranslated fragments; one example per language pair.

Supporting sources: [llmwise Haiku 5.5 translation task results](https://llmwise.ai/best-llm-for-translation) · [llmwise fixed fifty-prompt test methods](https://llmwise.ai/our-test-runs) · [llmwise published prompt and Haiku output: a delivery message into spanish](https://llmwise.ai/prompts/a-delivery-message-into-spanish) · [llmwise published prompt and Haiku output: a product description into french](https://llmwise.ai/prompts/a-product-description-into-french) · [llmwise published prompt and Haiku output: a meeting note into german](https://llmwise.ai/prompts/a-meeting-note-into-german) · [llmwise published prompt and Haiku output: idioms into natural japanese](https://llmwise.ai/prompts/idioms-into-natural-japanese) · [llmwise published prompt and Haiku output: a lease clause into brazilian portuguese](https://llmwise.ai/prompts/a-lease-clause-into-brazilian-portuguese)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Claude Opus 5.5 low-effort judge; one attempt per prompt. Failed-provider replies are excluded by method.

### Coding.scoped_edit (medium confidence)

On fixed-contract PHP and Go modifications, medium/high settings produced useful implementations but PHP import/sync attempts still incurred failed checks; shipping quotes earned all 5 points in both settings.

Scope: direct / conditional. Limited to the named task and the stated setup; no transfer from a mixed score or grader identity.

Direct task IDs: coding.scoped_edit

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-8519c22c2d0cdf56

Conditions: Claude Code; five fresh attempts per project with hidden deterministic checks; CSV and sync results are quality-point sums, not pass counts.

Failure modes / limitations: Partial failures require material acceptance testing; exact provider and CLI version undisclosed.

Supporting sources: [Haiku 5.5 Coding Benchmark](https://aicodingdaily.com/model/haiku-5-5) · [LLM Coding Leaderboard: My Methodology and Scoring Formulas](https://aicodingdaily.com/article/llm-coding-leaderboard-my-methodology-and-scoring-formulas)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Language.writing (low confidence)

A support draft preserved important policy distinctions and requested missing evidence, but its internal note exceeded the length limit and needed tone editing.

Scope: direct / conditional. Only the stated task and source-described setup; no universal model ranking.

Direct task IDs: language.writing

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-8867f39aa4bdde41

Conditions: Claude.ai Free Medium, one fresh no-tool chat; fictional refund/deletion policy.

Failure modes / limitations: Internal note 64 words versus under 60; customer reply 86 words; author would soften final sentence.

Supporting sources: [Claude Haiku 5.5 review: four editorial tasks](https://joinoasis.com/blog/claude-haiku-5-5-review)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Whitespace count excludes headings. Content success does not erase the instruction miss.

### Reasoning.general (low confidence)

The article reports a correct minimal 5-minute schedule repair, confirmed by enumeration. Its published prompt block also includes the solution summary; the screenshot shows only the answer, so clean unassisted reasoning remains unresolved.

Scope: unresolved / unknown. Limited to the named task and the stated setup; no transfer from a mixed score or grader identity.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): reasoning.general

Judgment ID: judgment-98608fcccfe9ab7a

Conditions: One Claude.ai Free Medium reply with no tools; underlying prompt transcript not independently visible.

Failure modes / limitations: Potential editorial formatting error versus answer-bearing input cannot be resolved from the public body.

Supporting sources: [Claude Haiku 5.5 review: four editorial tasks](https://joinoasis.com/blog/claude-haiku-5-5-review)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Vision.question_answering (medium confidence)

Image-question results are useful with checking:visual reasoning judge accuracy 68.9% low/74.8% high and counting 68.9%/73.0%, with lower strict-match scores in some settings.

Scope: direct / conditional. Limited to the named task and the stated setup; no transfer from a mixed score or grader identity.

Direct task IDs: vision.question_answering

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-aa99bcfcb8165b0a

Conditions: Three runs per effort; Gemini 3.5 Flash temperature 0 judges against ground truth, with strict normalized answer matching shown separately.

Failure modes / limitations: Residual interpretation errors are material; unknown dataset denominator/resolution and inconsistent site-wide composite prevent stronger generalization.

Supporting sources: [Visual Reasoning Benchmark](https://playground.roboflow.com/evals/visual-reasoning) · [Object Counting Benchmark | Vision Evals](https://playground.roboflow.com/evals/object-counting) · [Vision Evals methodology](https://playground.roboflow.com/evals)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Vision.grounding (medium confidence)

Roboflow’s repeated detection task supports zero-shot labeled boxes with material localization checking:mAP@50 is 65.8 at low and 68.2 at high, falling to 52.3/53.0 across stricter IoU thresholds.

Scope: direct / conditional. Limited to the named task and the stated setup; no transfer from a mixed score or grader identity.

Direct task IDs: vision.grounding

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-acdb24a71a38f8c7

Conditions: Three runs per native effort; normalized box coordinates and fixed class labels; ground-truth mAP scoring.

Failure modes / limitations: Exact sample count, resolution and request manifest undisclosed; no GUI-workflow completion inference.

Supporting sources: [Object Detection Benchmark](https://playground.roboflow.com/evals/object-detection) · [Vision Evals methodology](https://playground.roboflow.com/evals)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Language.instruction_following (low confidence)

Crazyrouter reports only 1/24 original final outputs directly parseable as plain JSON despite prompt-only format instructions; Haiku also missed an 80–120-character rewrite minimum in two of three runs.

Scope: direct / warning. Only the source-described task and setup; no transfer to unrelated tasks or routes.

Direct task IDs: language.instruction_following

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-b03703cf1d5e9d5f

Conditions: Same Chinese-prompt suite, thinking disabled and max_tokens=2048 on a fixed undisclosed upstream.; The rewrite outputs were 78, 84 and 76 characters; all reportedly preserved source facts.

Failure modes / limitations: Fences/explanations can break JSON consumers despite correct content.; Native schema-constrained output was not evaluated; do not infer that it fails.

Supporting sources: [Claude Haiku 5.5 vs Sonnet 4.6: An Everyday Benchmark](https://crazyrouter.com/en/blog/claude-haiku-5-5-vs-sonnet-4-6-everyday-benchmark-2026-en)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Content score 24/27 uses a different denominator and tolerates wrapper prose; it is not the strict-format pass rate.

### Language.instruction_following (low confidence)

Creator warnings show that strict system-prompt adherence and mid-task user-message handling depend on effort, prompting and harness message placement.

Scope: direct / warning. Only the source-described task and setup; no transfer to unrelated tasks or routes.

Direct task IDs: language.instruction_following

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-b4eaf3079f3bd70d

Conditions: High effort is suggested for strict instruction following; user input should be delivered as a user text block rather than inside tool results.

Failure modes / limitations: User pressure can weaken chatbot system-prompt adherence; legitimate mid-turn input in tool-result/system positions can be ignored.

Supporting sources: [Haiku 5.5 prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Suggestions and vendor internal improvements have no disclosed task denominator or independent recovery; they do not establish aggregate suitability alone.

### Coding.repository_work (low confidence)

One practitioner reported correct medium-effort cross-language repository integration with tests and conventions, but low effort skipped checks, missed an error fallback and gave an unsupported reason for not testing.

Scope: direct / warning. Limited to the named task and the stated setup; no transfer from a mixed score or grader identity.

Direct task IDs: coding.repository_work

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-ba1e32b7164d9463

Conditions: Rust plus legacy scripting repository; effort-specific self-report; exact CLI/provider/run dates beyondOctober 8 publication unknown.

Failure modes / limitations: Private task/artifact set and no repeated trial count; does not justify the author’s broad daily-agent recommendation.

Supporting sources: [Small controlled Haiku 5.5 coding-agent test](https://www.reddit.com/r/ClaudeCode/comments/1x132yy/is_haiku_55_good_enough_to_be_your_main_coding/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Language.instruction_following (low confidence)

Karthikeya Meesala reports correct JSON ordering/keys on eight fictional tickets, but a 64-word internal support note violated the under-60-word instruction.

Scope: direct / conditional. Only the source-described task and setup; no transfer to unrelated tasks or routes.

Direct task IDs: language.instruction_following

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-baf6423c421fc5ca

Conditions: Four fresh Claude.ai Free-plan chats at Medium effort on 2026-10-08; no tools requested.; The customer reply was 86 words under a 120-word limit. Counts exclude headings and use whitespace-separated words.

Failure modes / limitations: One embedded ticket instruction was ignored successfully; this single case does not establish general prompt-injection resistance.; Hard length compliance was not universal.

Supporting sources: [Claude Haiku 5.5 review: four editorial tasks](https://joinoasis.com/blog/claude-haiku-5-5-review)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Routing success and support-note miss can coexist; the narrow result supports validation rather than a blanket pass rate.

### Language.summarization (low confidence)

A single five-bullet Polish summary exceeded its 80-word limit and contained a syntax error; source-fidelity performance was not separately reported.

Scope: direct / warning. Only the stated task and source-described setup; no universal model ranking.

Direct task IDs: language.summarization

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-bbc616d7eebd7a45

Conditions: OpenRouter low effort; one summary among thirteen mixed tasks; two non-Anthropic judges.

Failure modes / limitations: Summary task received 5.8/10 on the publisher grading; salience, factual preservation and exact output were not separately inspectable.

Supporting sources: [Claude Haiku 5.5: Polish-language original laboratory test](https://promptowy.com/claude-haiku-5-5/) · [Laboratorium Promptowe: independent Polish AI test methodology](https://promptowy.com/laboratorium-promptowego/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: A format/language weakness is recorded without turning a mixed score into a fidelity conclusion.

### Knowledge.classification (low confidence)

A small invoice-policy test assigned all twenty-four pay/hold/return labels correctly, supporting bounded classification use with validation.

Scope: direct / conditional. Only the stated task and source-described setup; no universal model ranking.

Direct task IDs: knowledge.classification

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-c6c14e837cdab3b5

Conditions: Haiku 5.5 high effort; twenty-four invoices paired with purchase orders and delivery notes; one test.

Failure modes / limitations: No repeated-trial or production label-distribution evidence; provider, client and output budget unknown.

Supporting sources: [Claude Haiku 5.5: invoice-policy classification hands-on test](https://www.datacamp.com/blog/claude-haiku-5-5)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Josef Waples reports twenty-four correct policy decisions; extraction fields and payment execution were not measured.

### Reasoning.math (low confidence)

All five elementary arithmetic, combinatorics and probability replies reached the expected final answer and displayed valid short derivations on inspection. Evidence supports these bounded problem types, with no advanced-mathematics conclusion.

Scope: direct / conditional. Limited to the named task and the stated setup; no transfer from a mixed score or grader identity.

Direct task IDs: reasoning.math

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-c9352a63e1b4d9f2

Conditions: One reply per prompt dated 2026-10-07; llmwise via OpenRouter and Anthropic; 8k output cap, no tools; actual effort undisclosed.

Failure modes / limitations: Only five fixed prompts; automatic grade checks final answer, not every derivation; no repeated generations.

Supporting sources: [Claude vs Gemini for math: exact Haiku 5.5 responses](https://llmwise.ai/claude-vs-gemini-for-math) · [llmwise fixed fifty-prompt test methods](https://llmwise.ai/our-test-runs)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Coding.frontend (medium confidence)

The Flutter transaction-feed task provides direct interface evidence:3.5/5 points at medium and 3/5 at high across five attempts, with rendering, state, retry and pagination tests. Useful starting implementations still need material checking.

Scope: direct / conditional. Limited to the named task and the stated setup; no transfer from a mixed score or grader identity.

Direct task IDs: coding.frontend

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-cc9e887e3c17d763

Conditions: Fixed widget constructor/data-source contract; 48 checks per attempt including phone-size layout and async updates; points are not success percentages.

Failure modes / limitations: No broad accessibility/visual-design assessment; repeated project-specific failures remain.

Supporting sources: [Haiku 5.5 Coding Benchmark](https://aicodingdaily.com/model/haiku-5-5) · [LLM Coding Leaderboard: My Methodology and Scoring Formulas](https://aicodingdaily.com/article/llm-coding-leaderboard-my-methodology-and-scoring-formulas)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Context.reasoning (low confidence)

Vendor OfficeQA evaluates grounded reasoning with relevant documents preselected as extracted text; Haiku 5.5 scored 73.5% on OfficeQA and 60.3% on its 133-question Pro subset at max effort, mean of five runs.

Scope: direct / conditional. Only the source-described task and setup; no transfer to unrelated tasks or routes.

Direct task IDs: context.reasoning

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-d3ee677a27e49d79

Conditions: Agentic reasoning over historical U.S. Treasury Bulletin documents; the retrieval selection step is supplied.; The card does not disclose per-question supplied-context length, placement or dependency distribution.

Failure modes / limitations: Nontrivial answer errors remain; no inference to arbitrary1M-token reasoning or position-robust retrieval.

Supporting sources: [Claude Haiku 5.5 System Card](https://www.anthropic.com/document/claude-haiku-5-5-system-card)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: This is direct supplied-document reasoning evidence. It does not establish end-to-end external retrieval or reranking performance.

### Knowledge.extraction (low confidence)

A long-interview task produced source-matching quotes, but widely variable item counts and no gold coverage list leave complete extraction unestablished.

Scope: direct / conditional. Only the stated task and source-described setup; no universal model ranking.

Direct task IDs: knowledge.extraction

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-d5e38e96dfec2d99

Conditions: Sixty-two-minute interview; every extracted item must quote the original verbatim. Haiku ran three times at Medium and three at High.

Failure modes / limitations: Six Haiku outputs contain 45–85 items; comparison outputs contain more, but this is not a gold recall denominator and different granularity may matter.; Exact prompt/input token length, backend, checkpoint request and output cap undisclosed.

Supporting sources: [Can Haiku 5.5 take over Sonnet work? Original delegated-task test](https://www.agentcrew.cc/blog/posts/en/haiku-55-own-task-benchmark)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Author reports quote checks passed. Increasing effort did not reliably increase coverage; no source-grounded completeness score is published.

### Research.synthesis (low confidence)

In four application research briefs, missed authoritative material and unsupported source handling undermined grounded reporting, even after effort increased.

Scope: direct / warning. Only the stated task and source-described setup; no universal model ranking.

Direct task IDs: research.synthesis

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-dab8687c81a7a991

Conditions: One run per setup at low, medium and high; Exa/Brave search, page fetch, image search/analysis; blind Opus judging.

Failure modes / limitations: Brand-guideline source missed and colors guessed from screenshots; a forum-quote win used search excerpts without opening source pages.

Supporting sources: [Haiku 5.5 versus DeepSeek V4.1 Flash on two application jobs](https://www.reddit.com/r/ClaudeAI/comments/1x0iu5x/haiku_55_vs_deepseek_v41_flash_on_my_2_boring/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Four briefs and subjective pairwise judging provide a narrow Low-confidence warning. Higher effort is not evidence of recovered source fidelity.

### Coding.review (low confidence)

A repeated supplied-code review case identified a hardcoded secret and personal-data logging risks with concrete fixes. Severity labeling varied and a cosmetic naming issue was over-prioritized without the skill; this supports reviewed triage, not exhaustive defect detection.

Scope: direct / conditional. Limited to the named task and the stated setup; no transfer from a mixed score or grader identity.

Direct task IDs: coding.review

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-df67900e20adda9d

Conditions: Claude Code 2.1.284, runner 0.10.1; 2026-10-07 run 1; one case, 3 with-skill and 4 baseline generated replies, each judged 3 times by Claude Opus 5.; Receipt gives grading rationale; the three-run report studies skill lift, not a broad model ranking.

Failure modes / limitations: Only one review scenario; full code/transcripts not published; repeated grader scores are not additional model generations.

Supporting sources: [Report 014: Claude Haiku 5.5 on release day, three skills](https://driftproofhq.com/reports/014/) · [Driftproof Report 014 Haiku 5.5 review run 1 receipt](https://driftproofhq.com/reports/014/evidence/run-1/code-review-and-quality-claude-haiku-5-5-2026-10-07.json)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

### Coding.review (low confidence)

All three planted validation-script bugs were found in each of three medium and three high effort runs. This corroborates narrow supplied-code review usefulness without establishing broad defect recall.

Scope: direct / conditional. One validation-script bug-finding scenario,not repair execution or a mixed-task total.

Direct task IDs: coding.review

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-e38ef14d0467ef9e

Conditions: Answer key established before model runs; one script,three planted bugs,two effort configurations with three generations each.

Failure modes / limitations: Full script/outputs,precise client/provider/tool manifest and run dates are undisclosed; private selected-task evidence.

Supporting sources: [Can Haiku 5.5 take over Sonnet work? Original delegated-task test](https://www.agentcrew.cc/blog/posts/en/haiku-55-own-task-benchmark)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Original article Q6 inspected; unrelated permission-block failure and seven-task totals are not mapped onto this task.

### Context.reasoning, context.retrieval, coding.repository_work (low confidence)

Anthropic reports 82.0% hidden behavioral-test pass rate for long-context program reconstruction, with episodes reaching up to 1M tokens.

Scope: compound / conditional. Only the source-described task and setup; no transfer to unrelated tasks or routes.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): context.reasoning; context.retrieval; coding.repository_work

Judgment ID: judgment-e8a4640fbffb0def

Conditions: ProgramBench retained166 of 200 tasks after excluding 34 where the reference binary scored below 0.9; only tests passed by the reference are scored.; Input is a compiled binary plus project documentation; internet and decompilation tools unavailable; mini-swe-agent without the upstream six-hour limit.

Failure modes / limitations: Coding reconstruction and behavioral testpass are not isolated passage retrieval or position-controlled context reasoning.; Task length varies and no retrieval-only breakdown is supplied.

Supporting sources: [Claude Haiku 5.5 System Card](https://www.anthropic.com/document/claude-haiku-5-5-system-card)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Direct task conclusions should not be inferred from the broad long-context label.

### Knowledge.classification (low confidence)

A tight migrated output budget dropped usable labels on ambiguous tickets; disabling thinking restored label-set membership in this small test, without establishing semantic label accuracy.

Scope: direct / warning. Only the stated task and source-described setup; no universal model ranking.

Direct task IDs: knowledge.classification

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-ebf985b28bd05114

Conditions: Claude API claude-haiku-5-5; fifteen tickets repeated three times per row; output budget and thinking vary.

Failure modes / limitations: Default adaptive thinking with max_tokens 10 yields 38/45 valid labels; five empty responses and two prose outputs.

Supporting sources: [Haiku 5.5 classifier migration: hardest tickets and output recovery](https://www.ainews.tech/blog/haiku-5-5-classifier-drops-the-hardest-tickets)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Thinking-disabled 10-token and low-effort 32-token enum-schema rows reach 45/45 valid labels. These are measured configuration outcomes, not service fixes or accuracy guarantees.

### Agent.tool_use (low confidence)

In u/dergachoff’s four-brief research workflow, Haiku used tools but missed a brand’s official guide at all tested effort levels and relied on search excerpts without page inspection on a forum-quote brief.

Scope: direct / warning. Only the source-described task and setup; no transfer to unrelated tasks or routes.

Direct task IDs: agent.tool_use

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-ecb2349a787cc3e7

Conditions: Same Exa/Brave search, page fetch, image search and image analysis tools for compared models.; Haiku low/medium/high; one run per setup; one high-effort brand task used60 tool calls without finding the official page.

Failure modes / limitations: Guessed colors from screenshots rather than recovering exact official values.; Excerpts alone did not establish quote author or full context.; Tool-argument validity and error handling were not separately scored.

Supporting sources: [Haiku 5.5 versus DeepSeek V4.1 Flash on two application jobs](https://www.reddit.com/r/ClaudeAI/comments/1x0iu5x/haiku_55_vs_deepseek_v41_flash_on_my_2_boring/)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: The four-brief W/T/L totals concern mixed research reports and are not a narrow tool-use success rate.

### Context.reasoning (low confidence)

On a 180-record conditional lookup, Crazyrouter reports 0/3 fully correct results: Haiku found the 117-day maximum but named extra IDs rather than only the two tied records.

Scope: direct / warning. Only the source-described task and setup; no transfer to unrelated tasks or routes.

Direct task IDs: context.reasoning

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-ee4d2ab242a02eca

Conditions: Chinese prompts, thinking disabled,max_tokens=2048; no output truncation reported.; Combines filtering with maximum/tie reasoning; record count is known but context-token length and information placement are not.

Failure modes / limitations: Correct headline value can be paired with factually wrong supporting IDs.; Diagnostic recovery changed two settings and used manual thinking syntax incompatible with official Haiku 5.5 API documentation.

Supporting sources: [Claude Haiku 5.5 vs Sonnet 4.6: An Everyday Benchmark](https://crazyrouter.com/en/blog/claude-haiku-5-5-vs-sonnet-4-6-everyday-benchmark-2026-en)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Retest 3/3 is retained as an unresolved route-specific report, not causal or independently measured native-model recovery.

### Agent.tool_use (low confidence)

Dustin reports fragile recovery from permission-denied command choices under a python3-only calculation harness, including one empty handback, followed by a 3/3 explicit-command-list retest.

Scope: direct / warning. Only the source-described task and setup; no transfer to unrelated tasks or routes.

Direct task IDs: agent.tool_use

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-f35c41eac25b47a9

Conditions: Main suite: medium/high, three trials each; original allowlist prompt visibility and permission-event denominator are not disclosed.

Failure modes / limitations: Blocked attempts included wc, cd, mkdir and command chains; most recovered but extra turns increased cost.; A permission denial is a harness event; no blocked command executed and no general model-quality fix was established.

Supporting sources: [Can Haiku 5.5 take over Sonnet work? Original delegated-task test](https://www.agentcrew.cc/blog/posts/en/haiku-55-own-task-benchmark)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: Author corrected grader bugs before reviewing the scores; those scoring mistakes are not Haiku failures.

### Performance observation (low confidence)

Performance changes substantially with tools, effort and grading:AA medium 34 versus max 43; OSWorld 72.4 partial versus 37.1 strict; Chartography 46.4 without tools versus 86.2 with tools.

Scope: performance / conditional. Configuration-dependent measurements only; no universal model score or task endorsement.

Direct task IDs: Not established in this pass

Related task IDs (navigation only): Not established in this pass

Judgment ID: judgment-8104e1d5220e56b4

Conditions: Keep distinct metrics, providers, harnesses and run provenance; scores cannot be averaged into general ability.

Failure modes / limitations: Incomplete exact setup and measurement dates; higher effort does not guarantee improvement on every task.

Supporting sources: [Claude Haiku 5.5 medium evaluation](https://artificialanalysis.ai/models/claude-haiku-5-5-medium) · [Claude Haiku 5.5 max evaluation](https://artificialanalysis.ai/models/claude-haiku-5-5) · [Claude Haiku 5.5 System Card](https://www.anthropic.com/document/claude-haiku-5-5-system-card)

Contradictory or limiting sources: None separately identified in this pass; this is not evidence of consensus.

Evidence notes: This summary does not assign suitability; exact benchmark records preserve conditions.

## Specifications

| Field | Recorded value |
|---|---|
| architecture | Unknown / not established |
| parameters | Unknown / not established |
| context window | 1000000 |
| maximum output | 128000 |
| modalities | input: text; image; output: text |
| language support | Multilingual; exact language inventory unknown |

Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.

## Access and cost

6 recorded access route(s); 4 model-specific price record(s).

[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)

Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.

## Licensing and local use

License: Proprietary commercial service terms

Restrictions: Commercial and consumer terms differ.; No weight redistribution license or exact-model fine-tuning offer located.

Commercial use: API use to power customer products subject to commercial terms and usage/region policies.

Redistribution: Unknown / not established

Hosted service: Permitted customer applications; resale requires approval under commercial terms.

Local weights/runtime availability: unknown

Hardware: Not established in this pass

Local conditions: No public weights/runtime located. Hosted API does not establish local inference.

## Gaps and caveats

- Launch-day evidence; most task-specific independent results and dated practitioner failure/fix reports remain unknown.
- Partner tariffs and account eligibility are not inferred from first-party prices.
- System card original is now inspected; setup is disclosed for several evaluations, but task-specific independent replication and serving-route comparability remain limited.
- Full bounded initial assessment; all required fields and tasks accounted for with investigated unknowns.
- Haiku 4.5 remains a separate model; its judgments and behavior were not transferred.

## Recorded price offers

| Provider | Tier / status | Rates | Conditions | Verified |
|---|---|---|---|---|
| anthropic | Standard / <=100k / current | input: 0.1 USD / per 1 million tokens; output: 0.5 USD / per 1 million tokens; cached_input: 0.01 USD / per 1 million tokens; cache_write_5m: 0.125 USD / per 1 million tokens; cache_write_1h: 0.2 USD / per 1 million tokens | Prompt <=100,000 tokens; Global routing at published base rates; US-only inference_geo us applies 1.1× to every token category. Server-side tools may add separate charges. | 2026-10-07 |
| anthropic | Standard / >100k / current | input: 0.5 USD / per 1 million tokens; output: 2.5 USD / per 1 million tokens; cached_input: 0.05 USD / per 1 million tokens; cache_write_5m: 0.625 USD / per 1 million tokens; cache_write_1h: 1 USD / per 1 million tokens | Prompt >100,000 tokens; Global routing at published base rates; US-only inference_geo us applies 1.1× to every token category. Server-side tools may add separate charges. | 2026-10-07 |
| anthropic | Batch / <=100k / current | input: 0.05 USD / per 1 million tokens; output: 0.25 USD / per 1 million tokens | Prompt <=100,000 tokens; Global routing at published base rates; US-only inference_geo us applies 1.1× to every token category. Server-side tools may add separate charges. | 2026-10-07 |
| anthropic | Batch / >100k / current | input: 0.25 USD / per 1 million tokens; output: 1.25 USD / per 1 million tokens | Prompt >100,000 tokens; Global routing at published base rates; US-only inference_geo us applies 1.1× to every token category. Server-side tools may add separate charges. | 2026-10-07 |

## Recorded access routes

- anthropic / Claude API: Active. Published Haiku 5.5 maxima for Start, Build and Scale respectively: 1,000/5,000/10,000 RPM; 2M/5M/10M input TPM; 0.4M/1M/2M output TPM. Evaluation/account settings may be lower; maxima are not guaranteed capacity.; Start/Build/Scale monthly spend caps are USD 500/USD 1000/USD 200000; workspace caps may be lower. US/global requests share one model rate pool.
- aws-bedrock / Amazon Bedrock Mantle: Active. Exact account quota, entitlement and negotiated conditions unknown.
- google-cloud / Gemini Enterprise Agent Platform: Active. Exact account quota, entitlement and negotiated conditions unknown.
- azure-foundry / Microsoft Foundry / Azure-hosted Claude: Active. Exact account quota, entitlement and negotiated conditions unknown.
- azure-foundry / Microsoft Foundry / Anthropic-hosted Claude: Active. Exact account quota, entitlement and negotiated conditions unknown.
- claude-platform-on-aws / Claude Platform on AWS: Active. Exact account quota, entitlement and negotiated conditions unknown.

## Sources

[Artificial Analysis Intelligence Benchmarking Methodology](https://artificialanalysis.ai/methodology/intelligence-benchmarking) · [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws) · [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing) · [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) · [Supported Regions Policy](https://www.anthropic.com/supported-countries) · [Haiku 5.5 prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5) · [Claude on google-cloud](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai) · [model versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions) · [Haiku 5.5 AWS launch](https://aws.amazon.com/blogs/machine-learning/introducing-claude-haiku-5-5-on-aws/) · [Claude prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) · [Haiku 5.5 Google Cloud model card](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude/haiku-5-5) · [Haiku 5.5 launch](https://www.anthropic.com/claude-haiku-5-5) · [Claude Haiku 5.5 overview](https://platform.claude.com/docs/en/models/haiku-5-5/overview) · [Launch-day prompting discussion](https://www.reddit.com/r/ClaudeAI/comments/1x06d3z/claude_haiku_55_official_prompting_guide/) · [Claude Haiku 5.5 medium evaluation](https://artificialanalysis.ai/models/claude-haiku-5-5-medium) · [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry) · [Haiku 5.5 migration guide](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide) · [Claude API rate limits](https://platform.claude.com/docs/en/api/rate-limits) · [Claude on aws-bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock) · [Haiku 5.5 classifier migration: hardest tickets and output recovery](https://www.ainews.tech/blog/haiku-5-5-classifier-drops-the-hardest-tickets) · [Claude Haiku 5.5: Polish-language original laboratory test](https://promptowy.com/claude-haiku-5-5/) · [Laboratorium Promptowe: independent Polish AI test methodology](https://promptowy.com/laboratorium-promptowego/) · [Polish writing arena and grading method](https://promptowy.com/arena-modeli-ai-po-polsku/) · [Haiku 5.5 versus DeepSeek V4.1 Flash on two application jobs](https://www.reddit.com/r/ClaudeAI/comments/1x0iu5x/haiku_55_vs_deepseek_v41_flash_on_my_2_boring/) · [Claude Haiku 5.5: invoice-policy classification hands-on test](https://www.datacamp.com/blog/claude-haiku-5-5) · [Claude Haiku 5.5 review: four editorial tasks](https://joinoasis.com/blog/claude-haiku-5-5-review) · [Legal summarization use-case guide](https://platform.claude.com/docs/en/about-claude/use-case-guides/legal-summarization) · [Claude current model overview](https://platform.claude.com/docs/en/models/overview) · [llmwise Haiku 5.5 writing task results](https://llmwise.ai/best-llm-for-writing) · [llmwise Haiku 5.5 summarization task results](https://llmwise.ai/best-llm-for-summarization) · [llmwise Haiku 5.5 translation task results](https://llmwise.ai/best-llm-for-translation) · [llmwise published prompt and Haiku output: announce a second bakery shop on linkedin](https://llmwise.ai/prompts/announce-a-second-bakery-shop-on-linkedin) · [llmwise published prompt and Haiku output: rewrite corporate jargon in plain words](https://llmwise.ai/prompts/rewrite-corporate-jargon-in-plain-words) · [llmwise published prompt and Haiku output: decline a meeting and offer two times](https://llmwise.ai/prompts/decline-a-meeting-and-offer-two-times) · [llmwise published prompt and Haiku output: a product announcement with five rules](https://llmwise.ai/prompts/a-product-announcement-with-five-rules) · [llmwise published prompt and Haiku output: argue both sides of free buses](https://llmwise.ai/prompts/argue-both-sides-of-free-buses) · [llmwise published prompt and Haiku output: an article in three bullets](https://llmwise.ai/prompts/an-article-in-three-bullets) · [llmwise published prompt and Haiku output: an email thread in one sentence](https://llmwise.ai/prompts/an-email-thread-in-one-sentence) · [llmwise published prompt and Haiku output: decisions and action items from a meeting](https://llmwise.ai/prompts/decisions-and-action-items-from-a-meeting) · [llmwise published prompt and Haiku output: a quarterly memo for the ceo](https://llmwise.ai/prompts/a-quarterly-memo-for-the-ceo) · [llmwise published prompt and Haiku output: a study with a negative result](https://llmwise.ai/prompts/a-study-with-a-negative-result) · [llmwise published prompt and Haiku output: a delivery message into spanish](https://llmwise.ai/prompts/a-delivery-message-into-spanish) · [llmwise published prompt and Haiku output: a product description into french](https://llmwise.ai/prompts/a-product-description-into-french) · [llmwise published prompt and Haiku output: a meeting note into german](https://llmwise.ai/prompts/a-meeting-note-into-german) · [llmwise published prompt and Haiku output: idioms into natural japanese](https://llmwise.ai/prompts/idioms-into-natural-japanese) · [llmwise published prompt and Haiku output: a lease clause into brazilian portuguese](https://llmwise.ai/prompts/a-lease-clause-into-brazilian-portuguese) · [llmwise fixed fifty-prompt test methods](https://llmwise.ai/our-test-runs) · [Claude Haiku 5.5 System Card](https://www.anthropic.com/document/claude-haiku-5-5-system-card) · [Can Haiku 5.5 take over Sonnet work? Original delegated-task test](https://www.agentcrew.cc/blog/posts/en/haiku-55-own-task-benchmark) · [FrontierSWE v2 leaderboard](https://www.frontierswe.com/) · [FrontierSWE v2](https://www.frontierswe.com/blog/v2) · [FrontierSWE changelog](https://www.frontierswe.com/changelog) · [Claude Haiku 5.5 vs Sonnet 4.6: An Everyday Benchmark](https://crazyrouter.com/en/blog/claude-haiku-5-5-vs-sonnet-4-6-everyday-benchmark-2026-en) · [Claude Haiku 5.5 Released: Pricing, Benchmarks, vs Haiku 4.5](https://computingforgeeks.com/claude-haiku-5-5-released-features-benchmarks/) · [Haiku 5.5 Coding Benchmark](https://aicodingdaily.com/model/haiku-5-5) · [LLM Coding Leaderboard: My Methodology and Scoring Formulas](https://aicodingdaily.com/article/llm-coding-leaderboard-my-methodology-and-scoring-formulas) · [FrontierCode public result data v 1.1](https://cognition.com/data/frontiercode-leaderboard/data.json) · [FrontierCode 1.1](https://cognition.com/blog/frontier-code-1.1) · [FrontierCode Leaderboard](https://cognition.com/frontiercode) · [Claude vs Gemini for math: exact Haiku 5.5 responses](https://llmwise.ai/claude-vs-gemini-for-math) · [Claude Haiku 5.5 Data Analytics Benchmark Results](https://plotly.com/blog/claude-haiku-5-5-plotly-data-analytics-bench/) · [Object Detection Benchmark](https://playground.roboflow.com/evals/object-detection) · [Vision Evals methodology](https://playground.roboflow.com/evals) · [Visual Reasoning Benchmark](https://playground.roboflow.com/evals/visual-reasoning) · [Object Counting Benchmark | Vision Evals](https://playground.roboflow.com/evals/object-counting) · [Report 014: Claude Haiku 5.5 on release day, three skills](https://driftproofhq.com/reports/014/) · [Driftproof Report 014 Haiku 5.5 review run 1 receipt](https://driftproofhq.com/reports/014/evidence/run-1/code-review-and-quality-claude-haiku-5-5-2026-10-07.json) · [Small controlled Haiku 5.5 coding-agent test](https://www.reddit.com/r/ClaudeCode/comments/1x132yy/is_haiku_55_good_enough_to_be_your_main_coding/) · [Claude Haiku 5.5 max evaluation](https://artificialanalysis.ai/models/claude-haiku-5-5) · [Agent Platform Pricing](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing) · [AWS Price List: Amazon Bedrock Foundation Models, us-gov-west-1, version 20261008165109](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonBedrockFoundationModels/20261008165109/us-gov-west-1/index.json) · [Claude Haiku 5.5 - Amazon Bedrock](https://docs.aws.amazon.com/us_en/bedrock/latest/userguide/model-card-anthropic-claude-haiku-5-5.html)
