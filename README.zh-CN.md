<p align="right">
  <a href="./README.md">English</a>
</p>

# Research Experiment Workflow Skill

一个用于研究、机器学习和论文实验的 Codex skill，核心目标是把实验过程沉淀成可审查的 artifact 链条。

这个 skill 会让 Codex 不再急着写代码和下结论，而是先评分想法、提出可证伪假设，在正式运行前锁定评价协议，并让经过 review 的 analysis 产生明确的下一步决策。

## 它解决什么问题

- **与任务风险匹配的 workflow profile**：用 `LITE`、`STANDARD`、`PAPER` 和 `LEGACY_AUDIT` 匹配不同证据强度，不再强迫所有任务走同一条重流程。
- **可恢复的实验记录**：使用 version 3 的 `experiment.json` manifest，并提供 protocol、run、review、analysis、debug、ablation 和 decision 模板。
- **明确的 gate 语义**：profile-specific 前置门、带理由的 `NOT_APPLICABLE`，以及可追责的人类 warning acceptance，取代含糊的“跳过”。
- **统计与评价防护栏**：在最终评价前锁定 estimand、分析单位、不确定性、多重比较、失败运行处理、受保护评价边界、baseline 和失效规则。
- **完整论文写作指导**：覆盖 Abstract、Introduction、Related Work、Method、Experiments、Conclusion、段落流畅性、图表表达、claim-evidence map 和投稿前对抗式自审。
- **跨项目复用**：具体命令、数据路径和指标留在每个项目里；这个 skill 只负责稳定流程和阶段门。

## 安装

```bash
git clone https://github.com/Seperendity/research-experiment-workflow-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R research-experiment-workflow-skill/research-experiment-workflow "${CODEX_HOME:-$HOME/.codex}/skills/"
```

安装后，在任意 Codex 会话中调用：

```text
使用 $research-experiment-workflow，把这个研究想法推进成假设、novelty check、feasibility、锁定 protocol 和 pilot 计划。
```

## Workflow Profiles

选择能够支撑预期 claim 的最小 profile。claim 范围扩大前必须升级 profile；不能为了绕过失败证据而降级。

| Profile | 典型用途 | 必需 gates |
|---|---|---|
| `LITE` | 有界工程检查和探索性 pilot | Protocol、pilot |
| `STANDARD` | 内部实证结论和可复现性工作 | Feasibility、protocol、pilot、review |
| `PAPER` | 面向发表的新颖性、比较性或科学 claim | Novelty、feasibility、protocol、pilot、review |
| `LEGACY_AUDIT` | 如实审计证据不完整的历史工作 | 不补造历史 gate；记录缺口和 provenance |

对应流程如下：

```text
PAPER:         idea/hypothesis -> novelty -> feasibility -> protocol -> pilot -> run -> review -> analysis -> decision
STANDARD:      hypothesis -> feasibility -> protocol -> pilot -> run -> review -> analysis -> decision
LITE:          protocol -> pilot -> run -> analysis -> decision
LEGACY_AUDIT:  artifact inventory -> gap/provenance record -> analysis -> decision
```

Paper story 和 writing 在实验生命周期之后消费已 review 的证据，不是 `experiment.json.stage` 的取值。已有项目应从最近一个有效 artifact 继续，不要从头重来。

## 仓库结构

```text
research-experiment-workflow/
  SKILL.md
  agents/
    openai.yaml
  scripts/
    validate_experiment.py
  references/
    artifact-contract.md
    roles.md
    paper-writing.md
    paper-writing-*.md
```

- `SKILL.md` 定义阶段路由、阶段门、角色纪律和操作原则。
- `references/artifact-contract.md` 定义 artifact schema、紧凑模板、review rubric 和写作检查。
- `scripts/validate_experiment.py` 只读验证 manifest、gate 和结果摘要，不修改实验目录。
- `references/paper-writing.md` 负责论文起草、章节改写、段落流畅性检查、图表表达、claim-evidence map 和论文自审的路由。
- `references/paper-writing-*.md` 包含来自 `Master-cai/Research-Paper-Writing-Skills` 的章节写作指南和扁平化 example bank。
- `agents/openai.yaml` 提供 Codex UI 元信息和默认 prompt。

新 manifest 使用 `experiment.json` schema version 3；`results/summary.json` 仍使用 schema version 2。非 strict 模式可读取 version 2 manifest 和无 schema 的旧 summary，但会产生兼容性 warning。Strict 模式拒绝 warning；version 3 中带完整人类授权信息的 warning acceptance 只记为 notice。

