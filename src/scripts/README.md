# 数据处理脚本

> 用于 ArbiterOS trace 清洗、格式转换、结构检查。

## 脚本清单

- `validate_structure.py`：检查每个 `data/block-XX/` 是否包含必要的目录、README、metadata.yml，以及是否符合 ArbiterOS 格式。
- `parse_arbiteros_trace.py`：把 `raw/arbiteros_logs/*.jsonl` 解析成 `processed/trace_summary.json` 和 `processed/timeline.csv`。

## 使用方式

```bash
cd /path/to/repo

# 结构检查（默认模板模式：只检查目录和元数据，不强制要求已填充数据）
python src/scripts/validate_structure.py

# 严格模式（要求 raw/arbiteros_logs 或 raw/cases 非空，且 processed/ 至少有一种输出文件）
python src/scripts/validate_structure.py --strict

# 解析 JSONL 日志
python src/scripts/parse_arbiteros_trace.py --block block-01
```

## 后续扩展

- `parse_arbiteros_case.py`：把 redteam case JSON 转成 `processed/case_records.jsonl`。
- `merge_blocks.py`：合并 5 块数据到统一分析表。
- `generate_report.py`：根据 metadata 生成数据收集报告。
