<p align="right">
  <a href="./README.md">English</a>
</p>

# Research Experiment Workflow Skill

一个用于研究、机器学习和论文实验的 Codex skill，核心目标是把实验过程沉淀成可审查的 artifact 链条。

这个 skill 会让 Codex 不再急着写代码和下结论，而是先评分想法、提出可证伪假设、检查新颖性风险、做可行性判断和 pilot，再进入正式实验、review、analysis，最后才写论文或报告文本。

## 它解决什么问题

- **稳定的研究流程**：覆盖 idea scoring、hypothesis、novelty check、feasibility、pilot、experiment run、review、analysis、writing。
- **可恢复的实验记录**：提供 `ideas.json`、`NOVELTY.md`、`FEASIBILITY.md`、`PILOT.md`、`run_notes.md`、`results/summary.json`、`REVIEW.md`、`analysis.md` 等 artifact 模板。
- **面向论文的防护栏**：检查 baseline、公平比较、新颖性风险、数据泄漏、指标误用、事后筛选、审稿 rubric 和写作完整性。
- **跨项目复用**：具体命令、数据路径和指标留在每个项目里；这个 skill 只负责稳定流程和阶段门。

## 安装

```bash
git clone https://github.com/Seperendity/research-experiment-workflow-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R research-experiment-workflow-skill/research-experiment-workflow "${CODEX_HOME:-$HOME/.codex}/skills/"
```

安装后，在任意 Codex 会话中调用：

```text
使用 $research-experiment-workflow，帮我把这个研究想法推进成假设、novelty check、feasibility 和 pilot 计划。
```

## 流程

```text
idea scoring
  -> hypothesis
  -> novelty check
  -> feasibility
  -> pilot
  -> experiment run
  -> review
  -> analysis
  -> writing
```

新研究方向建议走完整流程。已有项目则从最近一个有效 artifact 继续，不要从头重来。

## 仓库结构

```text
research-experiment-workflow/
  SKILL.md
  agents/
    openai.yaml
  references/
    artifact-contract.md
```

- `SKILL.md` 定义阶段路由、阶段门、角色纪律和操作原则。
- `references/artifact-contract.md` 定义 artifact schema、紧凑模板、review rubric 和写作检查。
- `agents/openai.yaml` 提供 Codex UI 元信息和默认 prompt。

## 示例：一个新项目如何开始实验

假设你新开一个项目 `personal-knowledge-os`，想验证：

> 混合检索 BM25 + embedding rerank，是否比纯 embedding 检索更适合个人知识库问答？

第一步先建立实验流程，而不是直接写代码：

```text
使用 $research-experiment-workflow，帮我为这个新项目建立实验流程。

项目目标：构建个人知识库问答系统。
研究想法：验证 hybrid retrieval（BM25 + embedding rerank）是否比 pure embedding retrieval 更能找回相关笔记。
请先不要写代码，先做 idea scoring、hypothesis、novelty check 和 feasibility。
```

第一轮产物应该类似：

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
- 指标：recall@5、recall@10、MRR、latency_ms
```

接着先跑 pilot：

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

最后把 review、analysis、writing 分开推进：

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

## 设计原则

- **Baseline first**：没有复现或明确替代 baseline，不声称提升。
- **Pilot first**：重大改动先通过最小 pilot，再扩大实验。
- **Novelty before paper claims**：写论文贡献前先检查相近工作。
- **Evidence over memory**：把证据写入 artifact，不依赖聊天上下文。
- **Writing after review**：论文文本消费通过 review 的 analysis，而不是直接消费原始日志。

## 设计来源

这个 skill 借鉴了 artifact-driven research workflow 和 AI-Scientist 类系统中的 idea scoring、novelty check、实验预算、run notes、自动审稿 rubric 和写作完整性检查，但它有意保持为人工可控的流程守门员，而不是全自动论文生成器。

## 许可证

当前仓库未附带开源许可证。公开分享或接受外部贡献前，建议按你的授权意愿添加 `LICENSE` 文件。