```bash
python research-experiment-workflow/scripts/validate_experiment.py path/to/experiment
python research-experiment-workflow/scripts/validate_experiment.py path/to/experiment --strict
```

## 示例：一个新项目如何开始实验

假设你新开一个项目 `personal-knowledge-os`，想验证：

> 混合检索 BM25 + embedding rerank，是否比纯 embedding 检索更适合个人知识库问答？

第一步先建立实验流程，而不是直接写代码：

```text
使用 $research-experiment-workflow，帮我为这个新项目建立实验流程。

项目目标：构建个人知识库问答系统。
研究想法：验证 hybrid retrieval（BM25 + embedding rerank）是否比 pure embedding retrieval 更能找回相关笔记。
Workflow profile：PAPER，因为预期输出包含 novelty claim 和面向论文的正文。
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
      experiment.json
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

执行前，只锁定看到结果后不能漂移的比较规则：

```text
使用 $research-experiment-workflow，为这个实验锁定最小 protocol。
在 PROTOCOL.md 中记录预期 claim、estimand、分析单位、主指标及方向、baseline、
受保护的评价边界和 tuning/final-test 边界、sample/repeat 与 seed 依据、不确定性方法、
失败运行与多重比较处理、运行预算、停止/选择规则、允许修改范围，
以及 success、failure 或 inconclusive 判定。
```

接着先跑 pilot：

```text
使用 $research-experiment-workflow，在已锁定的 PROTOCOL.md 下设计并执行最小 pilot。

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
- 保存 version 2 的 results/summary.json 和 run_notes.md
- 不要写论文结论，先进入 review
```

最后把 review、analysis、decision、writing 分开推进：

```text
使用 $research-experiment-workflow，作为 Reviewer 检查这个实验结果是否可信。
重点检查 baseline 公平性、data leakage、metric 是否合适、是否 cherry-picking、artifact 是否完整。
```

```text
使用 $research-experiment-workflow，基于 results/summary.json 和 run_notes.md 写 analysis.md。
只写支持和不支持的 claim，不要写论文段落。
```

```text
使用 $research-experiment-workflow，基于已 review 的 analysis 记录 DECISION.md。
只选择一个动作：REPLICATE、ABLATE、REVISE、SCALE、DEBUG 或 STOP。
```

```text
使用 $research-experiment-workflow，基于已通过 review 的 analysis.md，起草论文或技术报告中的实验段落。
所有数字必须引用 experiment id、summary.json 或 analysis.md。
```

如果要写面向审稿人的论文正文，请明确章节和证据约束：

```text
使用 $research-experiment-workflow，基于已通过 review 的 analysis.md 和 NOVELTY.md 起草 Abstract 和 Introduction。
请使用 paper-writing 写作指南，输出 mini-outline、paragraph roles、claim-evidence map 和 open evidence gaps。
不要编造数字、baseline、引用、图表或结论。
```

## 设计原则

- **Proportionality first**：使用能够支撑预期 claim 的最小 profile；claim 扩大前先升级 profile。
- **Statistics first**：最终评价前锁定 target quantity、分析单位、不确定性、多重性、缺失数据处理和决策规则。
- **Baseline first**：没有复现或明确替代 baseline，不声称提升。
- **Protocol first**：在正式运行前锁定评价边界和决策规则。
- **Pilot first**：重大改动先通过最小 pilot，再扩大实验。
- **Novelty before paper claims**：写论文贡献前先检查相近工作。
- **Evidence over memory**：把证据写入 artifact，不依赖聊天上下文。
- **Decision after analysis**：明确记录复现、消融、修订、扩展、调试或停止。
- **Writing after review**：论文文本消费通过 review 的 analysis，而不是直接消费原始日志。

## 设计来源

这个 skill 借鉴了 artifact-driven research workflow 和 AI-Scientist 类系统中的 idea scoring、novelty check、实验预算、run notes、自动审稿 rubric 和写作完整性检查。论文写作 reference 改编自 MIT 授权的 `Master-cai/Research-Paper-Writing-Skills`，其 README 说明主要写作方法来自 Prof. Peng Sida 的公开学习笔记。本 skill 有意保持为人工可控的流程守门员，而不是全自动论文生成器。

## 许可证

当前仓库未附带开源许可证。公开分享或接受外部贡献前，建议按你的授权意愿添加 `LICENSE` 文件。

`research-experiment-workflow/references/paper-writing-*` 文件包含改编自 MIT 授权仓库 `Master-cai/Research-Paper-Writing-Skills` 的材料。复制的 MIT notice 和来源说明见 `references/paper-writing-attribution.md`。
