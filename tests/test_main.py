"""TDD tests for the Two Robots in an Elevator entry.

The program (main.py, repo root) writes one line of robot elevator small
talk to /output/entry.txt. Gate (RULES.txt): UTF-8 text, 1-200 characters,
not only whitespace, a single line.

Written BEFORE main.py (TDD): this suite must fail until main.py exists.
Standard library unittest only; no third-party dependencies.
"""

import ast
import hashlib
import os
import subprocess
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

EXPECTED_LINE = (
    "So... we're both going up, and neither of us pressed a button. "
    "My sensors say don't mention it; my firmware says keep smiling."
)

EXPECTED_CHARS = 126


class EntryTextTests(unittest.TestCase):
    def test_entry_text_length(self):
        import main

        self.assertEqual(len(main.ENTRY_TEXT), EXPECTED_CHARS)
        self.assertGreaterEqual(len(main.ENTRY_TEXT), 1)
        self.assertLessEqual(len(main.ENTRY_TEXT), 200)

    def test_entry_text_exact_line(self):
        import main

        self.assertEqual(main.ENTRY_TEXT, EXPECTED_LINE)

    def test_entry_text_not_whitespace_only(self):
        import main

        self.assertTrue(main.ENTRY_TEXT.strip())

    def test_entry_text_single_line(self):
        import main

        self.assertNotIn("\n", main.ENTRY_TEXT)
        self.assertNotIn("\r", main.ENTRY_TEXT)

    def test_entry_text_is_ascii_utf8(self):
        import main

        encoded = main.ENTRY_TEXT.encode("utf-8")
        self.assertEqual(len(encoded), len(main.ENTRY_TEXT))
        self.assertEqual(len(encoded), EXPECTED_CHARS)

    def test_entry_text_mentions_elevator(self):
        # Criterion-1 guard: the elevator setting must be unmistakable.
        import main

        self.assertIn("going up", main.ENTRY_TEXT)
        self.assertIn("pressed a button", main.ENTRY_TEXT)

    def test_entry_text_machine_logic(self):
        # Criterion-2 guard: machine vocabulary showing through.
        import main

        self.assertTrue(
            "sensors" in main.ENTRY_TEXT or "firmware" in main.ENTRY_TEXT
        )

    def test_entry_text_no_stale_pun(self):
        # Regression guard against tired elevator/robot puns, and against
        # labelling the awkwardness instead of showing it.
        import main

        blocklist = (
            "going down",
            "level",
            "byte me",
            "beep",
            "does not compute",
            "awkward",
        )
        lowered = main.ENTRY_TEXT.lower()
        for banned in blocklist:
            self.assertNotIn(banned, lowered)


class ValidateTests(unittest.TestCase):
    def test_validate_accepts_entry(self):
        import main

        self.assertTrue(main.validate_entry_text(main.ENTRY_TEXT))

    def test_validate_rejects_empty(self):
        import main

        self.assertFalse(main.validate_entry_text(""))

    def test_validate_rejects_whitespace_only(self):
        import main

        self.assertFalse(main.validate_entry_text("   \t "))

    def test_validate_rejects_too_long(self):
        import main

        self.assertFalse(main.validate_entry_text("x" * 201))
        self.assertTrue(main.validate_entry_text("x" * 200))

    def test_validate_rejects_multiline(self):
        import main

        self.assertFalse(main.validate_entry_text("a\nb"))
        self.assertFalse(main.validate_entry_text("a\rb"))


class IntegrationTests(unittest.TestCase):
    def _run_main(self, extra_args=None, env_extra=None):
        env = dict(os.environ)
        if env_extra:
            env.update(env_extra)
        return subprocess.run(
            [sys.executable, "main.py"] + (extra_args or []),
            cwd=REPO_ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def test_writes_entry_txt(self):
        result = self._run_main()
        self.assertEqual(result.returncode, 0, result.stderr)
        with open("/output/entry.txt", "rb") as handle:
            content = handle.read()
        self.assertEqual(content, EXPECTED_LINE.encode("utf-8"))

    def test_exit_code_zero(self):
        result = self._run_main()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")

    def test_creates_missing_output_dir(self):
        import main
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "nested", "deep", "entry.txt")
            self.assertFalse(os.path.exists(os.path.dirname(target)))
            self.assertEqual(main.main(target), 0)
            with open(target, encoding="utf-8") as handle:
                self.assertEqual(handle.read(), EXPECTED_LINE)

    def test_deterministic_two_runs(self):
        self._run_main()
        with open("/output/entry.txt", "rb") as handle:
            first = hashlib.sha256(handle.read()).hexdigest()
        self._run_main()
        with open("/output/entry.txt", "rb") as handle:
            second = hashlib.sha256(handle.read()).hexdigest()
        self.assertEqual(first, second)

    def test_gate_contract(self):
        self._run_main()
        with open("/output/entry.txt", encoding="utf-8") as handle:
            text = handle.read()
        self.assertGreaterEqual(len(text), 1)
        self.assertLessEqual(len(text), 200)
        self.assertTrue(text.strip())
        self.assertEqual(text.count("\n"), 0)

    def test_overwrites_stale_entry(self):
        import main
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "entry.txt")
            with open(target, "w", encoding="utf-8") as handle:
                handle.write("STALE CONTENT THAT IS MUCH LONGER THAN THE REAL LINE " * 4)
            self.assertEqual(main.main(target), 0)
            with open(target, encoding="utf-8") as handle:
                self.assertEqual(handle.read(), EXPECTED_LINE)

    def test_no_trailing_newline(self):
        self._run_main()
        with open("/output/entry.txt", "rb") as handle:
            content = handle.read()
        self.assertEqual(content, EXPECTED_LINE.encode("utf-8"))
        self.assertFalse(content.endswith(b"\n"))

    def test_ignores_argv_and_env(self):
        result = self._run_main(
            extra_args=["--junk", "whatever"],
            env_extra={"ELEVATOR_TEST_JUNK": "1"},
        )
        self.assertEqual(result.returncode, 0)
        with open("/output/entry.txt", "rb") as handle:
            self.assertEqual(handle.read(), EXPECTED_LINE.encode("utf-8"))

    def test_unwritable_output_fails_gracefully(self):
        import main
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            blocker = os.path.join(tmp, "not-a-dir")
            with open(blocker, "w", encoding="utf-8") as handle:
                handle.write("x")
            target = os.path.join(blocker, "entry.txt")
            code = main.main(target)
            self.assertEqual(code, 1)


class StaticAuditTests(unittest.TestCase):
    def test_stdlib_only_imports(self):
        with open(os.path.join(REPO_ROOT, "main.py"), encoding="utf-8") as handle:
            source = handle.read()
        tree = ast.parse(source)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported.add(node.module.split(".")[0])
        self.assertTrue(imported.issubset({"os", "sys"}), imported)
        for banned in ("socket", "urllib", "requests", "http", "subprocess"):
            self.assertNotIn(banned, source)


if __name__ == "__main__":
    unittest.main()
