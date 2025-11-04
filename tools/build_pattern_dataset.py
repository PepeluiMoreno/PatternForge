"""
FILE: build_pattern_dataset.py
CREATED: 2025-11-04 19:48:06
DESCRIPTION: Parse Markdown patterns into a JSONL dataset for training or validation.
DEPENDENCIES: This script may interact with sibling tools in PatternForge/tools and expects project folders:
 - patterns/ (Markdown patterns)
 - backend/templates/ (Jinja2-style templates)
 - frontend/templates/ (Jinja2-style templates)

Logging follows the convention:
YYYY-MM-DD HH:MM:SS - SCRIPT_NAME - message
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

SCRIPT_NAME = "build_pattern_dataset"

def log(msg: str):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {SCRIPT_NAME} - {msg}")

HEADING_RE = re.compile(r"^(#+)\s*(.+?)\s*$")
SECTION_ORDER = [
    "Pattern", "Purpose", "GraphQL", "Vue", "Detection", "Input/Output",
    "Backend", "Frontend", "Examples", "Notes", "Performance", "Integrity",
]

def parse_markdown(md_text: str):
    lines = md_text.splitlines()
    sections = []
    current = None
    for line in lines:
        m = HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            current = {"level": level, "title": title, "content": []}
            sections.append(current)
        else:
            if current is None:
                current = {"level": 0, "title": "Preamble", "content": []}
                sections.append(current)
            current["content"].append(line)
    for s in sections:
        s["content"] = "\n".join(s["content"]).strip()
    return sections

def build_example_record(path: Path, sections):
    title = None
    for s in sections:
        if s["level"] == 1 and s["title"]:
            title = s["title"]
            break
    title = title or path.stem

    purpose = _get_section_text(sections, ["Purpose"])
    detection = _get_section_text(sections, ["Detection", "Detección"])
    graphql = _get_section_text(sections, ["GraphQL", "GraphQL (SDL, schema-first)"])
    vue = _get_section_text(sections, ["Vue", "Vue mapping"])
    backend = _get_section_text(sections, ["Backend", "Resolvers"])

    input_parts = [p for p in [purpose, detection] if p]
    output_parts = [p for p in [graphql, vue, backend] if p]

    record = {
        "id": path.stem,
        "title": title,
        "source_file": str(path),
        "sections": sections,
        "input": "\n\n".join(input_parts).strip(),
        "output": "\n\n".join(output_parts).strip(),
    }
    return record

def _get_section_text(sections, names):
    for s in sections:
        for n in names:
            if s["title"].lower().startswith(n.lower()):
                return s["content"]
    return ""

def main():
    ap = argparse.ArgumentParser(description="Build JSONL dataset from Markdown patterns")
    ap.add_argument("--patterns-dir", default=str(Path(__file__).resolve().parents[1] / "patterns"), help="Path to patterns directory")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "data/pattern_dataset.jsonl"), help="Output JSONL path")
    ap.add_argument("--glob", default="*.md", help="Glob for pattern files")
    args = ap.parse_args()

    patterns_dir = Path(args.patterns_dir)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not patterns_dir.exists():
        log(f"Patterns directory not found: {patterns_dir}")
        raise SystemExit(1)

    log(f"Scanning patterns in {patterns_dir} (glob={args.glob})")
    files = sorted(patterns_dir.rglob(args.glob))
    log(f"Found {len(files)} files")

    count = 0
    with open(out_path, "w", encoding="utf-8") as fout:
        for fp in files:
            try:
                text = fp.read_text(encoding="utf-8")
                sections = parse_markdown(text)
                rec = build_example_record(fp, sections)
                fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
                count += 1
            except Exception as e:
                log(f"Error processing {fp}: {e}")
    log(f"Wrote {count} records to {out_path}")

if __name__ == "__main__":
    main()
