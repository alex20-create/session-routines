"""List every graphify-out/ under a root and say whether its graph is stale.

Usage: python find_graphs.py <root> [<root> ...]

For each graphify-out/ found (at most 3 levels deep, skipping .git and
node_modules), compares the corpus on disk with the manifest graphify wrote
on its last run. Prints one line per graph:

    STALE     ~/notes/vault    2 changed, 0 deleted
    CURRENT   ~/code/my-app    no changes
    UNKNOWN   ~/some/dir       no manifest.json

Exit code is 0 either way; the output is meant to be read, not tested.

Needs the graphify package (PyPI name `graphifyy`). Any Python can launch
this script: if graphify is not importable here, it re-runs itself with the
interpreter graphify recorded in the first `graphify-out/.graphify_python`
it finds, which is by construction one that has the package.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# Folders not worth walking into when looking for graphify-out/. What counts
# as corpus inside a graph is graphify's own business: it honours a
# .graphifyignore at the graph root, so put exclusions there, not here.
SKIP_DIRS = {".git", "node_modules", ".obsidian", ".trash"}
MAX_DEPTH = 3


def find_graph_roots(root: Path) -> list[Path]:
    found: list[Path] = []
    root = root.resolve()
    for dirpath, dirnames, _ in os.walk(root):
        rel_depth = len(Path(dirpath).relative_to(root).parts)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if "graphify-out" in dirnames:
            found.append(Path(dirpath))
            dirnames.remove("graphify-out")
        if rel_depth >= MAX_DEPTH:
            dirnames[:] = []
    return found


def status(graph_root: Path) -> tuple[str, str]:
    out = graph_root / "graphify-out"
    if not (out / "manifest.json").exists():
        return "UNKNOWN", "no manifest.json"
    try:
        from graphify.detect import detect_incremental
    except ImportError:
        return "UNKNOWN", "graphify not importable from this interpreter"
    cwd = os.getcwd()
    try:
        # detect_incremental reads graphify-out/ relative to the cwd.
        os.chdir(graph_root)
        result = detect_incremental(Path("."))
    finally:
        os.chdir(cwd)
    changed = [f for files in result.get("new_files", {}).values() for f in files]
    deleted = list(result.get("deleted_files", []))
    if not changed and not deleted:
        return "CURRENT", "no changes"
    return "STALE", f"{len(changed)} changed, {len(deleted)} deleted"


def _graphify_available() -> bool:
    try:
        import graphify  # noqa: F401
    except ImportError:
        return False
    return True


def _reexec_with_recorded_interpreter(graphs: list[Path], argv: list[str]) -> int | None:
    """Re-run this script under the interpreter a graph recorded, if any."""
    for g in graphs:
        marker = g / "graphify-out" / ".graphify_python"
        if not marker.exists():
            continue
        interpreter = marker.read_text(encoding="utf-8").strip()
        if interpreter and Path(interpreter).exists() and Path(interpreter).resolve() != Path(sys.executable).resolve():
            return subprocess.call([interpreter, "-X", "utf8", *argv])
    return None


def main(argv: list[str]) -> int:
    roots = [Path(a) for a in argv[1:]] or [Path(".")]
    graphs: list[Path] = []
    for r in roots:
        graphs.extend(find_graph_roots(r))
    if not graphs:
        print("No graphify-out/ found under", ", ".join(str(r.resolve()) for r in roots))
        return 0
    if not _graphify_available():
        rc = _reexec_with_recorded_interpreter(graphs, argv)
        if rc is not None:
            return rc
    for g in sorted(set(graphs)):
        state, detail = status(g)
        print(f"{state:<9} {g.as_posix():<45} {detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
