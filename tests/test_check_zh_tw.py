"""Unit tests for check_zh_tw.py. Run: python3 -m unittest discover tests"""

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_zh_tw  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RULES, VARIANTS = check_zh_tw.load_rules(check_zh_tw.DEFAULT_REFERENCE)


def matches(text, kind=None):
    return [(f["match"], f["kind"]) for f in check_zh_tw.scan(text, RULES, VARIANTS)
            if kind is None or f["kind"] == kind]


def definite(text):
    return [f for f in check_zh_tw.scan(text, RULES, VARIANTS) if not f["needs_context"]]


class LoadRulesTest(unittest.TestCase):
    def test_all_tables_are_parsed(self):
        kinds = {rule["kind"] for rule in RULES}
        self.assertEqual(kinds, {"term", "typo"})
        self.assertIn(("台", "臺"), [(a, b) for a, b, _ in VARIANTS])

    def test_no_duplicate_entries(self):
        seen = [rule["match"] for rule in RULES]
        self.assertEqual(len(seen), len(set(seen)))


class ScanTest(unittest.TestCase):
    def test_longest_term_wins(self):
        self.assertEqual(matches("資料放在數據庫。"), [("數據庫", "term")])

    def test_typos_and_simplified_characters(self):
        self.assertEqual(matches("已髮布這个版本"),
                         [("髮布", "typo"), ("个", "simplified")])

    def test_context_terms_are_not_definite(self):
        self.assertEqual(definite("我支持這個提案。"), [])

    def test_code_and_links_are_skipped(self):
        text = "執行 `軟件 --help`，見[說明](https://a.invalid/軟件)。\n```\n軟件\n```\n"
        self.assertEqual(matches(text), [])

    def test_clean_taiwan_text(self):
        self.assertEqual(matches("這款軟體在預設設定下支援匯出影片。"), [])


class VariantTest(unittest.TestCase):
    def test_minority_spelling_is_flagged(self):
        found = matches("臺北市政府說，台北與台中都會參加。", "variant")
        self.assertEqual(found, [("臺", "variant")])

    def test_single_spelling_passes(self):
        self.assertEqual(matches("臺北市與臺中市都會參加。", "variant"), [])

    def test_variant_findings_do_not_fail_strict(self):
        self.assertEqual(definite("臺北與台中"), [])


class DocumentExamplesTest(unittest.TestCase):
    """Rewritten examples shown to users must pass their own checker."""

    def rewritten_lines(self, path, marker):
        text = (ROOT / path).read_text(encoding="utf-8")
        lines = [line for line in text.splitlines() if marker in line]
        self.assertTrue(lines, f"no {marker} lines in {path}")
        return "\n".join(lines)

    def test_reference_examples(self):
        self.assertEqual(definite(self.rewritten_lines("references/zh-tw.md", "改寫後：")), [])

    def test_readme_examples(self):
        self.assertEqual(definite(self.rewritten_lines("README.zh-TW.md", "改寫：")), [])


class RepositoryTest(unittest.TestCase):
    def test_local_links_exist(self):
        for doc in ["SKILL.md", "README.md", "README.zh-TW.md", "CHANGELOG.md",
                    "tests/README.md", "references/zh-tw.md",
                    "references/patterns.md"]:
            text = (ROOT / doc).read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)\s]+)\)", text):
                if re.match(r"[a-z]+:|#", target):
                    continue
                path = (ROOT / doc).parent / target.split("#")[0]
                self.assertTrue(path.exists(), f"{doc}: broken link {target}")

    def test_cases_are_well_formed(self):
        import json
        cases = json.loads((ROOT / "tests/fixtures/cases.json").read_text(encoding="utf-8"))
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        for case in cases:
            self.assertTrue(case["request"] and case["input"], case["id"])


if __name__ == "__main__":
    unittest.main()
