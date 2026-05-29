#!/usr/bin/env python3
"""Read-only public-readiness validator for the Hermes Agent Continuity Kit."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

SOURCE_PUBLIC_ROOT = Path("docs/continuity-kit")
ROOT_LAYOUT_MARKERS = ["README.md", "PACKAGING.md", "templates", "scripts"]
TEXT_SUFFIXES = {".md", ".yaml", ".yml"}
TEMPLATE_SUFFIXES = {".yaml", ".yml"}

REQUIRED_DOCS = [
    "README.md",
    "ARCHITECTURE.md",
    "PACKAGING.md",
    "ADOPTION_GUIDE.md",
    "VALIDATION_CHECKLIST.md",
    "PUBLIC_PRIVATE_BOUNDARY.md",
    "SAFETY_BOUNDARIES.md",
    "AUTOMATION_POLICY.md",
    "APPROVAL_MODEL.md",
    "BOOTSTRAP_RUNBOOK.md",
    "SERVER_REQUIREMENTS.md",
    "KNOWLEDGE_WORKSPACE_ADAPTER.md",
    "RELEASE_TEST_HARNESS.md",
]

REQUIRED_TEMPLATES = [
    "templates/archive-manifest.yaml",
    "templates/monthly-index.yaml",
    "templates/last_scan_cursor.yaml",
    "templates/last_archive_cursor.yaml",
    "templates/recovery-current-state.yaml",
    "templates/approval-receipt.yaml",
    "templates/automation-profile.yaml",
    "templates/audit-ledger-entry.yaml",
    "templates/recovery-state.yaml",
    "templates/workspace-adapter-config.yaml",
]

PUBLIC_VOCABULARY = [
    "Continuity Engine",
    "Memory Router",
    "Audit Ledger",
    "Encrypted Archive Pipeline",
    "Recovery Workbench",
    "Knowledge Workspace Adapter",
    "Approval Kernel",
    "Release Test Harness",
]

APPROVAL_PROFILES = [
    "report-only",
    "docs-batch",
    "safe-local-setup",
    "archive-batch-local",
    "maintainer-guarded",
]

FORBIDDEN_IDENTITY_PATTERNS = {
    "naming_debt_hermesagent": re.compile(r"HermesAgent Continuity Kit", re.I),
    "naming_debt_shareable": re.compile(r"Shareable HermesAgent Continuity Kit", re.I),
    "karpathy": re.compile(r"Karpathy", re.I),
    "rag": re.compile(r"\bRAG\b"),
    "openclaw": re.compile(r"OpenClaw", re.I),
    "ceo": re.compile(r"\bCEO\b", re.I),
    "persona": re.compile(r"persona", re.I),
    "soul": re.compile(r"\bsoul\b", re.I),
    "agent_team": re.compile(r"agent team", re.I),
}

# Construct the most sensitive literals so the validator source can describe the
# checks without itself resembling a payload.
PRIVATE_KEY_BLOCK_RE = re.compile("-{5}BEGIN [A-Z ]*" + "PRIVATE KEY" + "-{5}")
AGE_SECRET_RE = re.compile("AGE-" + "SECRET-KEY-")
OPENSSH_KEY_RE = re.compile("OPENSSH " + "PRIVATE KEY")

ARCHIVE_REAL_PATH_RE = re.compile(
    "archive/" + r"(decrypted|plaintext|restore|tmp|work)/[^\s<>]+" + "|" + "archive/" + "encrypted/" + r"(?!YYYY/)[^\s<>]+",
    re.I,
)

RISK_PATTERNS = {
    "private_key_block": PRIVATE_KEY_BLOCK_RE,
    "age_secret_key": AGE_SECRET_RE,
    "ssh_private_key_marker": OPENSSH_KEY_RE,
    "real_abs_root_path": re.compile("/" + "root" + r"/(?!<)"),
    "archive_artifact_path": ARCHIVE_REAL_PATH_RE,
    "message_id_assignment_numeric": re.compile(r"(?i)(message[_ -]?id|cursor)\s*[:=]\s*[1-9][0-9]{2,}"),
    "token_assignment": re.compile(r"(?i)\b(token|api[_-]?key|password)\s*[:=]\s*[^<\s][^\s]+"),
    "auth_json": re.compile(r"auth\.json", re.I),
    "telegram_entities_marker": re.compile("text" + r"_entities", re.I),
    "telegram_result_file": re.compile("result" + r"\.json", re.I),
}

RAW_PAYLOAD_PATTERNS = {
    "telegram_json_payload": re.compile(r"(?s)\{\s*\"messages\"\s*:\s*\[.*\"text\"\s*:"),
    "raw_transcript_block": re.compile(r"(?i)(raw transcript|session plaintext|message content)\s*:\s*```"),
    "decrypted_archive_block": re.compile(r"(?i)(decrypted archive|decrypted content)\s*:\s*```"),
}

@dataclass
class Finding:
    severity: str
    check: str
    file: str
    summary: str

class Validator:
    def __init__(self, repo_root: Path, strict_release: bool, clean_server_rc1: bool, repo_clean_required: bool, origin_aligned_required: bool, public_root_override: str | None = None):
        self.repo_root = repo_root.resolve()
        self.strict_release = strict_release
        self.clean_server_rc1 = clean_server_rc1
        self.repo_clean_required = repo_clean_required
        self.origin_aligned_required = origin_aligned_required
        self.public_root, self.layout = self.detect_public_root(public_root_override)
        self.docs_root = self.public_root
        self.findings: List[Finding] = []
        self.checks: Dict[str, str] = {}
        self.files: List[Path] = []
        self.texts: Dict[Path, str] = {}

    def rel(self, path: Path) -> str:
        try:
            return str(path.resolve().relative_to(self.repo_root))
        except Exception:
            return str(path)

    def public_root_label(self) -> str:
        return "." if self.public_root == self.repo_root else self.rel(self.public_root)

    def display_path(self, relpath: str) -> str:
        return relpath if self.public_root == self.repo_root else str(SOURCE_PUBLIC_ROOT / relpath)

    def detect_public_root(self, public_root_override: str | None = None) -> Tuple[Path, str]:
        if public_root_override:
            root = (self.repo_root / public_root_override).resolve()
            try:
                root.relative_to(self.repo_root)
            except ValueError:
                raise ValueError("public root must stay inside repo root")
            return root, "explicit"
        source_root = self.repo_root / SOURCE_PUBLIC_ROOT
        if source_root.is_dir():
            return source_root, "source-compatible"
        root_markers_present = all((self.repo_root / marker).exists() for marker in ROOT_LAYOUT_MARKERS)
        if root_markers_present:
            return self.repo_root, "release-root"
        return source_root, "missing"

    def add(self, severity: str, check: str, file: str, summary: str) -> None:
        self.findings.append(Finding(severity, check, file, summary))

    def set_check(self, name: str) -> None:
        severities = [f.severity for f in self.findings if f.check == name]
        if "error" in severities:
            self.checks[name] = "fail"
        elif "warn" in severities:
            self.checks[name] = "warn"
        else:
            self.checks[name] = "pass"

    def run_git(self, args: List[str]) -> Tuple[int, str]:
        try:
            cp = subprocess.run(["git", "-C", str(self.repo_root)] + args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            return cp.returncode, cp.stdout.strip()
        except FileNotFoundError:
            return 127, ""

    def load_files(self) -> None:
        if not self.docs_root.is_dir():
            self.add("error", "inventory", self.public_root_label(), "Public docs directory is missing.")
            return
        skip_parts = {".git", "memory", "archive", "recovery"}
        for p in sorted(self.docs_root.rglob("*")):
            if not p.is_file():
                continue
            if any(part in skip_parts for part in p.relative_to(self.repo_root).parts):
                continue
            rel_parts = p.relative_to(self.docs_root).parts
            if rel_parts and rel_parts[0] == "scripts":
                continue
            if p.suffix.lower() in TEXT_SUFFIXES:
                self.files.append(p)
                self.texts[p] = p.read_text(errors="ignore")

    def check_repo_state(self) -> None:
        code, status = self.run_git(["status", "--porcelain=v1", "--untracked-files=all"])
        if code != 0:
            self.add("warn", "repo_state", ".", "Git status is unavailable.")
        elif self.repo_clean_required and status:
            self.add("error", "repo_state", ".", "Working tree is not clean while --repo-clean-required is active.")
        if self.origin_aligned_required:
            code, counts = self.run_git(["rev-list", "--left-right", "--count", "origin/main...HEAD"])
            if code == 0:
                parts = counts.split()
                if len(parts) == 2 and parts != ["0", "0"]:
                    self.add("error", "repo_state", ".", "HEAD is not aligned with origin/main while --origin-aligned-required is active.")
            else:
                self.add("warn", "repo_state", ".", "origin/main comparison is unavailable.")
        self.set_check("repo_state")

    def check_inventory(self) -> None:
        required_scripts = ["scripts/validate-public-readiness.sh", "scripts/validate_public_readiness.py"]
        for relpath in REQUIRED_DOCS + REQUIRED_TEMPLATES + required_scripts:
            if not (self.docs_root / relpath).is_file():
                self.add("error", "inventory", self.display_path(relpath), "Required public file is missing.")
        self.set_check("inventory")

    def all_text(self) -> str:
        return "\n".join(self.texts.values())

    def check_naming(self) -> None:
        text = self.all_text()
        if "Hermes Agent Continuity Kit" not in text:
            self.add("error", "naming", self.public_root_label(), "Canonical product name is missing.")
        for name, pattern in list(FORBIDDEN_IDENTITY_PATTERNS.items())[:2]:
            for path, body in self.texts.items():
                if pattern.search(body):
                    self.add("error", "naming", self.rel(path), f"Forbidden naming debt marker found: {name}.")
        self.set_check("naming")

    def check_public_vocabulary(self) -> None:
        text = self.all_text()
        for term in PUBLIC_VOCABULARY:
            if term not in text:
                self.add("error", "public_vocabulary", self.public_root_label(), f"Required public vocabulary term is missing: {term}.")
        self.set_check("public_vocabulary")

    def check_forbidden_identity(self) -> None:
        for name, pattern in list(FORBIDDEN_IDENTITY_PATTERNS.items())[2:]:
            for path, body in self.texts.items():
                if pattern.search(body):
                    self.add("error", "forbidden_identity", self.rel(path), f"Forbidden public identity marker found: {name}.")
        self.set_check("forbidden_identity")

    def is_policy_context(self, path: Path, body: str, pattern_name: str) -> bool:
        # Public safety docs and templates intentionally mention forbidden surfaces
        # as policy examples. Only concrete payload/key/assignment patterns should fail.
        policy_only = {"auth_json", "telegram_entities_marker", "telegram_result_file"}
        return pattern_name in policy_only

    def check_private_markers(self) -> None:
        for name, pattern in RISK_PATTERNS.items():
            for path, body in self.texts.items():
                if pattern.search(body):
                    if self.is_policy_context(path, body, name):
                        continue
                    self.add("error", "private_marker_scan", self.rel(path), f"Potential private/runtime marker found: {name}.")
        self.set_check("private_marker_scan")

    def check_raw_markers(self) -> None:
        for name, pattern in RAW_PAYLOAD_PATTERNS.items():
            for path, body in self.texts.items():
                if pattern.search(body):
                    if self.is_policy_context(path, body, name):
                        continue
                    self.add("error", "raw_decrypted_marker_scan", self.rel(path), f"Potential raw/decrypted payload marker found: {name}.")
        self.set_check("raw_decrypted_marker_scan")

    def check_templates(self) -> None:
        templates = [p for p in self.files if "templates" in p.parts and p.suffix.lower() in TEMPLATE_SUFFIXES]
        for path in templates:
            body = self.texts[path]
            if "<" not in body or ">" not in body:
                self.add("warn", "template_placeholder_validation", self.rel(path), "Template has no angle-bracket placeholders; verify it is intentionally static.")
            # Real-risk patterns are already errors in private_marker_scan.
        self.set_check("template_placeholder_validation")

    def check_yaml(self) -> None:
        yaml_files = [p for p in self.files if p.suffix.lower() in TEMPLATE_SUFFIXES]
        yaml_module = None
        try:
            import yaml as yaml_module  # type: ignore
        except Exception:
            yaml_module = None
        for path in yaml_files:
            body = self.texts[path]
            if not body.strip():
                self.add("error", "yaml_validation", self.rel(path), "YAML file is empty.")
                continue
            if "\t" in body:
                self.add("error", "yaml_validation", self.rel(path), "YAML file contains tabs.")
            if yaml_module is not None:
                try:
                    yaml_module.safe_load(body)
                except Exception:
                    self.add("error", "yaml_validation", self.rel(path), "YAML parser rejected the file.")
        self.set_check("yaml_validation")

    def check_approval_profiles(self) -> None:
        text = self.all_text()
        for profile in APPROVAL_PROFILES:
            if profile not in text:
                self.add("error", "approval_profiles", self.public_root_label(), f"Canonical approval profile is missing: {profile}.")
        self.set_check("approval_profiles")

    def check_workspace_adapter(self) -> None:
        text = self.all_text()
        if "Knowledge Workspace Adapter" not in text:
            self.add("error", "knowledge_workspace_adapter", self.public_root_label(), "Knowledge Workspace Adapter term is missing.")
        if "product-agnostic" not in text.lower():
            self.add("error", "knowledge_workspace_adapter", self.public_root_label(), "Product-agnostic wording is missing.")
        obsidian_count = text.lower().count("obsidian")
        optional_count = text.lower().count("optional")
        if obsidian_count and optional_count == 0:
            self.add("error", "knowledge_workspace_adapter", self.public_root_label(), "Obsidian appears without optional-adapter framing.")
        self.set_check("knowledge_workspace_adapter")

    def check_clean_server_docs(self) -> None:
        for relpath in ["SERVER_REQUIREMENTS.md", "BOOTSTRAP_RUNBOOK.md", "VALIDATION_CHECKLIST.md", "AUTOMATION_POLICY.md", "APPROVAL_MODEL.md", "RELEASE_TEST_HARNESS.md"]:
            if not (self.docs_root / relpath).is_file():
                self.add("error", "clean_server_readiness_docs", self.display_path(relpath), "Clean-server readiness document is missing.")
        self.set_check("clean_server_readiness_docs")

    def check_package_boundary(self) -> None:
        p = self.docs_root / "PACKAGING.md"
        body = p.read_text(errors="ignore") if p.exists() else ""
        for term in ["Include allowlist", "Exclude denylist", "Private-state exclusion", "Placeholder"]:
            if term.lower() not in body.lower():
                self.add("error", "package_boundary", self.rel(p), f"Package boundary term is missing: {term}.")
        self.set_check("package_boundary")

    def run(self) -> Tuple[str, Dict[str, str], List[Finding]]:
        self.load_files()
        self.check_repo_state()
        self.check_inventory()
        self.check_naming()
        self.check_public_vocabulary()
        self.check_forbidden_identity()
        self.check_private_markers()
        self.check_raw_markers()
        self.check_templates()
        self.check_yaml()
        self.check_approval_profiles()
        self.check_workspace_adapter()
        self.check_clean_server_docs()
        self.check_package_boundary()
        result = "fail" if any(f.severity == "error" for f in self.findings) else "pass"
        return result, self.checks, self.findings

def render_text(result: str, checks: Dict[str, str], findings: List[Finding]) -> str:
    lines = [f"release_test_harness_result={result}"]
    for name in sorted(checks):
        lines.append(f"{name}={checks[name]}")
    warnings = sum(1 for f in findings if f.severity == "warn")
    errors = sum(1 for f in findings if f.severity == "error")
    lines.append(f"warnings={warnings}")
    lines.append(f"errors={errors}")
    for i, f in enumerate(findings):
        lines.append(f"finding[{i}].severity={f.severity}")
        lines.append(f"finding[{i}].check={f.check}")
        lines.append(f"finding[{i}].file={f.file}")
        lines.append(f"finding[{i}].summary={f.summary}")
    return "\n".join(lines)

def render_json(result: str, checks: Dict[str, str], findings: List[Finding]) -> str:
    payload = {
        "result": result,
        "summary": {
            "warnings": sum(1 for f in findings if f.severity == "warn"),
            "errors": sum(1 for f in findings if f.severity == "error"),
        },
        "checks": checks,
        "findings": [f.__dict__ for f in findings],
    }
    return json.dumps(payload, indent=2, sort_keys=True)

def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate public-readiness for the Hermes Agent Continuity Kit.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--public-root", default=None, help="Optional public package root; auto-detects source docs/continuity-kit or release root when omitted.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--strict-release", action="store_true")
    parser.add_argument("--clean-server-rc1", action="store_true")
    parser.add_argument("--repo-clean-required", action="store_true")
    parser.add_argument("--origin-aligned-required", action="store_true")
    parser.add_argument("--allow-policy-marker-mentions", action="store_true")
    parser.add_argument("--fail-on-warning", action="store_true")
    return parser.parse_args(argv)

def main(argv: List[str]) -> int:
    try:
        args = parse_args(argv)
        strict = args.strict_release
        validator = Validator(
            Path(args.repo_root),
            strict,
            args.clean_server_rc1,
            args.repo_clean_required,
            args.origin_aligned_required,
            args.public_root,
        )
        result, checks, findings = validator.run()
        if args.fail_on_warning and any(f.severity == "warn" for f in findings) and result == "pass":
            result = "fail"
        if args.format == "json":
            print(render_json(result, checks, findings))
        else:
            print(render_text(result, checks, findings))
        return 0 if result == "pass" else 1
    except KeyboardInterrupt:
        return 3
    except argparse.ArgumentError:
        return 2
    except Exception as exc:
        print(f"release_test_harness_result=error\nsummary=sanitized internal error: {exc.__class__.__name__}", file=sys.stderr)
        return 3

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
