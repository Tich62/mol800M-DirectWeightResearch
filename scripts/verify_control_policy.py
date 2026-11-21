#!/usr/bin/env python3
"""Offline ZzzOps policy verification; no model, network, or secrets."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

EXPECTED_REPOSITORY = "Tich62/mol800M-DirectWeightResearch"
MAX_CONTROL_FILE_BYTES = 256_000
# SHA-256 of the exact policy bytes from the separately approved control PR head.
# This pin is review-bound, NOT a signature or standalone owner authorization.
# Any legitimate policy revision requires its own review and an updated pin.
EXPECTED_REVIEWED_POLICY_SHA256 = "49bee026d18ff566808672a03cc0983b698e47b69f68b55999effbc19a3cc684"
# This is a control-only repo: new paths need an explicit code review.
ALLOWED_SOURCE_FILES = frozenset({
    "README.md", "AGENTS.md",
    ".zzzops/.gitignore", ".zzzops/PROJECT.md",
    ".zzzops/POLICY.json", ".zzzops/PROJECT_AUDIT.md",
    ".github/workflows/verify-control.yml",
    "scripts/verify_control_policy.py",
    "scripts/test_verify_control_policy.py",
})
FORBIDDEN_SUFFIXES = {
    ".safetensors", ".gguf", ".pt", ".pth", ".bin", ".parquet",
    ".db", ".sqlite", ".pem", ".pfx", ".key", ".onnx", ".env",
    ".ckpt",
}
FORBIDDEN_FILENAMES = frozenset({".npmrc", ".pypirc", ".netrc", "id_rsa", "id_ed25519"})
FORBIDDEN_CONTENT = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:ghp_|gho_|ghu_|ghs_|github_pat_)[A-Za-z0-9_]{20,}"),
    re.compile(r"\b[A-Za-z]:[\\/]"),
)


def _digest(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _source_files(root):
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "--others",
         "--exclude-standard"], capture_output=True, text=True, check=True,
    )
    return sorted(set(result.stdout.splitlines()))


def _linked_path(path, root):
    """Reject symlinks and Windows directory junctions before any file read."""
    current = path
    while current != root:
        if (current.is_symlink() or
                getattr(current, "is_junction", lambda: False)()):
            return True
        current = current.parent
    return False


def verify(root, files=None):
    root = Path(root).resolve()
    failures = []
    project = root / ".zzzops/PROJECT.md"
    policy_path = root / ".zzzops/POLICY.json"
    audit = root / ".zzzops/PROJECT_AUDIT.md"
    agents = root / "AGENTS.md"
    for path in (root / "README.md", project, policy_path, audit, agents):
        relative = path.relative_to(root).as_posix()
        if _linked_path(path, root):
            failures.append("linked control file forbidden: " + relative)
        elif not path.is_file():
            failures.append("missing control file: " + relative)
        else:
            try:
                if path.stat().st_size > MAX_CONTROL_FILE_BYTES:
                    failures.append("oversized control file: " + relative)
            except OSError:
                failures.append("cannot inspect control file: " + relative)
    if failures:
        return failures
    try:
        # A syntactically valid, but unreviewed, POLICY.json must not pass.
        # Verify raw bytes before parsing so JSON reformatting also needs review.
        policy_bytes = policy_path.read_bytes()
        if hashlib.sha256(policy_bytes).hexdigest() != EXPECTED_REVIEWED_POLICY_SHA256:
            failures.append("policy bytes differ from reviewed source snapshot")
        policy = json.loads(policy_bytes.decode("utf-8"))
        if policy.get("initialized") is not True:
            failures.append("ZzzOps project not initialized")
        if policy.get("backend") != "github_issues":
            failures.append("unexpected goal backend")
        if policy.get("repository", {}).get("identity") != EXPECTED_REPOSITORY:
            failures.append("wrong repository identity")
        sections = policy.get("policy", {}).get("sections", [])
        if len(sections) != 13 or not all(
            item.get("review", {}).get("approved") is True for item in sections
        ):
            failures.append("all 13 policy sections must be approved")
        approval = policy.get("approval")
        if not isinstance(approval, dict) or not re.fullmatch(
            r"sha256:[0-9a-f]{64}", str(approval.get("digest", ""))
        ):
            failures.append("missing source-bound policy approval")
        bindings = policy.get("bindings", {})
        for key, path in (("project", project), ("audit", audit)):
            if bindings.get(key, {}).get("digest") != _digest(path):
                failures.append("ZzzOps " + key + " content digest mismatch")
    except (TypeError, ValueError, KeyError) as error:
        failures.append("invalid control policy: " + type(error).__name__)
    agent_text = agents.read_text(encoding="utf-8")
    if ("<!-- BEGIN ZZZOPS WORKFLOW ADHERENCE -->" not in agent_text or
        "<!-- END ZZZOPS WORKFLOW ADHERENCE -->" not in agent_text):
        failures.append("missing bounded agent instructions")
    if files is None:
        try:
            files = _source_files(root)
        except (OSError, subprocess.CalledProcessError):
            return failures + ["cannot enumerate git source files"]
    for relative in files:
        # Files from Git use forward slashes; reject any other path grammar.
        if (not isinstance(relative, str) or not relative
                or relative.startswith("/") or "\\" in relative
                or ":" in relative or any(
                    component in ("", ".", "..") for component in relative.split("/")
                )):
            failures.append("unsafe control path: " + str(relative))
            continue
        path = root / relative
        name = path.name.casefold()
        if name == ".env" or name.startswith(".env.") or name in FORBIDDEN_FILENAMES:
            failures.append("prohibited sensitive filename: " + relative)
            continue
        if path.suffix.casefold() in FORBIDDEN_SUFFIXES:
            failures.append("prohibited file type: " + relative)
            continue
        if relative not in ALLOWED_SOURCE_FILES:
            failures.append("unapproved control file: " + relative)
            continue
        if _linked_path(path, root):
            failures.append("linked control file forbidden: " + relative)
            continue
        if not path.is_file():
            failures.append("missing source file: " + relative)
            continue
        try:
            if path.stat().st_size > MAX_CONTROL_FILE_BYTES:
                failures.append("oversized control file: " + relative)
                continue
            contents = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append("non-text control source: " + relative)
            continue
        except OSError:
            failures.append("unreadable control source: " + relative)
            continue
        if any(pattern.search(contents) for pattern in FORBIDDEN_CONTENT):
            failures.append("prohibited sensitive pattern: " + relative)
    return failures


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    problems = verify(root)
    for problem in problems:
        print("FAIL:", problem)
    if problems:
        raise SystemExit(1)
    print("PASS: ZzzOps policy bindings and control-only source checks")
