"""Synthetic-only tests of the ZzzOps source-bound policy check."""
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
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

    def test_secret_dotfiles_are_rejected(self):
        for name in (".env", ".env.local", ".npmrc", ".pypirc"):
            with self.subTest(name=name):
                path = self.root / name
                path.write_text("SYNTHETIC_CONFIG=not_a_secret\n", encoding="utf-8")
                self.assertTrue(
                    verify(self.root, self.files + [name]),
                    f"{name} must not enter the control repository",
                )
                path.unlink()

    def test_model_checkpoint_extensions_are_rejected(self):
        for name in ("weights.ckpt", "model.CKPT", "adapter.gguf", "weights.pth"):
            with self.subTest(name=name):
                path = self.root / name
                path.write_bytes(b"synthetic model placeholder")
                self.assertTrue(
                    verify(self.root, self.files + [name]),
                    f"{name} must be rejected",
                )
                path.unlink()

    def test_oversized_unknown_file_is_rejected(self):
        name = "large_notes.txt"
        (self.root / name).write_bytes(
            b"synthetic note " * 23000 + b"github_pat_" + b"A" * 32
        )
        self.assertTrue(verify(self.root, self.files + [name]))

    def test_oversized_allowed_file_is_rejected(self):
        (self.root / "AGENTS.md").write_bytes(b"synthetic text " * 23000)
        self.assertIn("oversized control file: AGENTS.md",
                      verify(self.root, self.files))

    def test_unapproved_regular_control_file_is_rejected(self):
        name = "unapproved.txt"
        (self.root / name).write_text("harmless synthetic content", encoding="utf-8")
        self.assertTrue(verify(self.root, self.files + [name]))

    def test_directory_traversal_is_rejected(self):
        self.assertTrue(verify(self.root, self.files + ["../outside.txt"]))

    def test_absolute_file_path_is_rejected(self):
        self.assertTrue(verify(self.root, self.files + [str(self.root / "README.md")]))

    def test_external_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "external.txt"
            source.write_text("SYNTHETIC_CONFIG=sample", encoding="utf-8")
            link = self.root / "AGENTS.md"
            link.unlink()
            try:
                link.symlink_to(source)
            except (OSError, NotImplementedError) as error:
                self.skipTest(f"file symlinks unavailable on this host: {error}")
            self.assertTrue(verify(self.root, self.files))

    def test_mocked_symlink_fails_closed_without_privilege(self):
        link = self.root / "AGENTS.md"
        original = Path.is_symlink

        def mock_symlink(path):
            return path == link or original(path)

        with patch.object(Path, "is_symlink", mock_symlink):
            self.assertIn("linked control file forbidden: AGENTS.md",
                          verify(self.root, self.files))

    def test_changed_policy_is_rejected(self):
        with (self.root / ".zzzops/POLICY.json").open("a", encoding="utf-8") as out:
            out.write("\nsynthetic unauthorized change\n")
        self.assertTrue(verify(self.root, self.files))

    def test_valid_control_files_remain_accepted(self):
        self.assertEqual(verify(self.root, self.files), [])


if __name__ == "__main__":
    unittest.main()
