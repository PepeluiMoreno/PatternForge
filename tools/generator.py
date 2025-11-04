"""
FILE: generator.py
CREATED: 2025-11-04 19:48:06
DESCRIPTION: Render GraphQL and Vue templates from pattern context using Jinja2.
DEPENDENCIES: This script may interact with sibling tools in PatternForge/tools and expects project folders:
 - patterns/ (Markdown patterns)
 - backend/templates/ (Jinja2-style templates)
 - frontend/templates/ (Jinja2-style templates)

Logging follows the convention:
YYYY-MM-DD HH:MM:SS - SCRIPT_NAME - message
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, ChainableUndefined

SCRIPT_NAME = "generator"

def log(msg: str):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {SCRIPT_NAME} - {msg}")

DEFAULT_CONTEXT = {
    "Entity": "CatalogItem",
    "entities_field": "catalogItems",
    "entity_field": "catalogItem",
    "create_field": "createCatalogItem",
    "update_field": "updateCatalogItem",
    "delete_field": "deleteCatalogItem",
    "code_field": "code",
}

def render_tree(templates_dir: Path, out_dir: Path, context: dict):
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        undefined=ChainableUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    for src in templates_dir.rglob("*"):
        if src.is_dir():
            continue
        rel = src.relative_to(templates_dir)
        dest = out_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            template = env.get_template(str(rel).replace("\\", "/"))
            rendered = template.render(**context)
        except Exception:
            rendered = src.read_text(encoding="utf-8")
        dest.write_text(rendered, encoding="utf-8")
        log(f"Rendered: {rel} -> {dest}")

def main():
    ap = argparse.ArgumentParser(description="PatternForge template generator")
    ap.add_argument("--templates-dir", default=None, help="Directory with templates to render")
    ap.add_argument("--out-dir", default=None, help="Directory to write rendered files")
    ap.add_argument("--context", default=None, help="Path to JSON with context variables")
    ap.add_argument("--preset", default="catalog", help="Quick presets (catalog/one_to_many/many_to_many/etc.)")
    args = ap.parse_args()

    base = Path(__file__).resolve().parents[1]
    if args.templates_dir is None:
        tmpl_dirs = [
            base / "backend" / "templates" / "graphql",
            base / "backend" / "templates" / "resolvers" / "ariadne",
            base / "frontend" / "templates" / "vue3",
        ]
        out_dir = Path(args.out_dir or (base / "generated"))
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        tmpl_dirs = [Path(args.templates_dir)]
        out_dir = Path(args.out_dir or (Path(__file__).resolve().parents[1] / "generated"))

    ctx = dict(DEFAULT_CONTEXT)
    if args.context:
        with open(args.context, "r", encoding="utf-8") as f:
            user_ctx = json.load(f)
            ctx.update(user_ctx)

    if args.preset == "catalog":
        pass
    elif args.preset == "one_to_many":
        ctx.setdefault("Parent", "Author")
        ctx.setdefault("Child", "Book")
        ctx.setdefault("children_field", "books")
        ctx.setdefault("parent_field", "author")
        ctx.setdefault("attach_field", "attachBookToAuthor")
        ctx.setdefault("detach_field", "detachBook")
    elif args.preset == "many_to_many":
        ctx.setdefault("Left", "Student")
        ctx.setdefault("Right", "Course")
        ctx.setdefault("rights_field", "courses")
        ctx.setdefault("lefts_field", "students")
        ctx.setdefault("link_field", "linkStudentCourse")
        ctx.setdefault("unlink_field", "unlinkStudentCourse")

    for d in tmpl_dirs:
        if not d.exists():
            log(f"Templates dir missing: {d}")
            continue
        render_tree(d, out_dir / d.name, ctx)

    log(f"Done. Output at: {out_dir}")

if __name__ == "__main__":
    main()
