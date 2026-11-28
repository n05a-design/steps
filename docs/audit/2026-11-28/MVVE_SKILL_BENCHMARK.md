# MVVE V2.1 skill benchmark protocol

All arms are **NOT_RUN**. The local deterministic knowledge run and unfilled review templates document preparation. They contain no model answers or human ratings.

| Arm | Access | Result |
| --- | --- | --- |
| A | Neutral system prompt | NOT_RUN |
| B | A plus the selected STEPS skill revision | NOT_RUN |
| C | B plus read-only retrieval from the approved KnowledgeAdapter scope | NOT_RUN |
| D | C plus audited, read-only STEPS theory and analysis functions | NOT_RUN |

Use the twelve published COACH questions for calibration. The reviewer holds a distinct scored set outside the model and skill prompts. Cover pitch register, enharmonic spelling, inversion, ambiguous recognition, tonicization, borrowed chords, altered extensions, rhythm, evidence and abstention. Hash the question file and independent key before model execution. The key records expected outcomes, allowable alternatives and an actionable source locator for each source claim. [Existing questions and rubrics](../../../knowledge/benchmark/cases.json)

Freeze provider and model revision, system prompt versions, allowed tools, decoding parameters, optional seed, output limits, repeat count, test order and total cost ceiling. Use fresh context per case and the same conditions for all four arms. Use the same clean STEPS SHA and approved content for the tool-connected arms. Model access and the spend limit require owner approval before execution.

Record question ID, frozen question-set hash, arm, repeat, model, settings, start time, original answer, citations, tool calls, usage, failures and duration. Retain all responses and explicit timeouts. The case reviewer should be blind to the arm. Use distinct files from the review-template exporter for arm and repeat, and aggregate only after applying case-level mandatory criteria. [Benchmark forms and commands](../../../knowledge/benchmark/README.md)

Evaluate factual correctness, coverage of the question, register and notation, explanation quality, source validity, plausible alternatives, appropriate abstention, unsupported claims, repeatability and cost. Report matched-case differences A→B, B→C and C→D with denominators and missing cases. Release approval remains independent.
