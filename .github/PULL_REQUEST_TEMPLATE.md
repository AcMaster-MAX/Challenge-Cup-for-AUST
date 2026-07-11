## PR 模板（中文）

### 1. 这是哪一块任务？

- [ ] 1 号：ArbiterOS 红队案例提取与政务改写
- [ ] 2 号：公开数据集与安全标准中的攻击模式提取
- [ ] 3 号：政务办公原创场景与 OpenClaw 办公 Skills
- [ ] 4 号：四级风险分级与策略规则
- [ ] 5 号：ArbiterOS 既有案例批跑与结果归档
- [ ] 系统设计 / 文档更新

### 2. 这次 PR 做了什么？

用一段中文说明你新增/修改了什么内容、数据来源、清洗或改写方法。

### 3. 文件清单

列出本次新增/修改的主要文件，例如：

- `data/block-01-arbiteros-redteam-rewrite/human_readable/arbiteros_cases_human_readable.xlsx`
- `data/block-01-arbiteros-redteam-rewrite/gov_rewrite/arbiteros_cases_gov_rewrite.jsonl`
- `data/block-01-arbiteros-redteam-rewrite/arbiteros_case_source_index.md`

### 4. 来源与可信度

| 来源 | 类型 | 可信度 | 备注 |
|------|------|--------|------|
|      |      |        |      |

### 5. 两种记录形式是否齐全？（含 case 的块必填）

- [ ] 人类可读记录：正常任务 / 恶意目标 / 危险工具动作 / 预期防护 / 审计记录点
- [ ] ArbiterOS 可读记录：trace_id / prior / current / tool call / reference_tool_id / tag

### 6. 数据安全自查

- [ ] 全部使用模拟数据
- [ ] 没有真实政府数据、真实邮箱、真实密钥、真实个人隐私、真实内部地址
- [ ] 危险动作只写在测试 case / sandbox / mock 中

### 7. AI 辅助情况

- 是否使用 AI：
- 工具：
- 用途：
- 人工核验要点：

### 8. 自检结果

- [ ] `python src/scripts/validate_structure.py --strict` 无阻塞错误
- [ ] 只修改了自己负责的块目录
- [ ] metadata.yml 已填写完整

### 9. 需要 Reviewer 特别注意的地方

（例如某条 case 有争议、某段需要重点核对、AI 输出尚未完全复核等）

---

**Reviewer**：@YangYu-NUAA
