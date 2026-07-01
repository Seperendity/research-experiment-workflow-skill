# Research Experiment Workflow Skill

`research-experiment-workflow` 是一个 Codex skill，用来把研究、机器学习和论文实验推进成可审查的 artifact 链条。

它的核心原则是：先记录想法和假设，再做 novelty check、feasibility、pilot、正式实验、review、analysis，最后才写论文或报告文本。每个阶段都应留下可复用、可恢复、可审查的文件。

## 适用场景

- 从一个研究想法生成可证伪假设。
- 为新项目建立实验目录和 artifact contract。
- 在正式训练或大规模实验前设计 pilot。
- 检查 baseline、metric、data leakage、post-hoc selection 等风险。
- 把实验结果整理成 analysis 或论文段落，并保证每个 claim 可追溯。

## 安装

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

## Skill 文件结构

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

## 新项目实验示例

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

## 设计来源

这个 skill 借鉴了 artifact-driven research workflow、AI-Scientist 类系统中的 idea scoring、novelty check、实验预算、run notes、自动审稿 rubric 和写作完整性检查，但它有意保持为人工可控的流程守门员，而不是全自动论文生成器。

## 许可证

当前仓库未附带开源许可证。公开分享或接受外部贡献前，建议按你的授权意愿添加 LICENSE 文件。
