<p align="right"><a href="./README.md">English</a></p>

# Research Experiment Workflow Skill

一个用于可复现研究、机器学习实验和循证论文写作的 Codex skill。它通过锁定协议、保存结果、审查证据和明确决策，让每项结论都能追溯到实验文件。

## 特性

- 四种严谨度配置：`LITE`、`STANDARD`、`PAPER` 和 `LEGACY_AUDIT`。
- 正式运行前检查协议、基线、评估边界、不确定性和失败处理。
- 可恢复的 `experiment.json` 清单和确定性校验器。
- 基于证据的分析、决策和论文写作。
- 渐进加载：只在需要时读取详细格式定义和写作指南。

## 安装

```bash
git clone https://github.com/Seperendity/research-experiment-workflow-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R research-experiment-workflow-skill/research-experiment-workflow \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

## 使用

显式调用：

```text
使用 $research-experiment-workflow，为这个比较创建并锁定 PROTOCOL.md。
```

该 skill 默认关闭隐式调用。普通实验讨论、构思、代码调试和通用分析应使用 Codex 的常规行为；只有用户点名该 skill 或明确要求创建持久化实验文件时才调用。

常见请求：

```text
使用 $research-experiment-workflow，从 experiment.json 恢复实验。

使用 $research-experiment-workflow，审查 results/summary.json 并给出下一步决策。

使用 $research-experiment-workflow，根据已审查的证据起草 Experiments 章节。
```

## Profiles

| Profile | 用途 | 必需阶段门 |
|---|---|---|
| `LITE` | 有界工程证据或探索性 pilot | Protocol、pilot |
| `STANDARD` | 内部实证结论和可复现性工作 | Feasibility、protocol、pilot、review |
| `PAPER` | 面向发表的新颖性或科学结论 | Novelty、feasibility、protocol、pilot、review |
| `LEGACY_AUDIT` | 无法重建流程历史的旧实验 | 记录缺口；不补造历史阶段门 |

选择能够支撑预期结论的最低配置。不能通过降级绕过缺失或失败的证据。

## 证据流程

```text
hypothesis -> protocol -> pilot -> run -> review -> analysis -> decision
```

`STANDARD` 增加 feasibility 和 review；`PAPER` 还增加 novelty。`LITE` 省略其结论范围不需要的阶段门。论文写作使用已审查的证据，不属于实验阶段。

## 校验

新实验清单使用 schema version 3；结果摘要使用 schema version 2。

```bash
python research-experiment-workflow/scripts/validate_experiment.py path/to/experiment --strict
python -m unittest discover -s tests -v
```

## 仓库结构

```text
research-experiment-workflow/
  SKILL.md
  agents/openai.yaml
  scripts/validate_experiment.py
  references/
tests/
```

- `SKILL.md` 包含任务路由和核心契约。
- `references/artifact-contract.md` 定义格式和模板。
- `references/paper-writing.md` 路由各章节写作指南。
- `tests/` 包含校验器、行为、触发和测试夹具。

## 归因与许可证

`paper-writing-*` 参考文件改编自 MIT 授权的 [`Master-cai/Research-Paper-Writing-Skills`](https://github.com/Master-cai/Research-Paper-Writing-Skills)。完整许可声明见 [`paper-writing-attribution.md`](research-experiment-workflow/references/paper-writing-attribution.md)。

仓库目前没有项目级开源许可证。授予复用权或接受外部贡献前，应先添加 `LICENSE` 文件。
