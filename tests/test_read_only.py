"""Enforce the read-only promise.

The analyzer is offline file analysis only. This test fails if Python under
src/ imports, or pyproject.toml depends on, a library that can reach a
vehicle, an adapter, or the network.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
PYPROJECT = ROOT / "pyproject.toml"

# Whole names only, after PEP 503-style normalization. The first group is the
# review list. The second group is similar vehicle, adapter, and network
# access libraries.
BANNED = frozenset(
    {
        "serial",
        "pyserial",
        "can",
        "python-can",
        "obd",
        "pyobd",
        "pyftdi",
        "socket",
        "bluetooth",
        "usb",
        "pyusb",
        "ftd2xx",
        "subprocess",
        "requests",
        "urllib",
        "urllib3",
        "http",
        "httpx",
        "aiohttp",
        "websockets",
        "websocket-client",
        "bleak",
        "pybluez",
        "udsoncan",
        "cantools",
        "can-isotp",
        "elm327",
        "j2534",
        "pylibftdi",
        "socketserver",
        "telnetlib",
        "ftplib",
        "smtplib",
        "poplib",
        "imaplib",
    }
)


def _normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name.strip().lower())


def _is_banned(name: str) -> bool:
    return _normalize(name) in BANNED


def _requirement_name(requirement: str) -> str:
    requirement = requirement.split(";", 1)[0].strip()
    requirement = requirement.split("@", 1)[0].strip()
    requirement = re.split(r"\s|[<>=!~\[]", requirement, maxsplit=1)[0]
    return _normalize(requirement)


def _strip_comment(line: str) -> str:
    out: list[str] = []
    quote: str | None = None
    i = 0
    while i < len(line):
        ch = line[i]
        if quote:
            out.append(ch)
            if quote == '"' and ch == "\\" and i + 1 < len(line):
                out.append(line[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in {'"', "'"}:
            quote = ch
            out.append(ch)
            i += 1
            continue
        if ch == "#":
            break
        out.append(ch)
        i += 1
    return "".join(out)


def _read_assignment(lines: list[str], start: int) -> tuple[str, int]:
    """Read one assignment, including a multi-line array, starting at start."""
    chunks: list[str] = []
    depth = 0
    started = False
    quote: str | None = None
    i = start
    while i < len(lines):
        piece = _strip_comment(lines[i])
        chunks.append(piece)
        j = 0
        while j < len(piece):
            ch = piece[j]
            if quote:
                if quote == '"' and ch == "\\" and j + 1 < len(piece):
                    j += 2
                    continue
                if ch == quote:
                    quote = None
                j += 1
                continue
            if ch in {'"', "'"}:
                quote = ch
            elif ch == "[":
                depth += 1
                started = True
            elif ch == "]":
                depth -= 1
            j += 1
        i += 1
        if started and depth == 0 and quote is None:
            break
        if not started and i > start and "=" in chunks[0] and "[" not in chunks[0]:
            break
    return "\n".join(chunks), i


def declared_dependency_names(text: str) -> list[str]:
    """Return normalized names from project dependencies and optional extras.

    Parses the subset of TOML this repository uses. The standard library has
    no TOML parser on Python 3.10, and this test stays stdlib only.
    """
    names: list[str] = []
    section = ""
    lines = text.splitlines()
    i = 0
    saw_project = False
    while i < len(lines):
        line = _strip_comment(lines[i]).strip()
        if not line:
            i += 1
            continue
        if line.startswith("[") and line.endswith("]") and "=" not in line:
            section = line[1:-1].strip().strip('"').strip("'")
            if section == "project":
                saw_project = True
            i += 1
            continue
        in_project_deps = section == "project" and line.startswith("dependencies")
        in_extra = section == "project.optional-dependencies" or section.startswith(
            "project.optional-dependencies."
        )
        if (in_project_deps or in_extra) and "=" in line:
            assignment, i = _read_assignment(lines, i)
            value = assignment.split("=", 1)[1].strip()
            try:
                items = ast.literal_eval(value)
            except (SyntaxError, ValueError) as exc:
                raise AssertionError(
                    f"Could not parse dependencies in [{section}]: {exc}"
                ) from exc
            if not isinstance(items, list) or not all(isinstance(item, str) for item in items):
                raise AssertionError(f"Dependencies in [{section}] are not a list of strings")
            names.extend(_requirement_name(item) for item in items)
            continue
        i += 1
    if not saw_project:
        raise AssertionError("pyproject.toml has no [project] table")
    return names


def imported_roots(tree: ast.AST) -> list[str]:
    roots: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.append(alias.name.split(".", 1)[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                roots.append(node.module.split(".", 1)[0])
        elif isinstance(node, ast.Call):
            func = node.func
            is_import = (isinstance(func, ast.Name) and func.id == "__import__") or (
                isinstance(func, ast.Attribute) and func.attr == "import_module"
            )
            if (
                is_import
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            ):
                roots.append(node.args[0].value.split(".", 1)[0])
    return roots


def collect_violations() -> list[str]:
    violations: list[str] = []
    if not SRC.is_dir():
        return ["src/ is missing"]
    for path in sorted(SRC.rglob("*.py")):
        source = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            violations.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        for root in imported_roots(tree):
            if _is_banned(root):
                violations.append(
                    f"{path.relative_to(ROOT)} imports {root}, which can reach a vehicle or the network"
                )
    if not PYPROJECT.is_file():
        violations.append("pyproject.toml is missing")
        return violations
    for name in declared_dependency_names(PYPROJECT.read_text(encoding="utf-8")):
        if _is_banned(name):
            violations.append(
                f"pyproject.toml depends on {name}, which can reach a vehicle or the network"
            )
    return violations


def test_project_stays_read_only():
    violations = collect_violations()
    assert not violations, "Read-only promise violated:\n" + "\n".join(violations)
