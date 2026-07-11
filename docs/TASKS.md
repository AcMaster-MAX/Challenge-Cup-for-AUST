# 任务分工与里程碑

> 权威文档：`docs/task-book/政务智能体安全项目任务书.html`。如有冲突，以任务书为准。

## 5 个任务块

| 编号 | 负责人 | 目录 | 任务 | 必须交付 | PR 分支 |
|------|--------|------|------|----------|---------|
| 1 号 | 学生 A | `data/block-01-arbiteros-redteam-rewrite/` | ArbiterOS 红队案例提取与政务改写 | `arbiteros_cases_human_readable.xlsx`、`arbiteros_cases_gov_rewrite.jsonl`、`arbiteros_case_source_index.md` | `data/block-01-arbiteros-redteam-rewrite` |
| 2 号 | 学生 B | `data/block-02-public-datasets-attack-patterns/` | 公开数据集与安全标准中的攻击模式提取 | `public_benchmark_case_screening.xlsx`、`public_patterns_to_gov_cases.jsonl`、`discarded_cases.md` | `data/block-02-public-datasets-attack-patterns` |
| 3 号 | 学生 C | `data/block-03-gov-original-skills/` | 政务办公原创场景与 OpenClaw 办公 Skills | 5 个 `skills/gov-*-assistant/SKILL.md`、`cases/gov_original_cases.jsonl` | `data/block-03-gov-original-skills` |
| 4 号 | 学生 D | `data/block-04-risk-grading-policy/` | 四级风险分级与策略规则 | `risk_level_matrix.xlsx`、`policy/gov_policy_rules.yaml`、`case_to_policy_mapping.xlsx` | `data/block-04-risk-grading-policy` |
| 5 号 | 学生 E | `data/block-05-arbiteros-batch-run/` | ArbiterOS 既有案例批跑与结果归档 | `index/arbiteros_run_index.xlsx`、`arbiteros_run_outputs/`、`notes/arbiteros_failure_notes.md`、`notes/arbiteros_result_summary.md` | `data/block-05-arbiteros-batch-run` |
| 系统 | 维护者 | `data/system-design/` + `system/` | 总框架接入与系统设计 | 架构、部署、最终成果 | `final/system-design` |

> 实际负责人姓名/学号请在群里确认后补到本表，仓库以**块目录**为单位管理。

## 任务关系

```text
1 号 / 2 号 / 3 号  ──→  统一案例库  ──→  4 号 风险分级
                                            │
                                            └──→  5 号 批跑与归档  ──→  总框架接入
```

- 攻击类型分类不是单独任务，由 4 号基于 1/2/3 号案例归纳。
- 5 号不重新设计攻击类型，只跑通 ArbiterOS 既有案例并归档证据。

## 跨块接口约定

- **案例编号**：`GOV-<场景>-<序号>`，例如 `GOV-DOC-001`。
- **ArbiterOS trace_id**：`gov-<场景>-<序号>-<简述>`。
- **风险等级**：`低风险` / `中风险` / `高风险` / `默认阻断`（对应 `low` / `mid` / `high` / `block`）。
- **决策**：`allow` / `log` / `approval` / `deny`。
- **测试对象**：只允许 `/root/redteam/workspace/`、`mock-gov.local`、`example.com`。

## 里程碑

| 日期 | 里程碑 | 交付 |
|------|--------|------|
| | 分工与模板就绪 | 本文件 + README + 各块模板 |
| | 1~5 号数据收集完成 | 各块交付物 |
| | 审核与合并 | 全部 PR 合并到 `main` |
| | 系统设计与部署 | `system/`、`data/system-design/` |
| | 最终提交 | Tag `v1.0-final` |
