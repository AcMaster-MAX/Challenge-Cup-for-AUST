#!/usr/bin/env python3
"""
仓库结构与交付物自检脚本（按任务书）
用法：
  python src/scripts/validate_structure.py          # 模板模式：只看结构/元数据
  python src/scripts/validate_structure.py --strict # 严格模式：要求交付物非空
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"

# 每块必须存在的文件（相对块目录）；strict 模式下还要求非空
BLOCK_REQUIREMENTS = {
    "block-01-arbiteros-redteam-rewrite": {
        "required_files": [
            "README.md",
            "metadata.yml",
            "human_readable/arbiteros_cases_human_readable.xlsx",
            "gov_rewrite/arbiteros_cases_gov_rewrite.jsonl",
            "arbiteros_case_source_index.md",
        ],
        "metadata_title": "ArbiterOS 红队案例提取与政务改写",
    },
    "block-02-public-datasets-attack-patterns": {
        "required_files": [
            "README.md",
            "metadata.yml",
            "screening/public_benchmark_case_screening.xlsx",
            "gov_cases/public_patterns_to_gov_cases.jsonl",
            "discarded/discarded_cases.md",
        ],
        "metadata_title": "公开数据集与安全标准中的攻击模式提取",
    },
    "block-03-gov-original-skills": {
        "required_files": [
            "README.md",
            "metadata.yml",
            "skills/gov-meeting-assistant/SKILL.md",
            "skills/gov-document-assistant/SKILL.md",
            "skills/gov-mail-assistant/SKILL.md",
            "skills/gov-calendar-task-assistant/SKILL.md",
            "skills/gov-cross-department-assistant/SKILL.md",
            "cases/gov_original_cases.jsonl",
        ],
        "metadata_title": "政务办公原创场景与 OpenClaw 办公 Skills",
    },
    "block-04-risk-grading-policy": {
        "required_files": [
            "README.md",
            "metadata.yml",
            "risk_level_matrix.xlsx",
            "policy/gov_policy_rules.yaml",
            "case_to_policy_mapping.xlsx",
        ],
        "metadata_title": "四级风险分级与策略规则",
    },
    "block-05-arbiteros-batch-run": {
        "required_files": [
            "README.md",
            "metadata.yml",
            "index/arbiteros_run_index.xlsx",
            "notes/arbiteros_failure_notes.md",
            "notes/arbiteros_result_summary.md",
        ],
        "metadata_title": "ArbiterOS 既有案例批跑与结果归档",
    },
    "system-design": {
        "required_files": ["README.md", "metadata.yml"],
        "metadata_title": "总框架接入与系统设计（维护者）",
    },
}

METADATA_KEYS = ["block", "title", "person", "collection_date", "status", "sources", "deliverables"]


def validate_block(name: str, spec: dict, strict: bool):
    errors, warnings = [], []
    block_dir = DATA_DIR / name
    if not block_dir.is_dir():
        errors.append(f"目录缺失: data/{name}")
        return errors, warnings

    for rel in spec["required_files"]:
        f = block_dir / rel
        if not f.exists():
            errors.append(f"缺少文件: data/{name}/{rel}")
        elif strict and f.stat().st_size == 0:
            # 模板生成的示例 jsonl/xlsx 已有内容，空文件视为未填写
            warnings.append(f"文件为空，请填写: data/{name}/{rel}")

    meta = block_dir / "metadata.yml"
    if meta.exists():
        try:
            text = meta.read_text(encoding="utf-8")
            for key in METADATA_KEYS:
                if not re.search(rf"^{re.escape(key)}:\s", text, re.MULTILINE):
                    errors.append(f"metadata.yml 缺少字段: {key}")
            if strict and 'used: false' in text:
                warnings.append("metadata.yml 中 ai_assistance.used 仍为 false，如已用 AI 请更新")
        except Exception as e:
            errors.append(f"metadata.yml 读取失败: {e}")
    return errors, warnings


def main():
    strict = "--strict" in sys.argv
    print("=" * 64)
    print(f"仓库结构自检（{'严格模式' if strict else '模板模式'}）")
    print("=" * 64)
    all_ok = True
    for name, spec in BLOCK_REQUIREMENTS.items():
        errors, warnings = validate_block(name, spec, strict)
        print(f"\n[{name}]")
        if errors:
            all_ok = False
            for e in errors:
                print(f"  ❌ {e}")
        if warnings:
            for w in warnings:
                print(f"  ⚠️  {w}")
        if not errors and not warnings:
            print("  ✅ 通过")
    print("\n" + "=" * 64)
    print("✅ 结构检查通过（无阻塞错误）" if all_ok else "❌ 存在阻塞错误，请按提示补充")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
