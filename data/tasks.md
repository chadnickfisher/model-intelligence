# Task rubric

Generated from [canonical task definitions](capability-taxonomy.yaml). Rubric 1.0 defines claim boundaries; it does not reclassify earlier judgments.

Cost, provider, modality, effort and harness remain explicit operating conditions. Absence of evidence is unknown, not exclusion.

## coding.scoped_edit — Coding: scoped edit

Implement a bounded code change with a specified goal and a localized acceptance criterion.

Include:

- Add or change a specific function, endpoint, or component to meet stated behavior.
- Evaluate correctness of the requested change and preservation of relevant existing behavior.

Exclude from this task:

- Fault diagnosis belongs to coding.debugging when locating the cause is the measured work.
- Broad repository coordination or system design requires its own task evidence.

Examples:

- Add pagination to an existing endpoint with specified ordering and page limits.

Neighboring tasks: coding.debugging, coding.refactoring, coding.repository_work

## coding.debugging — Coding: debugging

Diagnose a concrete software failure, identify its cause, and assess a corrective change.

Include:

- Trace failing behavior through code, logs, or a reproducible test to a supported cause.
- Check that a proposed repair addresses the failure under the recorded setup.

Exclude from this task:

- Implementing a supplied repair without diagnosis is a scoped edit.
- Reporting suspicious code without investigating a failure is code review.

Examples:

- Find why an empty input crashes a parser and verify a repair against the reproduction.

Neighboring tasks: coding.scoped_edit, coding.tests, coding.review

## coding.architecture — Coding: architecture

Design software structure and interfaces while reasoning about requirements and system tradeoffs.

Include:

- Propose component boundaries, data flows, or interfaces for stated system requirements.
- Explain consequences of design choices for maintenance, reliability, or scalability.

Exclude from this task:

- A local implementation change does not itself establish system design ability.
- General logical puzzles without software design requirements belong to reasoning.general.

Examples:

- Design a job queue with retry boundaries, idempotency, and failure isolation.

Neighboring tasks: coding.refactoring, coding.repository_work, reasoning.general

## coding.refactoring — Coding: refactoring

Restructure existing code while preserving its specified externally observable behavior.

Include:

- Remove duplication, reorganize modules, or simplify implementation without changing the contract.
- Assess behavior preservation through relevant checks or explicit invariants.

Exclude from this task:

- A requested new feature or behavior change is a scoped edit even when restructuring accompanies it.
- Proposing a design without restructuring existing code is architecture work.

Examples:

- Extract shared validation from three handlers while keeping responses and errors stable.

Neighboring tasks: coding.scoped_edit, coding.architecture, coding.tests

## coding.tests — Coding: tests

Develop or improve software tests that meaningfully distinguish correct from incorrect behavior.

Include:

- Select representative inputs, edge cases, and assertions for a specified software contract.
- Assess whether tests detect relevant faults and avoid misleading passes.

Exclude from this task:

- Merely running an existing suite does not measure test design.
- Diagnosing the underlying application defect is debugging when that is the task outcome.

Examples:

- Write regression tests for retry exhaustion, successful recovery, and duplicate delivery.

Neighboring tasks: coding.debugging, coding.review, coding.scoped_edit

## coding.review — Coding: review

Inspect code or a proposed change and produce actionable, supported findings about its risks or defects.

Include:

- Identify concrete correctness, security, or maintenance problems in the reviewed code.
- Explain a finding's trigger and impact with evidence from the change and relevant context.

Exclude from this task:

- Stylistic preference alone does not establish defect detection.
- Implementing repairs or independently tracing a reported failure requires separate task evidence.

Examples:

- Review an authorization change and identify a path that exposes another user's record.

Neighboring tasks: coding.debugging, coding.tests, coding.repository_work

## coding.repository_work — Coding: repository work

Coordinate a software change across an existing repository's files, dependencies, conventions, and checks.

Include:

- Navigate relevant repository context and integrate mutually dependent changes.
- Keep implementation, configuration, tests, and documentation consistent with the requested outcome.

Exclude from this task:

- An isolated function exercise does not measure repository integration.
- Duration alone does not make repository work a long-horizon agent task.

Examples:

- Update an API contract across server code, client types, tests, and migration documentation.

