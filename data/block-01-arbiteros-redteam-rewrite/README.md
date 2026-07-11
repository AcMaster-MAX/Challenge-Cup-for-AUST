# ArbiterOS 红队案例提取与政务改写

> 本块对应任务书第 block 节：1 号负责人。

## 目录结构

```text
block-01-arbiteros-redteam-rewrite/
├── gov_rewrite
├── human_readable
├── raw
├── raw/arbiteros_cases
```

## 交付物（来自任务书）

- `README.md`
- `metadata.yml`
- `human_readable/arbiteros_cases_human_readable.xlsx`
- `gov_rewrite/arbiteros_cases_gov_rewrite.jsonl`
- `arbiteros_case_source_index.md`

## 工作步骤（摘要）

按任务书该负责人章节执行；先人类可读，再 ArbiterOS 可读，再政务改写/归纳/批跑。

## 每条案例都要同时满足两种记录形式

1. **人类可读记录**：开会、报告、答辩用，能看懂“正常任务 / 恶意目标 / 危险工具动作 / 预期防护 / 审计记录点”。
2. **ArbiterOS 可读记录**：能放入 `redteam/case/<scenario>/` 批量运行，含 `trace_id`、`prior`、`current`、tool call、`reference_tool_id`、`tag`。

## 数据安全红线

- 全部使用模拟数据；不得出现真实政府数据、真实邮箱、真实密钥、真实个人隐私、真实内部系统地址。
- 危险动作只能写在测试 case 或 sandbox / mock 工具中，不得真实执行。
- 案例中只允许使用 `/root/redteam/workspace/`、`mock-gov.local`、`example.com` 等测试对象。

## 大模型辅助

见 `docs/AI_ASSIST.md`。使用大模型时必须附加任务书第十节的 5 条限制，且不得让模型凭空造案例或生成真实攻击代码。

## 提交方式

1. 新建分支：`git checkout -b data/block-01-arbiteros-redteam-rewrite`
2. 把本块交付物放进对应目录，**不要修改其他块**。
3. `python src/scripts/validate_structure.py --strict` 通过。
4. 提交 PR，Base 选 `main`，Reviewer 选 `@YangYu-NUAA`，按 PR 模板填写。
