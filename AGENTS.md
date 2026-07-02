# AGENTS.md — Research Experiment Workflow Skill Repository

This repository publishes a reusable Codex skill: `research-experiment-workflow`.

The root documentation is for humans who install or maintain the skill. The `research-experiment-workflow/` directory is the skill package that Codex loads.

## Mission And Scope

- Maintain a compact, reusable skill for artifact-gated research, machine learning, and paper-oriented experiments.
- Keep the skill generic across projects. Do not hardcode one lab, dataset, framework, model, benchmark, paper, or repository into the skill instructions.
- Preserve the core workflow: idea scoring, hypothesis, novelty check, feasibility, pilot, experiment run, review, analysis, and writing.
- Optimize for evidence discipline: durable artifacts, explicit gates, baseline-first comparisons, pilot-first execution, and claims traceable to files.

## Repository Layout

- `research-experiment-workflow/SKILL.md`: required skill entrypoint, frontmatter, stage router, and concise operating rules.
- `research-experiment-workflow/references/artifact-contract.md`: artifact schemas, compact templates, review rubric, writing checks, and cross-project adaptation guidance.
- `research-experiment-workflow/references/roles.md`: role model for multi-agent, delegated, or role-scoped research work.
- `research-experiment-workflow/agents/openai.yaml`: UI metadata and default prompt.
- `README.md`: English public-facing README.
- `README.zh-CN.md`: Simplified Chinese public-facing README.
- `AGENTS.md`: repository maintenance instructions for agentic coding tools.
- `CLAUDE.md`: short pointer to this file for Claude Code.

Do not add root maintenance files inside `research-experiment-workflow/`. The skill package should contain only files that directly support skill execution.

## Context Loading Order

When maintaining this repository, load context in this order:

1. `AGENTS.md`
2. `research-experiment-workflow/SKILL.md`
3. Relevant files in `research-experiment-workflow/references/`
4. `research-experiment-workflow/agents/openai.yaml` when UI metadata or default prompts change
5. `README.md` and `README.zh-CN.md` when public documentation changes

Do not assume hidden workflow loading. All maintenance rules that matter should be visible in repository files.

## Skill Design Rules

- Keep `SKILL.md` concise. It should route tasks, define gates, and link to references. Put detailed templates and role guidance in `references/`.
- Use progressive disclosure: only add a reference file when it helps a triggered task and can be loaded conditionally.
- Keep reference files one level below `references/`; avoid deep reference chains.
- Do not add `README.md`, tutorials, changelogs, installation guides, or marketing copy inside the skill package directory.
- Do not duplicate the same long guidance in both `SKILL.md` and a reference file.
- Keep the skill human-supervised. Do not present it as a fully automated scientist, paper generator, reviewer, or source of ground truth.
- Keep project-specific commands, metrics, datasets, and environment assumptions in each downstream project, not in this generic skill.

## Public Documentation Rules

- `README.md` is the primary English README.
- `README.zh-CN.md` is the Simplified Chinese README.
- Keep the language switch lightweight: each README should link to the other language at the top, without extra language-section headings.
- When changing install instructions, examples, workflow names, or repository structure, update both READMEs in the same commit.
- README content is for users; skill execution instructions belong in `SKILL.md` or `references/`.

## Validation

After any change to the skill package, run:

```bash
python /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py research-experiment-workflow
```

If the system skill validator path is unavailable, run the equivalent validator from the local Codex skill-creator installation and record what was used.

Before committing, also check:

```bash
git status --short
rg -n "sk-|gho_|API_KEY|TOKEN|password|secret" . -g '!AGENTS.md'
```

The secret scan is a lightweight guardrail, not a substitute for judgment.

## Editing Rules

- Preserve the skill folder name: `research-experiment-workflow`.
- Preserve required skill frontmatter fields: `name` and `description`.
- If `SKILL.md` trigger behavior changes, review `agents/openai.yaml` and update the default prompt if stale.
- If roles change, update `references/roles.md`; keep only a short loading rule in `SKILL.md`.
- If artifact schemas or templates change, update `references/artifact-contract.md` and consider whether README examples still match.
- Prefer small, focused commits with clear messages.

## Release And GitHub Workflow

Typical release flow:

```bash
python /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py research-experiment-workflow
git status --short
git add <changed-files>
git commit -m "<concise message>"
git push
```

Do not rewrite public history unless the user explicitly asks for it. If a push fails because Git uses the wrong SSH identity, prefer switching this repository's remote to HTTPS and using `gh auth setup-git` rather than changing global SSH configuration.

## License And Safety

- This repository currently has no open-source license unless a `LICENSE` file is added. Do not imply reuse rights beyond what the repository explicitly grants.
- Do not commit tokens, private endpoints, local machine paths that expose secrets, unpublished paper data, or private experiment results.
- Keep examples generic and safe to share publicly.

## Maintenance Philosophy

This repository should stay small. Add rules or files only when they prevent real misuse, reduce repeated maintenance work, or make the skill easier to apply correctly across projects.