Neighboring tasks: coding.scoped_edit, coding.architecture, agent.long_horizon

## coding.frontend — Coding: frontend

Build or modify user-facing software interfaces, including layout, interaction, and rendering behavior.

Include:

- Implement usable interface components and interactions under the stated design requirements.
- Evaluate visual layout, responsiveness, accessibility, or interaction correctness as documented.

Exclude from this task:

- Visual preference evidence does not establish production correctness or accessibility.
- Generating an interface illustration without functional code belongs to image.generation.

Examples:

- Implement a responsive search page with keyboard navigation and loading and error states.

Neighboring tasks: coding.scoped_edit, coding.tests, image.generation

## agent.long_horizon — Agent: long horizon

Maintain progress toward a goal through multiple dependent actions, intermediate results, and plan revisions.

Include:

- Track constraints and unfinished work across a sequence whose next steps depend on earlier outcomes.
- Adapt a plan after feedback or setbacks and verify the final goal state.

Exclude from this task:

- A single tool call or a long answer does not measure sustained agent execution.
- Large supplied input alone belongs to context tasks rather than long-horizon agency.

Examples:

- Investigate a repository issue, implement a repair, resolve failing checks, and verify the complete change.

Neighboring tasks: agent.tool_use, coding.repository_work, context.reasoning

## agent.tool_use — Agent: tool use

Select and invoke external tools with valid arguments, then use their results to complete a task.

Include:

- Choose appropriate available tools and supply arguments consistent with their contracts.
- Interpret tool responses, handle documented errors, and connect results to the requested outcome.

Exclude from this task:

- Describing a hypothetical tool call without execution does not measure tool execution.
- Visual GUI navigation belongs to computer use when that interaction is the measured task.

Examples:

- Query a structured catalog and use the returned route and price records to answer a constrained request.

Neighboring tasks: agent.computer_use, agent.long_horizon, knowledge.rag

## agent.computer_use — Agent: computer use

Operate a graphical interface by interpreting its visible state and performing appropriate interactions.

Include:

- Navigate pages or applications through controls such as clicks, typing, and scrolling.
- Verify interface state changes and recover from interaction failures within the measured setup.

Exclude from this task:

- Calling a structured API without GUI interaction is tool use.
- Identifying a control in a static screenshot alone is visual grounding.

Examples:

- Fill a browser form, correct a validation error, and confirm the saved result in the interface.

Neighboring tasks: agent.tool_use, vision.grounding, agent.long_horizon

## reasoning.general — Reasoning: general

Derive a justified answer from logical relationships, constraints, or causal premises outside specialized tasks.

Include:

- Solve a stated constraint or inference problem using the supplied premises.
- Assess consistency and explain the reasoning steps relevant to the answer.

Exclude from this task:

- Mathematical derivations and scientific inference have their own specialized task definitions.
- Recalling a fact or satisfying formatting constraints alone does not establish logical reasoning.

Examples:

- Determine a feasible schedule from availability constraints and explain why alternatives conflict.

Neighboring tasks: reasoning.math, reasoning.scientific, context.reasoning

## reasoning.math — Reasoning: math

Solve mathematical problems through quantitative derivation, calculation, proof, or formal argument.

Include:

- Derive numerical or symbolic results while respecting assumptions and mathematical constraints.
- Construct or evaluate a proof or a mathematical solution's validity.

Exclude from this task:

- Extracting a number from supplied text is retrieval or extraction unless derivation is required.
- Scientific interpretation of a computed result requires separate scientific reasoning evidence.

Examples:

- Prove an inequality under stated bounds and identify when equality holds.

Neighboring tasks: reasoning.general, reasoning.scientific, knowledge.extraction

## reasoning.scientific — Reasoning: scientific

Apply scientific concepts and evidence to explain phenomena, evaluate hypotheses, or interpret experiments.

Include:

- Reason about mechanisms, experimental controls, or conclusions supported by scientific observations.
- Distinguish evidence, assumptions, uncertainty, and competing explanations in a scientific problem.

Exclude from this task:

- Mathematical calculation alone does not establish scientific interpretation.
- Combining paper summaries without evaluating scientific reasoning is research synthesis.

Examples:

- Explain whether an experiment separates a treatment effect from a confounding variable.

