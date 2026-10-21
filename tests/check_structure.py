"""Compare protected Markdown parts in a source file and an edited copy."""

import argparse
import json
import re
from pathlib import Path


def fenced_code_blocks(text):
    """Collect top-level backtick or tilde fences without ending on shorter fences."""
    blocks = []
    current = []
    closing = None
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        if closing is not None:
            current.append(line)
            if closing.fullmatch(content):
                blocks.append("".join(current).rstrip("\r\n"))
                current = []
                closing = None
            continue

        opening = re.match(r" {0,3}(`{3,}|~{3,})(.*)$", content)
        if opening is None:
            continue
        fence, info = opening.groups()
        if fence[0] == "`" and "`" in info:
            continue
        current = [line]
        closing = re.compile(r" {0,3}" + re.escape(fence[0]) + r"{%d,}[ \t]*" % len(fence))

    if current:
        blocks.append("".join(current))
    return blocks


def protected_parts(text):
    frontmatter = re.match(r"\A---\n.*?\n---\n", text, re.S)
    return {
        "frontmatter": frontmatter.group(0) if frontmatter else None,
        "fenced_code": fenced_code_blocks(text),
        "inline_code": re.findall(r"(?<!`)`([^`\n]+)`(?!`)", text),
        "headings": re.findall(r"^#{1,6} .+$", text, re.M),
        "link_targets": re.findall(r"\]\(([^\n)]+)\)", text),
        "table_rows": re.findall(r"^\|.*\|$", text, re.M),
        "ordered_steps": re.findall(r"^\d+\. .+$", text, re.M),
        "explicit_ids": re.findall(r'<[^>]+\bid="[^"]+"[^>]*>', text),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("edited", type=Path)
    args = parser.parse_args()
    before = protected_parts(args.source.read_text(encoding="utf-8"))
    after = protected_parts(args.edited.read_text(encoding="utf-8"))
    checks = {key: before[key] == after[key] for key in before}
    print(json.dumps({"preserved": checks, "passed": all(checks.values())}, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
