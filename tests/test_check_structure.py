"""Offline CLI regressions for protected Markdown code fences."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("check_structure.py")


class FencedCodeCLITests(unittest.TestCase):
    def check_edit(self, source, edited):
        with tempfile.TemporaryDirectory() as directory:
            before = Path(directory) / "source.md"
            after = Path(directory) / "edited.md"
            before.write_text(source, encoding="utf-8")
            after.write_text(edited, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(before), str(after)],
                capture_output=True,
                encoding="utf-8",
                timeout=10,
            )
            self.assertEqual(result.stderr, "")
            return result.returncode, json.loads(result.stdout)

    def test_code_changes_are_rejected_for_supported_fences(self):
        cases = {
            "backticks": "```python\nvalue = 1\n```\n",
            "tildes": "~~~python\nvalue = 1\n~~~\n",
            "three_space_indent": "   ```python\nvalue = 1\n   ```\n",
            "long_fence_with_inner_example": "````markdown\n```python\nexample\n```\nvalue = 1\n````\n",
            "different_marker_does_not_close": "~~~text\n```\nvalue = 1\n~~~\n",
            "shorter_fence_does_not_close": "~~~~text\n~~~\nvalue = 1\n~~~~\n",
            "trailing_text_does_not_close": "~~~text\n~~~ still code\nvalue = 1\n~~~\n",
            "longer_closing_fence": "```python\nvalue = 1\n````\n",
            "unclosed_backticks": "```python\nvalue = 1\n",
            "unclosed_tildes": "~~~python\nvalue = 1\n",
        }
        for name, source in cases.items():
            with self.subTest(name=name):
                code, report = self.check_edit(source, source.replace("value = 1", "value = 2"))
                self.assertEqual(code, 1)
                self.assertFalse(report["passed"])
                self.assertFalse(report["preserved"]["fenced_code"])

    def test_prose_after_valid_closing_fence_can_change(self):
        for opening, closing in [("```", "```"), ("~~~", "~~~~"), ("````", "```` \t")]:
            with self.subTest(opening=opening, closing=closing):
                source = opening + "text\nfixed code\n" + closing + "\nOriginal prose.\n"
                code, report = self.check_edit(source, source.replace("Original prose.", "Clearer prose."))
                self.assertEqual(code, 0)
                self.assertTrue(report["passed"])

    def test_inline_markers_do_not_start_a_fenced_block(self):
        source = "A sentence contains ~~~ markers.\nOriginal prose.\n"
        code, report = self.check_edit(source, source.replace("Original prose.", "Clearer prose."))
        self.assertEqual(code, 0)
        self.assertTrue(report["passed"])

    def test_backticks_in_info_string_do_not_start_a_fenced_block(self):
        source = "```bad`info\nOriginal prose.\n"
        code, report = self.check_edit(source, source.replace("Original prose.", "Clearer prose."))
        self.assertEqual(code, 0)
        self.assertTrue(report["passed"])

    def test_tilde_code_change_reports_the_protected_category(self):
        source = "# Heading\n\n~~~text\nOriginal code.\n~~~\n"
        code, report = self.check_edit(source, source.replace("Original code.", "Changed code."))
        self.assertEqual(code, 1)
        self.assertEqual(
            [name for name, preserved in report["preserved"].items() if not preserved],
            ["fenced_code"],
        )


if __name__ == "__main__":
    unittest.main()