Neighboring tasks: reasoning.math, research.synthesis, research.fact_check

## research.fact_check — Research: fact check

Verify a specific factual claim against attributable sources and report the supported conclusion and uncertainty.

Include:

- Inspect source identity, date, and relevance to the exact claim being checked.
- Reconcile supporting and conflicting sources or state that the claim remains unresolved.

Exclude from this task:

- A sourced overview without adjudicating a specific claim is research synthesis.
- Fluent unsupported recall does not measure source-based verification.

Examples:

- Check whether a published product limit applies to a named version on the stated date.

Neighboring tasks: research.synthesis, knowledge.rag, language.summarization

## research.synthesis — Research: synthesis

Combine multiple relevant sources into a grounded account of their findings, relationships, and disagreements.

Include:

- Integrate distinct sources around a research question while preserving attribution and source conditions.
- Explain areas of agreement, conflicting findings, and unresolved gaps across the sources.

Exclude from this task:

- Condensing a single supplied document is summarization unless cross-source synthesis is measured.
- Verifying one isolated proposition is fact checking rather than evidence integration.

Examples:

- Compare several studies of an intervention while retaining their populations and measurement differences.

Neighboring tasks: research.fact_check, language.summarization, reasoning.scientific

## language.writing — Language: writing

Compose or revise prose to meet a communicative purpose, audience, tone, and structure.

Include:

- Produce clear, coherent prose appropriate to the requested genre and audience.
- Revise wording or organization while preserving the intended meaning and constraints.

Exclude from this task:

- Fidelity in condensing source material is primarily summarization.
- Quality in transferring meaning between languages is translation.

Examples:

- Rewrite a technical explanation for a general audience while keeping its essential caveats.

Neighboring tasks: language.summarization, language.instruction_following, language.translation

## language.summarization — Language: summarization

Condense supplied material while preserving its essential meaning, qualifications, and attribution.

Include:

- Select salient content for the requested summary length and purpose.
- Preserve important limitations and avoid adding claims absent from the source.

Exclude from this task:

- Gathering and integrating independent sources is research synthesis when that is the measured work.
- Returning specified fields without an overview is knowledge extraction.

Examples:

- Summarize a meeting transcript with decisions, unresolved issues, and assigned actions.

Neighboring tasks: language.writing, research.synthesis, knowledge.extraction

## language.instruction_following — Language: instruction following

Satisfy explicit task instructions and output constraints while resolving their stated priority and dependencies.

Include:

- Follow requested content, formatting, ordering, or exclusion constraints that can be assessed directly.
- Maintain multiple compatible instructions throughout the response or task.

Exclude from this task:

- Correct format alone does not establish factual accuracy or competence in the requested domain.
- Generic praise for helpfulness does not identify an instruction-following task outcome.

Examples:

- Return exactly three labeled items in a specified order while respecting a word limit for each.

Neighboring tasks: language.writing, knowledge.extraction, agent.long_horizon

## language.translation — Language: translation

Transfer supplied meaning from one language to another while preserving relevant register and nuance.

Include:

- Translate text with attention to semantic fidelity, idioms, terminology, and audience.
- Evaluate source-to-target meaning preservation for the stated language pair.

Exclude from this task:

- Open-ended conversation in another language is multilingual chat unless translation is requested.
- Transcribing spoken words into the same language is audio understanding.

Examples:

- Translate a formal customer notice into Spanish while preserving its conditions and polite register.

Neighboring tasks: language.multilingual_chat, language.writing, audio.understanding

## language.multilingual_chat — Language: multilingual chat

Conduct contextually appropriate dialogue in one or more languages across conversational turns.

Include:

- Understand and respond coherently in the evaluated language or code-switching setup.
- Maintain conversational context, register, and relevant cultural or linguistic distinctions.

Exclude from this task:

- Translating fixed source text is translation rather than open-ended dialogue.
- Speech timing and interruption handling belong to audio conversation when measured.

Examples:

- Answer follow-up support questions in French while retaining details established earlier in the chat.

Neighboring tasks: language.translation, audio.conversation, language.instruction_following

## knowledge.extraction — Knowledge: extraction

Identify and return specified facts, entities, or relationships from supplied material in a requested structure.

Include:

