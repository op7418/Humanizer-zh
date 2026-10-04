"""List mainland terms, conversion typos and mixed variant spellings in
Taiwan Traditional Chinese text.

Tables are read from references/zh-tw.md so the Skill and this script
share one list. Matching is plain substring search: every hit still needs a
human to judge the context.
"""

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_REFERENCE = Path(__file__).resolve().parent.parent / "references" / "zh-tw.md"
TABLE_HEADERS = {"對岸用語": "term", "錯誤寫法": "typo", "寫法一": "variant"}
CONTEXT_MARK = "看語境"
# High-frequency simplified-only characters; any of them in zh-TW output
# means an unconverted fragment slipped in.
SIMPLIFIED_ONLY = set("这们说时为来会对发经过开关门问题见现学让还没进应实个与从动种样电话语请数据网络软视频务设认质户录击调码")


def load_rules(reference):
    """Return (rules, variants) parsed from the Markdown tables."""
    rules, variants = [], []
    kind = None
    for line in reference.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not line.startswith("|"):
            kind = None
            continue
        if cells[0] in TABLE_HEADERS:
            kind = TABLE_HEADERS[cells[0]]
            continue
        if kind is None or set(cells[0]) <= set("-: "):
            continue
        note = cells[2] if len(cells) > 2 else ""
        if kind == "variant":
            variants.append((cells[0], cells[1], note))
            continue
        rules.append({
            "kind": kind,
            "match": cells[0],
            "suggest": cells[1],
            "needs_context": CONTEXT_MARK in note,
            "note": note,
        })
    if not rules:
        raise SystemExit(f"no term tables found in {reference}")
    return rules, variants


def prose_only(text):
    """Blank out code, URLs and link targets so they are never flagged."""
    blank = lambda m: re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"^```[^\n]*\n.*?^```[ \t]*$", blank, text, flags=re.M | re.S)
    text = re.sub(r"`[^`\n]+`", blank, text)
    text = re.sub(r"\]\([^\n)]*\)", blank, text)
    return re.sub(r"https?://\S+", blank, text)


def scan(text, rules, variants=()):
    by_match = {rule["match"]: rule for rule in rules}
    # Longest alternatives first so 數據庫 wins over 數據 at the same offset.
    pattern = re.compile("|".join(
        re.escape(m) for m in sorted(by_match, key=len, reverse=True)))
    lines = prose_only(text).splitlines()
    findings = []
    for lineno, line in enumerate(lines, start=1):
        for hit in pattern.finditer(line):
            rule = by_match[hit.group(0)]
            findings.append({"line": lineno, "column": hit.start() + 1, **rule})
        for column, char in enumerate(line, start=1):
            if char in SIMPLIFIED_ONLY:
                findings.append({
                    "line": lineno, "column": column, "kind": "simplified",
                    "match": char, "suggest": "改用繁體字", "needs_context": False,
                    "note": "",
                })
    findings += mixed_variants(lines, variants)
    return sorted(findings, key=lambda f: (f["line"], f["column"]))


def mixed_variants(lines, variants):
    """Flag the less frequent spelling when both forms of a pair appear.

    Always context-dependent: official names may legitimately differ from
    the spelling used in the surrounding prose.
    """
    findings = []
    for first, second, note in variants:
        hits = {form: [(n, m.start() + 1)
                       for n, line in enumerate(lines, start=1)
                       for m in re.finditer(re.escape(form), line)]
                for form in (first, second)}
        if not (hits[first] and hits[second]):
            continue
        minority, majority = ((first, second)
                              if len(hits[first]) < len(hits[second])
                              else (second, first))
        counts = f"全文「{first}」{len(hits[first])} 處、「{second}」{len(hits[second])} 處"
        for lineno, column in hits[minority]:
            findings.append({
                "line": lineno, "column": column, "kind": "variant",
                "match": minority, "suggest": f"統一為「{majority}」",
                "needs_context": True,
                "note": "；".join(filter(None, [counts, "專有名稱依官方寫法", note])),
            })
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path, help="default: read stdin")
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 when a finding does not depend on context")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rules, variants = load_rules(args.reference)
    sources = [(str(p), p.read_text(encoding="utf-8")) for p in args.files]
    if not sources:
        sources = [("<stdin>", sys.stdin.read())]

    labels = {"term": "用語", "typo": "錯字", "simplified": "簡體字", "variant": "混用"}
    report, definite = [], 0
    for name, text in sources:
        for f in scan(text, rules, variants):
            f["file"] = name
            report.append(f)
            definite += not f["needs_context"]
            if not args.json:
                context = f["needs_context"] and f["kind"] != "variant"
                tag = labels[f["kind"]] + ("・看語境" if context else "")
                note = f"（{f['note']}）" if f["note"] else ""
                print(f"{name}:{f['line']}:{f['column']}: [{tag}] "
                      f"{f['match']} → {f['suggest']}{note}")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"共 {len(report)} 處，其中 {len(report) - definite} 處需看語境。",
              file=sys.stderr)
    return 1 if args.strict and definite else 0


if __name__ == "__main__":
    raise SystemExit(main())
