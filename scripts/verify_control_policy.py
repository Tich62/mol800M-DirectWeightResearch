#!/usr/bin/env python3
"""Offline ZzzOps policy verification; no model, network, or secrets."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

EXPECTED_REPOSITORY = "Tich62/mol800M-DirectWeightResearch"
FORBIDDEN_SUFFIXES = {
    ".safetensors", ".gguf", ".pt", ".pth", ".bin", ".parquet",
    ".db", ".sqlite", ".pem", ".pfx", ".key", ".onnx", ".env",
}
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


def verify(root, files=None):
    root = Path(root).resolve()
    failures = []
    project = root / ".zzzops/PROJECT.md"
    policy_path = root / ".zzzops/POLICY.json"
    audit = root / ".zzzops/PROJECT_AUDIT.md"
    agents = root / "AGENTS.md"
    for path in (root / "README.md", project, policy_path, audit, agents):
        if not path.is_file():
            failures.append("missing control file: " + str(path.relative_to(root)))
    if failures:
        return failures
    try:
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
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
        path = root / relative
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            failures.append("prohibited file type: " + relative)
            continue
        if not path.is_file() or path.stat().st_size > 256000:
            continue
        try:
            contents = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append("non-text control source: " + relative)
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