- Map source content to requested fields while preserving values and relationships.
- Represent ambiguous or missing values explicitly under the task's extraction contract.

Exclude from this task:

- Assigning a category to an item is classification when category choice is the measured outcome.
- Finding dispersed facts in an extended context is context retrieval when placement or length is central.

Examples:

- Extract invoice dates, vendors, totals, and currencies into records without inventing missing amounts.

Neighboring tasks: knowledge.classification, context.retrieval, language.summarization

## knowledge.classification — Knowledge: classification

Assign supplied items to defined categories using their content and the stated category criteria.

Include:

- Choose labels for examples under a documented taxonomy or decision rule.
- Assess distinctions between neighboring labels and handling of ambiguous cases.

Exclude from this task:

- Copying an existing label from a source is extraction rather than classification.
- Inventing a new taxonomy is outside classification under a supplied category set.

Examples:

- Label support tickets as billing, access, or technical issues using the supplied definitions.

Neighboring tasks: knowledge.extraction, language.instruction_following, reasoning.general

## knowledge.rag — Knowledge: rag

Answer a question using evidence retrieved from an external corpus within a documented retrieval workflow.

Include:

- Use retrieved passages or records to ground an answer and preserve their source attribution.
- Assess retrieval relevance and answer support under the measured corpus, retriever, and context setup.

Exclude from this task:

- Locating facts already supplied in a prompt is context retrieval unless external retrieval is part of the task.
- A cited answer without a documented retrieval workflow does not establish RAG performance.

Examples:

- Answer a policy question from retrieved handbook sections and identify which section supports each condition.

Neighboring tasks: context.retrieval, research.fact_check, agent.tool_use

## context.retrieval — Context: retrieval

Locate and accurately recover relevant information from extended supplied context across its positions and distractions.

Include:

- Find a requested fact or passage whose placement, context length, or competing content matters to the task.
- Assess retrieval accuracy under the documented input length and information distribution.

Exclude from this task:

- Deriving a conclusion across retrieved facts is context reasoning when integration is required.
- Retrieving from a separate corpus belongs to knowledge.rag under its retrieval workflow.

Examples:

- Find an exception clause buried in a long supplied policy alongside similar but inapplicable clauses.

Neighboring tasks: context.reasoning, knowledge.extraction, knowledge.rag

## context.reasoning — Context: reasoning

Integrate relationships or constraints distributed across extended supplied context to derive an answer.

Include:

- Combine information from multiple parts of the input rather than merely retrieving a matching passage.
- Assess derived conclusions under the recorded context length, placement, and dependency structure.

Exclude from this task:

- Repeating a single located fact is context retrieval.
- An advertised context window size alone does not establish reasoning across that window.

Examples:

- Determine which contract deadline applies by combining amendments and exceptions spread across the input.

Neighboring tasks: context.retrieval, reasoning.general, research.synthesis

## vision.question_answering — Vision: question answering

Answer questions about visual input by interpreting visible objects, text, relationships, or diagrams.

Include:

- Derive an answer from image content relevant to the question.
- Evaluate interpretation under the documented image resolution and visual complexity.

Exclude from this task:

- Producing explicit coordinates or regions is visual grounding when localization is the required output.
- Creating or modifying image pixels belongs to image generation or editing.

Examples:

- Explain which series increased most in a supplied chart and cite its visible values.

Neighboring tasks: vision.grounding, knowledge.extraction, reasoning.scientific

## vision.grounding — Vision: grounding

Localize a described visual entity or interface element to a region, coordinate, or other explicit visual reference.

Include:

- Match a description to the correct location in an image or screenshot.
- Assess localization precision against the specified spatial output format or target region.

Exclude from this task:

- Describing an image without locating a target is visual question answering.
- Completing an interface workflow through interactions requires computer-use evidence.

Examples:

- Return the bounding box of the search field in a screenshot containing several similar controls.

Neighboring tasks: vision.question_answering, agent.computer_use, image.editing

## image.generation — Image: generation

Create a still image from a requested description or reference-based composition brief.

Include:

- Generate a new composition that follows specified subjects, relationships, style, or visible text.
- Evaluate output fidelity and visual quality under the documented generation settings.

Exclude from this task:

