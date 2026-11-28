# Independent knowledge and skill validation

The canonical benchmark holds 119 cases. The last V2.2 result reported 92 PASS, zero FAIL and the following 27 PENDING. Use the case definitions and the review template for the target commit. [Canonical cases and rubrics](../../../knowledge/benchmark/cases.json) · [German practical review packets](MVVE_FACHABNAHME.md)

| Responsible reviewer | Pending | Case IDs and evidence |
| --- | ---: | --- |
| Archive custodian and rights reviewer | 10 | KB-HISTORY-F00412, KB-HISTORY-F00571, KB-HISTORY-F00704, KB-HISTORY-F00768, KB-HISTORY-F00937, KB-HISTORY-F01002, KB-HISTORY-PPR-MIDI-01, KB-HISTORY-PPR-MIDI-02, KB-HISTORY-PPR-MIDI-03, KB-HISTORY-PPR-MIDI-04. Match each original to its registered digest. Record any alternate edition and archive decision. Obtain publication or usage clearance separately. |
| Independent musician or teacher | 3 | KB-M08-METER checks independently located accents and bar boundaries. KB-M12-PLAYABILITY checks span, fingering and tempo in a play test. KB-M09-LOOP-HEAR compares the documented hearing of two phrasings of the same chord loop. |
| Source curator | 1 | KB-SRC-033-PROVENANCE requires author, work, locator and applicability of the four-family claim. |
| Knowledge graph curator with a domain reviewer | 1 | KB-GRAPH-NODES requires independent locators for unresolved historical endpoints and a traceable claim or source for relations. |
| Benchmark operator and independent assessor | 12 | COACH-01, COACH-02, COACH-03, COACH-04, COACH-05, COACH-06, COACH-07, COACH-08, COACH-09, COACH-10, COACH-11, COACH-12. Collect genuine outputs and score the required criteria and checked sources. |

Benchmark manual approval requires the exact Git SHA and case fingerprint, named review, evidence and observations. A later commit makes the earlier manual evidence pending. Coach benchmark assessment uses the case fingerprint and genuine response with model, Skill revision, source and run evidence. The Coach benchmark does not impose a separate exact HEAD check on that assessment. Musical release reviews use a different gate and bind the GitHub evidence comment to the exact PR head or merged revision. The existing pilot claim fingerprints also bind source records and claim content. Freeze the candidate before requesting reviews and keep superseded evidence. [Musical release acceptance](../../governance/MUSICAL_RELEASE_ACCEPTANCE.md)

## Separately authorized experiment

Run the original matched A/B/C/D design. A gets a neutral prompt. B adds the frozen STEPS Skill. C adds approved read-only KnowledgeAdapter retrieval. D adds the audited read-only theory and analysis functions. Use the published twelve cases for calibration and the independently scored holdout separately. Freeze model revision, provenance, settings, repetition count, task order, resource ceiling and tool access. Require genuine responses, source checks, case-level scoring and reviewer independence. Record failures, missing outcomes and denominators per arm. The planned arms remain NOT_RUN until the operator has model access and budget and the assessor is assigned. [Original protocol and recording fields](MVVE_SKILL_BENCHMARK.md)
