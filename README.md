# Research Experiment Workflow Skill

Language: [English](#english) | [中文](#中文)

<a id="english"></a>
## English

`research-experiment-workflow` is a Codex skill for turning research, machine learning, and paper-oriented experiments into an auditable artifact chain.

Its core rule is simple: record ideas and hypotheses first, then run novelty checks, feasibility checks, pilots, full experiments, review, analysis, and only then draft paper or report text. Each stage should leave durable files that can be resumed, reviewed, and reused.

### When To Use

- Turn a research idea into a falsifiable hypothesis.
- Set up an experiment directory and artifact contract for a new project.
- Design a pilot before full training or expensive runs.
- Check risks around baselines, metrics, data leakage, post-hoc selection, and unsupported claims.
- Convert experimental results into analysis or paper prose while keeping every claim traceable.

### Installation

Clone this repository and copy the skill directory into your Codex skills directory:

```bash
git clone https://github.com/Seperendity/research-experiment-workflow-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R research-experiment-workflow-skill/research-experiment-workflow "${CODEX_HOME:-$HOME/.codex}/skills/"
```

After installation, invoke it from any project:

```text
Use $research-experiment-workflow to turn this research idea into a hypothesis, novelty check, feasibility report, and pilot plan.
```

### Skill Structure

```text
research-experiment-workflow/
  SKILL.md
  agents/
    openai.yaml
  references/
    artifact-contract.md
```

- `SKILL.md`: stage router, stage gates, role discipline, and operating principles.
- `references/artifact-contract.md`: experiment layout, summary schema, templates, review rubric, and writing integrity checks.
- `agents/openai.yaml`: Codex UI metadata and default prompt.

### Example: Starting A New Experiment Project

Suppose you start a new project called `personal-knowledge-os` and want to test:

> Does hybrid retrieval, BM25 plus embedding rerank, retrieve relevant personal notes better than pure embedding retrieval for personal knowledge-base QA?

From the project root, ask Codex:

```text
Use $research-experiment-workflow to set up the experiment workflow for this new project.

Project goal: build a personal knowledge-base QA system.
Research idea: test whether hybrid retrieval (BM25 + embedding rerank) retrieves relevant notes better than pure embedding retrieval.
Do not write code yet. Start with idea scoring, hypothesis, novelty check, and feasibility.
```

The expected artifacts may look like:

```text
research/
  ideas.json
  hypotheses/
    tracker.md
  experiments/
    exp-20260701-hybrid-retrieval/
      README.md
      NOVELTY.md
      FEASIBILITY.md
```

Then define the project interface contract:

```text
Use $research-experiment-workflow to add a minimal project interface contract.
Available commands:
- Retrieval evaluation: python scripts/eval_retrieval.py
- Dataset: data/eval_queries.jsonl
- Output: outputs/retrieval_metrics.json
- Baseline: pure_embedding
Metrics: recall@5, recall@10, MRR, latency_ms
```

Next, design and run a pilot:

```text
Use $research-experiment-workflow to design and execute the smallest pilot from the current FEASIBILITY.md.
Requirements:
- Use only 20 eval queries
- Compare only pure_embedding and hybrid_retrieval
- Save PILOT.md and run_notes.md
- Do not proceed to the full experiment until the pilot passes
```

If the pilot passes, run the full experiment:

```text
Use $research-experiment-workflow. The pilot passed. Execute the full experiment.
Requirements:
- Use the complete eval_queries.jsonl
- Fix the seed
- Compare pure_embedding, hybrid_retrieval, and hybrid_with_rerank
- Save results/summary.json and run_notes.md
- Do not write paper conclusions yet. Move to review first.
```

Finally, advance through review, analysis, and writing as separate stages:

```text
Use $research-experiment-workflow as Reviewer to check whether this experiment is trustworthy.
Focus on baseline fairness, data leakage, metric validity, cherry-picking, and artifact completeness.
```

```text
Use $research-experiment-workflow to write analysis.md from results/summary.json and run_notes.md.
Only state supported and unsupported claims. Do not draft paper prose yet.
```

```text
Use $research-experiment-workflow to draft the experiment section for a paper or technical report from the reviewed analysis.md.
Every number must cite the experiment id, summary.json, or analysis.md.
```

### Design Notes

This skill borrows ideas from artifact-driven research workflows and AI-Scientist-style systems: idea scoring, novelty checks, experiment budgets, run notes, review rubrics, and writing integrity checks. It is intentionally designed as a human-controlled workflow gatekeeper, not a fully automated paper generator.

### License

This repository currently has no open-source license. Add a `LICENSE` file before accepting external contributions or granting reuse rights beyond normal public viewing.

<a id="中文"></a>
## 中文

`research-experiment-workflow` 是一个 Codex skill，用来把研究、机器学习和论文实验推进成可审查的 artifact 链条。

它的核心原则是：先记录想法和假设，再做 novelty check、feasibility、pilot、正式实验、review、analysis，最后才写论文或报告文本。每个阶段都应留下可复用、可恢复、可审查的文件。

### 适用场景

- 从一个研究想法生成可证伪假设。
- 为新项目建立实验目录和 artifact contract。
- 在正式训练或大规模实验前设计 pilot。
- 检查 baseline、metric、data leakage、post-hoc selection 等风险。
- 把实验结果整理成 analysis 或论文段落，并保证每个 claim 可追溯。

### 安装

克隆仓库后，把 skill 目录复制到 Codex 的 skills 目录：

```bash
git clone https://github.com/Seperendity/research-experiment-workflow-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R research-experiment-workflow-skill/research-experiment-workflow "${CODEX_HOME:-$HOME/.codex}/skills/"
```

安装后，在任意项目里可以这样调用：

```text
使用 $research-experiment-workflow，帮我把这个研究想法推进成假设、novelty check、feasibility 和 pilot 计划。
```

### Skill 文件结构

```text
research-experiment-workflow/
  SKILL.md
  agents/
    openai.yaml
  references/
    artifact-contract.md
```

- `SKILL.md`：阶段路由、阶段门、角色纪律和操作原则。
- `references/artifact-contract.md`：实验目录、summary schema、模板、review rubric、写作完整性检查。
- `agents/openai.yaml`：Codex UI 元信息和默认 prompt。

### 新项目实验示例

假设你新开一个项目 `personal-knowledge-os`，想验证：

> 混合检索 BM25 + embedding rerank，是否比纯 embedding 检索更适合个人知识库问答？

可以在项目根目录里对 Codex 说：

```text
使用 $research-experiment-workflow，帮我为这个新项目建立实验流程。

项目目标：构建个人知识库问答系统。
研究想法：验证 hybrid retrieval（BM25 + embedding rerank）是否比 pure embedding retrieval 更能找回相关笔记。
请先不要写代码，先做 idea scoring、hypothesis、novelty check 和 feasibility。
```

理想产物类似：

```text
research/
  ideas.json
  hypotheses/
    tracker.md
  experiments/
    exp-20260701-hybrid-retrieval/
      README.md
      NOVELTY.md
      FEASIBILITY.md
```

然后补充项目接口契约：

```text
使用 $research-experiment-workflow，帮我为这个项目补一个最小 project interface contract。
当前可用命令：
- 运行检索评测：python scripts/eval_retrieval.py
- 数据集：data/eval_queries.jsonl
- 输出：outputs/retrieval_metrics.json
- baseline：pure_embedding
指标：recall@5、recall@10、MRR、latency_ms
```

接着让 Codex 设计并执行 pilot：

```text
使用 $research-experiment-workflow，基于当前 FEASIBILITY.md 设计并执行最小 pilot。
要求：
- 只用 20 条 eval queries
- 只比较 pure_embedding 和 hybrid_retrieval
- 保存 PILOT.md 和 run_notes.md
- pilot PASS 后再考虑正式实验
```

如果 pilot 通过，再进入正式实验：

```text
使用 $research-experiment-workflow，pilot 已 PASS。请执行正式实验。
要求：
- 使用完整 eval_queries.jsonl
- 固定 seed
- 比较 pure_embedding、hybrid_retrieval、hybrid_with_rerank 三组
- 保存 results/summary.json、run_notes.md
- 不要写论文结论，先进入 review
```

最后按阶段推进 review、analysis、writing：

```text
使用 $research-experiment-workflow，作为 Reviewer 检查这个实验结果是否可信。
重点检查 baseline 公平性、data leakage、metric 是否合适、是否 cherry-picking、artifact 是否完整。
```

```text
使用 $research-experiment-workflow，基于 results/summary.json 和 run_notes.md 写 analysis.md。
只写支持和不支持的 claim，不要写论文段落。
```

```text
使用 $research-experiment-workflow，基于已通过 review 的 analysis.md，起草论文或技术报告中的实验段落。
所有数字必须引用 experiment id、summary.json 或 analysis.md。
```

### 设计来源

这个 skill 借鉴了 artifact-driven research workflow、AI-Scientist 类系统中的 idea scoring、novelty check、实验预算、run notes、自动审稿 rubric 和写作完整性检查，但它有意保持为人工可控的流程守门员，而不是全自动论文生成器。

### 许可证

当前仓库未附带开源许可证。公开分享或接受外部贡献前，建议按你的授权意愿添加 `LICENSE` 文件。
