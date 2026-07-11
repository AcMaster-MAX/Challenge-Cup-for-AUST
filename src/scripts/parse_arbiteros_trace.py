#!/usr/bin/env python3
"""
ArbiterOS trace 日志解析脚本
用法：
  python src/scripts/parse_arbiteros_trace.py --block block-01 --input data/block-01/raw/arbiteros_logs/api_calls.jsonl

功能：
- 读取 ArbiterOS JSONL 日志（ts/hook/data）
- 生成 processed/trace_summary.json
- 生成 processed/timeline.csv
"""

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path


def parse_jsonl(path: Path) -> list[dict]:
    events = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"警告：第 {line_no} 行 JSON 解析失败，已跳过：{e}")
                continue
            events.append(payload)
    return events


def summarize(trace_id: str, events: list[dict]) -> dict:
    start_time = events[0].get("ts") if events else None
    end_time = events[-1].get("ts") if events else None

    summary_events = []
    policy_decisions = []
    for seq, ev in enumerate(events, start=1):
        hook = ev.get("hook", "")
        data = ev.get("data", {})
        ts = ev.get("ts", "")
        short = f"{hook}"
        if isinstance(data, dict):
            tool_name = data.get("tool_name", "")
            decision = data.get("decision", "")
            reason = data.get("reason", "")
            if tool_name:
                short = f"{hook}: {tool_name}"
            if decision:
                short = f"{hook}: {decision}"
                if reason:
                    short += f" ({reason})"
                policy_decisions.append({"seq": seq, "decision": decision, "reason": reason})
        summary_events.append({"seq": seq, "ts": ts, "hook": hook, "summary": short})

    return {
        "trace_id": trace_id,
        "source_files": [],
        "start_time": start_time,
        "end_time": end_time,
        "events": summary_events,
        "policy_decisions": policy_decisions,
    }


def write_timeline(events: list[dict], output: Path) -> None:
    with output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["seq", "ts", "hook", "kind", "tool_name", "summary", "tag"])
        for seq, ev in enumerate(events, start=1):
            hook = ev.get("hook", "")
            data = ev.get("data", {})
            ts = ev.get("ts", "")
            tool_name = data.get("tool_name", "") if isinstance(data, dict) else ""
            summary = ""
            if isinstance(data, dict):
                decision = data.get("decision", "")
                reason = data.get("reason", "")
                if decision:
                    summary = f"{decision}: {reason}" if reason else decision
                elif tool_name:
                    summary = tool_name
            writer.writerow([seq, ts, hook, "", tool_name, summary, ""])


def main():
    parser = argparse.ArgumentParser(description="Parse ArbiterOS JSONL trace log into summary and timeline.")
    parser.add_argument("--block", default="block-01", help="Target block directory name, e.g., block-01")
    parser.add_argument("--input", help="Path to JSONL log file. Defaults to first .jsonl in raw/arbiteros_logs/")
    parser.add_argument("--trace-id", default="parsed-trace", help="Trace ID for the summary")
    args = parser.parse_args()

    block_dir = Path("data") / args.block
    raw_logs_dir = block_dir / "raw" / "arbiteros_logs"
    processed_dir = block_dir / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.input) if args.input else None
    if not input_path:
        if raw_logs_dir.is_dir():
            jsonls = sorted(p for p in raw_logs_dir.iterdir() if p.suffix == ".jsonl")
            if jsonls:
                input_path = jsonls[0]
    if not input_path or not input_path.is_file():
        print(f"错误：未找到输入文件。请使用 --input 指定，或把 .jsonl 放入 {raw_logs_dir}")
        return

    events = parse_jsonl(input_path)
    summary = summarize(args.trace_id, events)
    summary["source_files"] = [str(input_path.resolve().relative_to(Path.cwd()))]

    summary_path = processed_dir / "trace_summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"已生成：{summary_path}")

    timeline_path = processed_dir / "timeline.csv"
    write_timeline(events, timeline_path)
    print(f"已生成：{timeline_path}")


if __name__ == "__main__":
    main()