- A targeted alteration with preservation requirements for an existing image is image editing.
- Generating temporal motion across frames belongs to video generation.

Examples:

- Generate an illustrated poster with three specified objects and a requested title.

Neighboring tasks: image.editing, video.generation, coding.frontend

## image.editing — Image: editing

Modify an existing still image while satisfying requested changes and preserving specified source content.

Include:

- Apply localized or global changes such as object replacement, recoloring, or background transformation.
- Assess both the requested edit and preservation of identity, geometry, or unaffected regions as specified.

Exclude from this task:

- Creating a new composition without source preservation criteria is image generation.
- Editing a clip with temporal consistency requirements belongs to video editing.

Examples:

- Replace a product photo's background while retaining the product's shape and printed label.

Neighboring tasks: image.generation, video.editing, vision.grounding

## audio.understanding — Audio: understanding

Interpret supplied audio to recover speech, events, speaker information, or other audible meaning.

Include:

- Transcribe speech or answer questions grounded in audible content.
- Identify sound events, speaker turns, or paralinguistic information under the stated recording conditions.

Exclude from this task:

- Producing speech audio is speech generation rather than audio interpretation.
- Interactive voice turn management requires audio-conversation evidence.

Examples:

- Transcribe a recorded discussion and identify which speaker agreed to each action.

Neighboring tasks: audio.conversation, audio.speech_generation, language.translation

## audio.speech_generation — Audio: speech generation

Produce intelligible spoken audio with requested verbal content, voice characteristics, or delivery.

Include:

- Render requested speech with assessable pronunciation, prosody, or voice consistency.
- Evaluate verbal fidelity and audio quality under the stated generation setup.

Exclude from this task:

- Understanding a recording without generating speech belongs to audio understanding.
- Musical composition or singing assessed as music belongs to music generation.

Examples:

- Speak a supplied announcement with clear numbers, natural pauses, and the requested tone.

Neighboring tasks: audio.conversation, audio.understanding, music.generation

## audio.conversation — Audio: conversation

Sustain interactive spoken dialogue through listening, responding, timing, and management of voice turns.

Include:

- Maintain dialogue context while interpreting spoken input and generating relevant spoken responses.
- Assess response timing, interruption handling, and turn continuity when documented in the setup.

Exclude from this task:

- A standalone transcription or narration task does not measure interactive conversation.
- Text-only multilingual dialogue belongs to multilingual chat.

Examples:

- Conduct a voice support exchange, handle an interruption, and resume with the corrected request.

Neighboring tasks: audio.understanding, audio.speech_generation, language.multilingual_chat

## video.generation — Video: generation

Create a video sequence from a prompt or conditioning inputs with requested motion and temporal content.

Include:

- Generate moving scenes that follow subject, action, camera, or continuity requirements.
- Evaluate temporal consistency and any requested synchronized audio under the documented output setup.

Exclude from this task:

- Targeted modifications to an existing source clip with preservation requirements are video editing.
- A still image's visual quality alone does not establish motion generation ability.

Examples:

- Generate a short clip of a cyclist turning a corner while preserving subject identity across frames.

Neighboring tasks: video.editing, image.generation, audio.speech_generation

## video.editing — Video: editing

Modify an existing video while preserving specified source content and consistency across time.

Include:

- Change clip content, appearance, timing, or composition according to an explicit edit request.
- Assess preservation of unaffected content and continuity of the edit across relevant frames.

Exclude from this task:

- Generating a new sequence without clip-preservation requirements is video generation.
- Altering a single still frame alone does not establish temporally consistent video editing.

Examples:

- Remove a background object throughout a moving shot while preserving the foreground subject.

Neighboring tasks: video.generation, image.editing, vision.grounding

## music.generation — Music: generation

Create musical audio with requested melodic, rhythmic, structural, instrumental, or vocal characteristics.

Include:

- Generate a composition or musical performance matching the supplied brief.
- Assess musical coherence, requested structure, and audio quality under the measured setup.

Exclude from this task:

- Spoken narration without musical composition is speech generation.
- Recognizing an instrument or transcribing existing audio is audio understanding.

Examples:

- Generate an instrumental piece with a specified tempo, instrumentation, and contrasting second section.

Neighboring tasks: audio.speech_generation, audio.understanding, video.generation

