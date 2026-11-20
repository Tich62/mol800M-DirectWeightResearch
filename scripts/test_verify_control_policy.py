"""Synthetic-only tests of the ZzzOps source-bound policy check."""
from pathlib import Path
import shutil
import tempfile
import unittest
from verify_control_policy import verify

SOURCE = Path(__file__).resolve().parents[1]


class ControlPolicyTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.files = []
        for name in (
            "README.md", "AGENTS.md", ".zzzops/PROJECT.md",
            ".zzzops/POLICY.json", ".zzzops/PROJECT_AUDIT.md",
        ):
            dest = self.root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / name, dest)
            self.files.append(name)

    def test_valid_approved_policy(self):
        self.assertEqual(verify(self.root, self.files), [])

    def test_changed_project_is_rejected(self):
        with (self.root / ".zzzops/PROJECT.md").open("a", encoding="utf-8") as out:
            out.write("\nsynthetic unauthorized edit\n")
        self.assertIn("ZzzOps project content digest mismatch",
                      verify(self.root, self.files))

    def test_model_binary_is_rejected(self):
        (self.root / "fake.safetensors").write_bytes(b"synthetic placeholder")
        self.assertIn("prohibited file type: fake.safetensors",
                      verify(self.root, self.files + ["fake.safetensors"]))


if __name__ == "__main__":
    unittest.main()
