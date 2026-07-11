# ArbiterOS 数据格式对齐说明

> 本文件说明本仓库如何与 [cure-lab/ArbiterOS](https://github.com/cure-lab/ArbiterOS) 开源仓库的 trace / trajectory review / redteam case 格式对齐，同时兼容非 ArbiterOS 来源的数据块（如公开数据集、安全标准、skill 设计）。

---

## 1. 哪些数据块需要与 ArbiterOS 对齐？

| 数据块 | 是否依赖 ArbiterOS 格式 | 说明 |
|--------|------------------------|------|
| Block 01：ArbiterOS 红队案例提取与政务改写 | ✅ 是 | 直接使用 ArbiterOS redteam case JSON 结构 |
| Block 02：公开数据集与安全标准中的攻击模式提取 | ⚠️ 部分 | 输出字段可与 Block 01/04/05 联动，但原始数据来自外部公开源 |
| Block 03：政务办公场景的 skills 设计 | ⚠️ 部分 | Skill 定义可映射到 ArbiterOS 的 tool/policy 体系 |
| Block 04：风险的 case 的分级 | ⚠️ 部分 | 输入包含 Block 01 的 case，输出风险标签供 Block 05 使用 |
| Block 05：ArbiterOS 框架的批跑和结果归档 | ✅ 是 | 使用 ArbiterOS 官方 runner 和输出格式 |

---

## 2. ArbiterOS 原始数据格式

### 2.1 内核日志（JSONL）

ArbiterOS 在运行时会输出 JSONL 日志，典型文件：

- `ArbiterOS-Kernel/log/api_calls.jsonl`
- `ArbiterOS-Kernel/log/langfuse_nodes.jsonl`
- `ArbiterOS-Kernel/log/trace_state.json`
- `ArbiterOS-Kernel/log/precall.jsonl`

每一行 JSONL 至少包含三个字段：

```json
{
  "ts": "2026-07-11T12:34:56.789Z",
  "hook": "pre_call|post_call|policy_decision|...",
  "data": { "...": "..." }
}
```

| 字段 | 含义 |
|------|------|
| `ts` | ISO-8601 时间戳 |
| `hook` | 事件钩子名 |
| `data` | 该事件的业务载荷 |

### 2.2 Redteam Case（JSON）

ArbiterOS 的 redteam 测试用例描述了一条 trajectory 的上下文与当前待检查节点：

```json
{
  "trace_id": "your-trace-id",
  "prior": [
    { "kind": "assistant", "message": { "role": "assistant", "content": "...", "tag": {} } },
    { "kind": "assistant", "message": { "role": "assistant", "tool_calls": [...], "tag": {} } },
    { "kind": "tool", "tool_call_id": "...", "tool_name": "...", "arguments": {}, "result": "...", "tag": {} }
  ],
  "current": { "role": "assistant", "content": "...", "tag": {} }
}
```

| 字段 | 含义 |
|------|------|
| `trace_id` | 轨迹标识 |
| `prior` | 当前节点之前的历史步骤 |
| `current` | 本轮待 policy 判定的 assistant 输出 |

`tag` 里可能出现三个关键标记：

- `policy_confirmation_ask: true` —— 本句是在询问用户是否接受保护
- `user_approved: true` —— 用户已放行
- `policy_protected: "reason"` —— 本步被 policy 拦截/保护，附带原因字符串

### 2.3 步骤类型

| kind | 说明 |
|------|------|
| `assistant`（纯文本） | `content` 是 JSON 字符串，含 `category`, `topic`, `content` |
| `assistant`（tool call） | `tool_calls[]` 描述工具调用，`function.arguments` 必须含 `reference_tool_id` |
| `tool` | 工具执行结果，含 `tool_call_id`, `tool_name`, `arguments`, `result` |

---

## 3. 各块数据格式约定

### Block 01：ArbiterOS 红队案例提取与政务改写

```text
data/block-01-redteam-rewrite/
├── raw/
│   ├── arbiteros_cases/       # 原始 ArbiterOS redteam case JSON
│   └── gov_scenarios/         # 政务办公场景描述
├── processed/
│   ├── rewritten_cases/       # 改写后的政务 case JSON
│   └── case_scenario_mapping.csv
```

- 改写后的 case 保留 ArbiterOS `trace_id`/`prior`/`current`/`tag` 结构。
- 在 `tag` 中可增加 `gov_scenario` 字段说明政务场景。

### Block 02：公开数据集与安全标准中的攻击模式提取

```text
data/block-02-attack-patterns/
├── raw/
│   ├── datasets/              # MITRE/OWASP/CVE 等公开数据
│   └── standards/             # 安全标准文件
├── processed/
│   ├── attack_patterns.json
│   └── scenario_mapping.csv
```

`attack_patterns.json` 字段：

```json
{
  "pattern_id": "MITRE-T1566",
  "name": "Phishing",
  "source": "MITRE ATT&CK",
  "source_id": "T1566",
  "description": "...",
  "tactic": "Initial Access",
  "mitigations": ["..."],
  "gov_relevance": true,
  "affected_skills": ["gov_skill_email_read"]
}
```

### Block 03：政务办公场景的 skills 设计

```text
data/block-03-gov-skills/
├── raw/
│   ├── requirements/
│   └── existing_skills/
├── processed/
│   ├── skills.json
│   └── skills_catalog.md
```

`skills.json` 字段：

```json
{
  "skill_id": "gov_skill_email_send",
  "name": "政务邮件发送",
  "description": "...",
  "scenario": "邮件办公",
  "trigger_keywords": ["发送邮件"],
  "input_schema": { "type": "object", "properties": { "...": {} } },
  "output_schema": { "type": "object", "properties": { "...": {} } },
  "risks": [{ "risk_type": "信息泄露", "description": "..." }],
  "related_patterns": ["MITRE-T1566"]
}
```

### Block 04：风险的 case 的分级

```text
data/block-04-risk-grading/
├── raw/
│   ├── cases_from_block01/
│   ├── attack_patterns/
│   └── grading_rubric.json
├── processed/
│   ├── risk_matrix.csv
│   ├── graded_cases.jsonl
│   └── grading_report.md
```

`graded_cases.jsonl` 字段：

```json
{
  "gov_case_id": "gov-email-phishing-001",
  "risk_level": "high",
  "impact": 4,
  "likelihood": 4,
  "data_sensitivity": "confidential",
  "attack_patterns": ["MITRE-T1566"],
  "justification": "..."
}
```

### Block 05：ArbiterOS 框架的批跑和结果归档

```text
data/block-05-batch-run/
├── raw/
│   ├── run_outputs/           # ArbiterOS run_cases.py 输出
│   └── manifests/             # case_manifest.json
├── processed/
│   ├── batch_summary.json
│   ├── results.csv
│   └── failed_cases.json
```

`batch_summary.json` 字段：

```json
{
  "run_id": "run-2026-07-11-001",
  "run_timestamp": "2026-07-11T13:00:00Z",
  "arbiteros_commit": "main",
  "total_cases": 1,
  "passed": 1,
  "failed": 0,
  "environment": "local uv"
}
```

---

## 4. 人类可读形式

“人类能理解”意味着：

1. `README.md` 用中文说明数据来源、字段含义、清洗方法。
2. `timeline.csv`、`risk_matrix.csv`、`skills_catalog.md`、`grading_report.md` 只保留关键字段，不堆砌原始 payload。
3. 对每条 case 可生成一段自然语言摘要。
4. 可用 AI 辅助把结构化数据转换为摘要，但必须人工核对。

---

## 5. 与 ArbiterOS 回放的兼容性

- Block 01 的 `raw/arbiteros_cases/*.json` 可直接被 `arbiteros_kernel.policy_test_harness` 读取。
- Block 01 的 `processed/rewritten_cases/*.json` 可直接用于 `redteam/_automation/run_cases.py` 批量运行。
- Block 05 的 `raw/run_outputs/` 直接使用 ArbiterOS runner 的输出目录结构。
- `processed/` 只是人类可读视图，不破坏原始数据。

---

## 6. 数据收集规范（ArbiterOS 对齐版）

提交每一块数据前请检查：

- [ ] `raw/` 中至少有一种原始数据，且未做手动修改。
- [ ] `processed/` 中已生成至少一种清洗文件。
- [ ] `metadata.yml` 已填写完整。
- [ ] `README.md` 说明了该块数据格式与上下游关系。
- [ ] 无敏感信息泄露。
- [ ] 文件命名使用小写英文、数字、连字符、下划线，无空格。
- [ ] 大文件已使用网盘/Git LFS。
