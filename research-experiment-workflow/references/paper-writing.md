<!-- Adapted from Master-cai/Research-Paper-Writing-Skills (MIT License). See references/paper-writing-attribution.md. -->

Source upstream path: `research-paper-writing/SKILL.md`.

# Paper Writing Workflow

## Contents

- Overview
- Core Workflow
- Global Principles
- Paragraph Clarity Check (Important)
- Section Guides
- Paper Review Core Points
- Execution Rules
- Output Contract
- Evidence-Gate Override


## Overview

Use this reference when drafting, rewriting, or reviewing paper text inside the research-experiment workflow. Prioritize first-impression quality (figures/tables/layout), logical flow, and claims backed by saved artifacts, analyses, or citations. The research workflow evidence gates override writing fluency: if a claim lacks support, weaken it, mark it as an evidence gap, or remove it.

## Core Workflow

1. Clarify the paper story before sentence-level edits.
2. Use section-specific guidance in `references/`.
3. Rewrite paragraph-by-paragraph with one message per paragraph.
4. Run reverse outlining after writing each section.
5. Check every major claim in Abstract/Introduction against experimental evidence.
6. Run final-paper adversarial review with `references/paper-writing-review.md`.
7. Preserve the claim-to-evidence map required by `references/artifact-contract.md`.

## Global Principles

1. Keep one paragraph for one message only.
2. State the paragraph message in the first sentence.
3. Make nouns self-contained; define new terms before reusing them.
4. Maintain sentence-to-sentence flow (cause, contrast, consequence, or refinement).
5. Iterate with adversarial self-review: read as a skeptical reviewer.
6. Treat visual quality as core content, not decoration.
7. Use a clean teaser and pipeline figure.
8. Use readable, minimal-ink tables.
9. Keep formatting consistent and tidy.

## Paragraph Clarity Check (Important)

Use this quick test whenever the user asks whether a paragraph "flows" or is clear.

1. Read as an external reader:
   - Does this paragraph have one explicit message?
   - Does the first sentence state what this paragraph will do?
   - Are all key nouns/terms readable without hidden context?
   - Does each sentence connect to the previous one with a clear relation (cause, contrast, consequence, refinement, example)?
2. Run reverse outlining for the current section:
   - Write down thesis/main claim.
   - Write down each paragraph topic sentence.
   - Write down the evidence/explanation points under each paragraph.
   - Check mapping: topic sentence -> thesis, and evidence -> topic sentence.
   - Revise or remove any paragraph that cannot be mapped cleanly.
3. If flow is still weak, add temporary section headers and explicit transition phrases during revision, then remove unnecessary headers before finalizing.

Source reference for this check:

- `references/paper-writing-flow.md`

## Section Guides

Load only the needed section file:

- Introduction: `references/paper-writing-introduction.md`
- Abstract: `references/paper-writing-abstract.md`
- Related Work: `references/paper-writing-related-work.md`
- Method: `references/paper-writing-method.md`
- Experiments: `references/paper-writing-experiments.md`
- Conclusion: `references/paper-writing-conclusion.md`
- Paper review (Paper Review): `references/paper-writing-review.md`
- Paragraph clarity source: `references/paper-writing-flow.md`
- Example bank index: `references/paper-writing-examples-index.md`

## Paper Review Core Points

Use `references/paper-writing-review.md` for the full checklist and workflow.

1. Add an end-of-draft self-review question list in five dimensions:
   - contribution,
   - writing clarity,
   - experimental strength,
   - evaluation completeness,
   - method design soundness.
2. Treat claim-evidence alignment as a hard constraint, especially for Abstract and Introduction.
3. Perform adversarial writing: review as a skeptical reviewer and resolve every high-risk question.
4. Revise until major rejection risks are explicitly addressed.

## Execution Rules

1. Build a mini-outline before drafting prose.
2. For each subsection, explicitly include motivation, design, and technical advantage when applicable.
3. Avoid writing style that looks like incremental patching of a naive baseline.
4. Keep terminology stable across the full paper.
5. If a claim cannot be supported by results, weaken or remove the claim.
6. Before finalizing, append and answer a five-dimension self-review question list, then revise the paper based on unresolved items.
7. Do not load all section references (Introduction/Abstract/Related Work/Method/Experiments/Conclusion) at once; load only the specific section guide needed for the current edit target.

## Output Contract

When asked to rewrite or draft sections, save or return:

1. A compact section outline (3-7 bullets).
2. Revised paragraphs with explicit paragraph roles (opening/challenge/method/advantage/evidence/limitation).
3. A short self-review checklist covering clarity, flow, terminology consistency, unsupported claims, and missing evidence.
4. A claim-evidence map for each major claim in the revised text using `Claim: ... | Evidence: ... | Status: supported/needs evidence`.

## Evidence-Gate Override

1. Treat every quantitative, comparative, novelty, and causal statement as unsupported until it points to an experiment ID, analysis artifact, figure, table, or citation.
2. If evidence is missing, keep the prose draftable but label the claim `needs evidence` in the claim-evidence map.
3. Do not let a smoother narrative hide failed runs, discarded runs, negative results, missing baselines, weak ablations, or novelty uncertainty.
4. For paper-facing work, use the Writer role after Analyst output and use the Reviewer role before presenting text as final.
