<p align="right"><a href="./README.md">English</a></p>

# Research Experiment Workflow Skill

一个用于可复现研究、机器学习实验和基于证据进行论文写作的 Codex Skill。它通过锁定实验方案、保存结果、审查证据和明确决策，让每项结论都能追溯到实验文件。

## 为什么需要这个 Skill

AI 编程代理已经能够修改代码并运行实验，但研究过程仍可能出现实验方案在运行中被悄然改变、最终测试集泄漏、基线缺失、会话中断后状态丢失，以及结论无法追溯到结果文件等问题。本 Skill 将研究状态和证据保存为可长期保留、可审查的文件，而不是依赖聊天记录。

## 设计重点

- **自动匹配严谨度：** 模型根据任务目标、结果用途和现有实验记录，自动选择 `LITE`、`STANDARD`、`PAPER` 或 `LEGACY_AUDIT`。
- **只完成当前所需工作：** 只生成完成当前步骤所需的文件，不擅自执行后续完整流程。
- **可恢复的实验状态：** `experiment.json` 记录当前阶段、状态、检查结果和文件路径。
- **确定性校验：** 基于 Python 标准库的校验器检查实验文件的结构和一致性，但不判断科学结论是否真实。
- **写作以证据为依据：** 定量和比较性结论必须能够追溯到已保存、已审查的证据。

## 安装

```bash
git clone https://github.com/Seperendity/research-experiment-workflow-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R research-experiment-workflow-skill/research-experiment-workflow \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

## 使用

直接描述任务，无需选择配置：

```text
使用 $research-experiment-workflow，比较两个本地训练配置。
先做一次小规模试运行，再告诉我应该保留哪一个。
```

Skill 会自动选择能够支撑当前目标的最低配置，并将选择结果记录在实验状态中。

该 skill 默认关闭隐式调用。未点名 `$research-experiment-workflow` 的请求一律使用 Codex 常规行为，包括实验设计、代码调试、分析和写作。

Skill 会自动校验修改后的实验文件并报告阻塞问题，用户无需手动运行校验器。

常见请求：

```text
使用 $research-experiment-workflow，从 experiment.json 恢复实验。

使用 $research-experiment-workflow，审查 results/summary.json 并给出下一步决策。

使用 $research-experiment-workflow，根据已审查的证据起草 Experiments 章节。
```

## 自动选择的工作配置

以下配置是 Skill 内部使用的严谨度等级，用户无需提前选择。

| 配置 | 适用场景 | 必需检查 |
|---|---|---|
| `LITE` | 范围明确的工程比较或探索性试运行 | 实验方案、试运行 |
| `STANDARD` | 内部实证结论和可复现性工作 | 可行性、实验方案、试运行、结果审查 |
| `PAPER` | 面向发表的新颖性或科学结论 | 新颖性、可行性、实验方案、试运行、结果审查 |
| `LEGACY_AUDIT` | 无法重建流程历史的旧实验 | 记录证据缺口；不补造历史检查记录 |

已有实验会沿用原配置；只有结论范围扩大时才升级，不能通过降级绕过缺失或失败的证据。

一个完整且已有结果的 `LITE` 实验只使用四个文件：`experiment.json`、`EXPERIMENT.md`、`results/summary.json` 和 `DECISION.md`。不要预先创建独立的检查文件、运行记录或分析文件。

## 工作流程

```text
LITE:     实验方案 -> 试运行 -> 正式运行 -> 分析 -> 决策
STANDARD: 假设 -> 可行性 -> 实验方案 -> 试运行 -> 正式运行 -> 结果审查 -> 分析 -> 决策
PAPER:    假设 -> 新颖性 -> 可行性 -> 实验方案 -> 试运行 -> 正式运行 -> 结果审查 -> 分析 -> 决策
```

论文写作使用已审查的证据，不属于实验阶段。

## 与同类工具的区别

本仓库为现有研究项目补充一套轻量的实验记录与证据管理方法：

| 对比类型 | 本仓库的侧重点 |
|---|---|
| 端到端自动科研系统 | 保留人工监督，完成当前请求后停止；必要条件不满足时也不会继续 |
| 自动优化循环 | 管理实验状态、基线、不确定性、已有结果何时需要作废，以及结论的适用范围，而不是只围绕单一指标循环 |
| 综合型学术 Skill 套件 | 聚焦实验生命周期，通过渐进加载减少不相关上下文 |
| 论文写作 Skill | 论文内容必须使用已保存的实验依据，而不是脱离实验过程单独生成 |

本 Skill 不替代实验代码、任务调度器、文献数据库或研究者判断；它为项目现有工具和约定补充一套轻量、可审查的工作流程。

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
- `tests/` 包含校验器测试、行为案例契约检查和测试夹具。

## 许可证与归因

本仓库采用 [MIT License](LICENSE)。

`paper-writing-*` 参考文件改编自采用 MIT License 的 [`Master-cai/Research-Paper-Writing-Skills`](https://github.com/Master-cai/Research-Paper-Writing-Skills)。这部分内容仍保留上游版权和许可声明，详见 [`paper-writing-attribution.md`](research-experiment-workflow/references/paper-writing-attribution.md)。
