#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vault.py - Tools for keeping an Obsidian vault's project notes in step with
work done in Claude Code.

Python 3.8+ standard library only.

Design principle: this script does NOT write prose. It reads the vault and
replaces specific pieces that Claude hands it, so nothing written by hand is
lost. Every write can be rehearsed first with --dry-run.

Subcommands:
  scan        Inventory of the vault or of one project (JSON on stdout)
  section     Replace the body of one section, found by its heading
  frontmatter Change single frontmatter keys, leaving the rest alone
  log         Record one session's data (hook mode, never touches notes)
  log-merge   Fold worktree logs into their repository's log
  canvas      Report on a .canvas, or add nodes without moving existing ones

Finding the vault: --vault PATH (before or after the subcommand), else the
OBSIDIAN_VAULT environment variable. There is no built-in default: a guessed
path would make scan inspect a folder that does not exist without saying so.
"""

import argparse
import datetime as dt
import difflib
import json
import os
import re
import subprocess
import sys
import unicodedata

MAX_SESSIONS = 20

# Environment variables that name the vault, in order of preference. The
# second is the name older installs used.
VAULT_ENV = ("OBSIDIAN_VAULT", "OBSIDIAN_VAULT_CLAUDE")

# The vault describes itself. The file sits at the root under a fixed name
# because it is the bootstrap: any other location would require already
# knowing how the vault is organised in order to find it.
CONFIG = ".claude-vault.json"

# Fallback values for a vault without a config file. They keep such a vault
# usable; they are not a claim that every vault is organised this way.
DEFAULT_CONFIG = {
    "projects": "Projects",
    "archive": "Archive",
    "logs": "Claude Sync",
    "conventions": "Conventions.md",
}

# Config keys written by earlier versions, which used Spanish names. Still
# read, so an existing vault keeps working; the English key wins when a file
# has both.
CONFIG_ALIASES = {
    "proyectos": "projects",
    "archivo": "archive",
    "registros": "logs",
    "convenciones": "conventions",
}

# Session-log keys written by earlier versions. Logs are rewritten with the
# English keys the next time the hook records a session for that project.
LOG_ALIASES = {
    "sesiones": "sessions",
    "fecha": "date",
    "hora": "time",
    "rama": "branch",
    "archivos": "files",
    "sin_commitear": "uncommitted",
    "carpeta": "folder",
    "carpetas": "folders",
    "proyecto": "project",
    "ruta": "path",
    "ultimo_commit": "last_commit",
    "ultima_sesion": "last_session",
}

# The Windows console defaults to cp1252 and cannot encode emoji. Vault notes
# often carry emoji in their headings, so without this `scan --project` dies
# with UnicodeEncodeError when it serialises the heading list, and so does any
# diff that touches a line with an emoji.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError, OSError):
        # Python < 3.7, or a redirected stdout that cannot be reconfigured.
        # Not a reason to abort: only the emoji on screen is lost.
        pass


class NoVault(Exception):
    pass


# ----------------------------------------------------------------- helpers

def today():
    return dt.date.today().isoformat()


def vault_of(args):
    vault = getattr(args, "vault", None)
    if not vault:
        for name in VAULT_ENV:
            if os.environ.get(name):
                vault = os.environ[name]
                break
    if not vault:
        raise NoVault("No vault given. Pass --vault PATH or set OBSIDIAN_VAULT.")
    vault = os.path.abspath(os.path.expanduser(vault))
    if not os.path.isdir(vault):
        raise NoVault("The vault folder does not exist: {}".format(vault))
    return vault


def config_of(vault):
    """Read .claude-vault.json at the vault root. Never fails.

    Also returns where each value came from, so `scan` can say it and nobody
    has to guess whether they are working on what was declared or on
    assumptions.
    """
    path = os.path.join(vault, CONFIG)
    cfg = dict(DEFAULT_CONFIG)
    source = "defaults"
    problem = None

    if os.path.exists(path):
        try:
            read_back = json.loads(read(path))
            if not isinstance(read_back, dict):
                raise ValueError("the file does not hold a JSON object")
            known = set(DEFAULT_CONFIG) | set(CONFIG_ALIASES)
            unknown = sorted(set(read_back) - known)
            for old, new in CONFIG_ALIASES.items():
                if old in read_back and new not in read_back:
                    read_back[new] = read_back[old]
            for key in DEFAULT_CONFIG:
                value = read_back.get(key)
                if isinstance(value, str) and value.strip():
                    cfg[key] = value.strip()
            source = CONFIG
            if unknown:
                problem = "unused keys: {}".format(", ".join(unknown))
        except Exception as e:
            # A broken config must not bring down the hook or scan, but it
            # must not go unnoticed either: warn and carry on with defaults.
            problem = "{} could not be read ({}); using defaults".format(CONFIG, e)

    cfg = {k: v.replace("/", os.sep) for k, v in cfg.items()}
    cfg["_source"] = source
    if problem:
        cfg["_warning"] = problem
    return cfg


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, content):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    os.replace(tmp, path)


def normalise(text):
    """'## 🚀 Deploy' -> 'deploy'. Matches headings without their emoji."""
    text = text.lstrip("#").strip()
    text = "".join(c for c in text if c.isalnum() or c.isspace())
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", text).strip().lower()


def slug(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s_]+", "-", text) or "project"


def output(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def show_diff(path, old, new, dry_run):
    """Print the diff. Write only when it is not a rehearsal."""
    if old == new:
        print("No changes: the content was already that.")
        return False
    diff = difflib.unified_diff(old.splitlines(), new.splitlines(),
                                fromfile="before", tofile="after", lineterm="", n=2)
    print("\n".join(diff))
    if dry_run:
        print("\n[DRY RUN] Nothing was written.")
    else:
        write(path, new)
        print("\nWritten: {}".format(path))
    return True


# ------------------------------------------------------------- frontmatter

def split(text):
    """Return (raw_frontmatter_block, body). The block comes without the ---."""
    if not text.startswith("---"):
        return None, text
    m = re.search(r"\n---[ \t]*\r?\n", text)
    if not m:
        return None, text
    return text[4:m.start() + 1], text[m.end():]


def parse_frontmatter(raw):
    """Minimal parser: scalars and block lists. No nesting."""
    if not raw:
        return {}
    data, list_key = {}, None
    for line in raw.split("\n"):
        if not line.strip():
            continue
        m = re.match(r"^\s*-\s+(.*)$", line)
        if m and list_key:
            data[list_key].append(m.group(1).strip().strip('"\''))
            continue
        m = re.match(r"^([\w\-]+)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if value == "":
            data[key], list_key = [], key
        else:
            list_key = None
            if value.startswith("[") and value.endswith("]"):
                data[key] = [x.strip().strip('"\'') for x in value[1:-1].split(",") if x.strip()]
            else:
                data[key] = value.strip('"\'')
    return data


def set_key(raw, key, value):
    """Change one scalar key, keeping the rest of the block as it was.
    Return None if the key exists but is a block list."""
    lines = (raw or "").rstrip("\n").split("\n")
    for i, line in enumerate(lines):
        m = re.match(r"^([\w\-]+)\s*:\s*(.*)$", line)
        if m and m.group(1) == key:
            if m.group(2).strip() == "" and i + 1 < len(lines) \
                    and re.match(r"^\s*-\s+", lines[i + 1]):
                return None
            lines[i] = "{}: {}".format(key, value)
            return "\n".join(lines) + "\n"
    lines.append("{}: {}".format(key, value))
    return "\n".join(lines) + "\n"


def assemble(raw, body):
    if raw is None:
        return body
    return "---\n" + raw.rstrip("\n") + "\n---\n" + body


# ---------------------------------------------------------------- sections

def headings(body):
    """(line_index, level, text). Skips anything inside code fences."""
    found, in_code = [], False
    for i, line in enumerate(body.split("\n")):
        if re.match(r"^\s*(```|~~~)", line):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            found.append((i, len(m.group(1)), m.group(2).strip()))
    return found


def locate(body, wanted):
    """Find a section by its heading. Return (start, end, level, text)."""
    target = normalise(wanted)
    lines = body.split("\n")
    heads = headings(body)
    chosen = None
    for idx, (i, level, text) in enumerate(heads):
        n = normalise(text)
        if n == target or (len(target) > 3 and target in n):
            chosen = (idx, i, level, text)
            break
    if not chosen:
        return None
    idx, i, level, text = chosen
    end = len(lines)
    for j, jlevel, _ in heads[idx + 1:]:
        if jlevel <= level:
            end = j
            break
    return i, end, level, text


# --------------------------------------------------------------------- git

def git(repo, *args):
    try:
        r = subprocess.run(["git", "-C", repo] + list(args),
                           capture_output=True, text=True, timeout=20)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


# -------------------------------------------------------------------- scan

def main_note(folder):
    """The note named like the folder; else the only .md; else None."""
    name = os.path.basename(folder.rstrip("\\/"))
    candidate = os.path.join(folder, name + ".md")
    if os.path.exists(candidate):
        return candidate
    notes = [f for f in os.listdir(folder) if f.endswith(".md")]
    return os.path.join(folder, notes[0]) if len(notes) == 1 else None


def folder_inventory(folder):
    files = {"notes": [], "canvas": [], "other": []}
    for root, dirs, names in os.walk(folder):
        # Hidden folders (.obsidian, plugin state such as .space) are not notes.
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in names:
            rel = os.path.relpath(os.path.join(root, f), folder).replace("\\", "/")
            if f.endswith(".md"):
                files["notes"].append(rel)
            elif f.endswith(".canvas"):
                files["canvas"].append(rel)
            else:
                files["other"].append(rel)
    return files


def sessions_since(log, note_path):
    """Sessions recorded after the note last changed on disk.

    A starting point for "what is not in the note yet", not proof: a note can
    be edited for other reasons, and a session can be noted by hand.
    """
    try:
        changed = dt.datetime.fromtimestamp(os.path.getmtime(note_path))
    except OSError:
        return log.get("sessions", [])
    newer = []
    for s in log.get("sessions", []):
        stamp = "{} {}".format(s.get("date", ""), s.get("time") or "23:59")
        try:
            when = dt.datetime.strptime(stamp, "%Y-%m-%d %H:%M")
        except ValueError:
            continue
        if when > changed:
            newer.append(s)
    return newer


def cmd_scan(args):
    vault = vault_of(args)
    cfg = config_of(vault)
    conventions = os.path.join(vault, cfg["conventions"])
    result = {
        "vault": vault,
        "config": {
            "source": cfg["_source"],
            "projects": cfg["projects"],
            "archive": cfg["archive"],
            "logs": cfg["logs"],
            # The vault's conventions note overrides any reference packaged
            # with the skill. Read it before writing.
            "conventions": conventions if os.path.exists(conventions) else None,
        },
        "projects": [], "archived": [], "statuses_in_use": [],
    }
    if cfg.get("_warning"):
        result["config"]["warning"] = cfg["_warning"]
    if not result["config"]["conventions"]:
        result["config"]["conventions_warning"] = (
            "{} does not exist. Without it no conventions are declared: ask "
            "before writing in any note.".format(cfg["conventions"]))
    statuses = set()

    for zone, target in ((cfg["projects"], "projects"), (cfg["archive"], "archived")):
        base = os.path.join(vault, zone)
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            folder = os.path.join(base, name)
            if name.startswith(".") or not os.path.isdir(folder):
                continue
            if args.project and normalise(name) != normalise(args.project):
                continue
            note = main_note(folder)
            card = {"name": name, "folder": folder, "zone": zone,
                    "main_note": os.path.basename(note) if note else None}
            if note:
                raw, body = split(read(note))
                fm = parse_frontmatter(raw)
                if fm.get("status"):
                    statuses.add(fm["status"])
                card["frontmatter"] = fm
                if args.project:
                    card["headings"] = ["{} {}".format("#" * n, t)
                                        for _, n, t in headings(body)]
            if args.project:
                card["files"] = folder_inventory(folder)
                # The hook names each log after the repository's folder, which
                # need not match the vault folder; the note's `path`, when it
                # has one, names the repository.
                log_name = slug(name)
                repo_path = (card.get("frontmatter") or {}).get("path")
                if isinstance(repo_path, str) and repo_path.strip() \
                        and not os.path.exists(log_path(vault, log_name)):
                    log_name = slug(os.path.basename(repo_path.strip().rstrip("\\/")))
                card["session_log_file"] = log_name + ".json"
                log = read_log(vault, log_name)
                card["session_log"] = log
                if note:
                    card["sessions_since_note_changed"] = sessions_since(log, note)
            result[target].append(card)

    result["statuses_in_use"] = sorted(statuses)
    if args.project and not result["projects"] and not result["archived"]:
        result["warning"] = ("No folder by that name in {} or in {}. "
                             "Ask before creating anything.".format(cfg["projects"],
                                                                    cfg["archive"]))
    output(result)
    return 0


# ----------------------------------------------------------------- section

def cmd_section(args):
    text = read(args.note)
    raw, body = split(text)
    place = locate(body, args.heading)

    if not place:
        print("There is no section '{}'. These exist:".format(args.heading),
              file=sys.stderr)
        for _, n, t in headings(body):
            print("  {} {}".format("#" * n, t), file=sys.stderr)
        if not args.after:
            print("\nTo create a new section, pass --after <another section>.",
                  file=sys.stderr)
            return 1
        place = locate(body, args.after)
        if not place:
            print("'{}' does not exist either.".format(args.after), file=sys.stderr)
            return 1
        _, end, level, _ = place
        lines = body.split("\n")
        block = ["{} {}".format("#" * level, args.heading), ""] \
            + read(args.content).strip().split("\n") + [""]
        lines[end:end] = block
        new_body = "\n".join(lines)
    else:
        start, end, level, title = place
        lines = body.split("\n")
        is_last = end >= len(lines)
        if is_last and args.mode == "replace" and not args.allow_tail:
            tail = [l for l in lines[start + 1:] if l.strip()]
            print("'{}' is the last section of the note, so replacing it takes "
                  "away EVERYTHING down to the end of the file, including the "
                  "loose links in the footer:".format(title), file=sys.stderr)
            for l in tail[-6:]:
                print("  | " + l, file=sys.stderr)
            print("\nOptions: use --mode append to add without deleting, or run "
                  "again with --allow-tail if you really mean to rewrite it all "
                  "(include the footer in the new content yourself).", file=sys.stderr)
            return 2
        content = read(args.content).rstrip("\n")
        if args.mode == "append":
            previous = lines[start + 1:end]
            # The note's footer (one-line paragraphs with [[links]] at the end)
            # is set aside so the new text goes above it, not below.
            footer, j = [], len(previous)
            while j > 0:
                k = j
                while k > 0 and not previous[k - 1].strip():
                    k -= 1
                if k > 0 and "[[" in previous[k - 1] and \
                        (k == 1 or not previous[k - 2].strip()):
                    footer.insert(0, previous[k - 1])
                    j = k - 1
                else:
                    break
            before = previous[:j]
            # A section wrapped in a fenced callout (```ad-note ... ```) takes
            # the new text inside the fence, not after it, where it would
            # render as loose prose under the box.
            fence = None
            stripped = [l for l in before if l.strip()]
            if stripped and re.match(r"^\s*(```|~~~)\s*ad-", stripped[0]) \
                    and re.match(r"^\s*(```|~~~)\s*$", stripped[-1]):
                last = max(i for i, l in enumerate(before) if l.strip())
                fence = before[last]
                before = before[:last]
            # A native callout (> [!note]) is a blockquote: new lines join it
            # only if they are quoted too.
            if fence is None and stripped and re.match(r"^\s*>\s*\[!", stripped[0]) \
                    and all(l.lstrip().startswith(">") for l in stripped):
                content = "\n".join("> " + l if l.strip() else ">" for l in content.split("\n"))
                prior = "\n".join(before).strip("\n")
                content = (prior + "\n>\n" + content).strip("\n")
            else:
                prior = "\n".join(before).strip("\n")
                content = (prior + "\n\n" + content).strip("\n")
            if fence is not None:
                content += "\n" + fence
            if footer:
                content += "\n\n" + "\n\n".join(footer)
        block = ["{} {}".format("#" * level, title), ""] + content.split("\n") + [""]
        lines[start:end] = block
        new_body = "\n".join(lines)

    if args.touch_updated and raw is not None:
        updated = set_key(raw, "updated", today())
        if updated:
            raw = updated

    show_diff(args.note, text, assemble(raw, new_body), args.dry_run)
    return 0


# ------------------------------------------------------------- frontmatter

def cmd_frontmatter(args):
    text = read(args.note)
    raw, body = split(text)
    if raw is None:
        print("That note has no frontmatter. I do not add one on my own.", file=sys.stderr)
        return 1
    for pair in args.set:
        if "=" not in pair:
            print("Format: key=value", file=sys.stderr)
            return 1
        key, _, value = pair.partition("=")
        result = set_key(raw, key.strip(), value.strip())
        if result is None:
            print("'{}' is a block list. This script does not touch it."
                  .format(key), file=sys.stderr)
            return 1
        raw = result
    show_diff(args.note, text, assemble(raw, body), args.dry_run)
    return 0


# --------------------------------------------------------------------- log

def log_path(vault, name):
    return os.path.join(vault, config_of(vault)["logs"], name + ".json")


def english_keys(value):
    """Rename the Spanish keys of an older log, recursively. Folder paths used
    as keys under `folders` are left alone: only known names are renamed."""
    if isinstance(value, list):
        return [english_keys(v) for v in value]
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            new = LOG_ALIASES.get(k, k)
            if new in out and k != new:
                continue  # the English key, already present, wins
            out[new] = english_keys(v) if new != "folders" else \
                {path: english_keys(entry) for path, entry in (v or {}).items()}
        return out
    return value


def read_log(vault, name):
    path = log_path(vault, name)
    if not os.path.exists(path):
        return {"sessions": []}
    try:
        return english_keys(json.loads(read(path)))
    except Exception:
        return {"sessions": []}


# Claude Code creates worktree folders under <repo>/.claude/worktrees/<name>.
# Used only for old logs whose folder no longer exists and cannot be asked of
# git.
WORKTREE_PATTERN = re.compile(r"^(.*?)[\\/]\.claude[\\/]worktrees[\\/][^\\/]+[\\/]?$")


def main_repo(repo):
    """The main repository's folder, even when `repo` is a worktree.

    Every worktree is a different folder, and each used to start its own log
    named after the folder (`gracious-lovelace-6c3ca0.json`): one project's
    work ended up spread over several files that did not say which project
    they belonged to. Now they all write to the repository's. git is asked
    for the common directory, which in a worktree is the main repository's
    `.git`. In a submodule that directory is not called `.git`, and the
    folder itself is kept, as before.
    """
    common = git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if not common:
        # git before 2.31 does not know --path-format and can return a path
        # relative to the folder.
        common = git(repo, "rev-parse", "--git-common-dir")
        if common and not os.path.isabs(common):
            common = os.path.join(repo, common)
    if common:
        common = os.path.normpath(common)
        if os.path.basename(common) == ".git":
            return os.path.dirname(common)
    m = WORKTREE_PATTERN.match(repo)
    return m.group(1) if m else repo


def known_commit(repo, sha):
    return bool(sha) and bool(git(repo, "rev-parse", "--verify", "--quiet", sha + "^{commit}"))


def cmd_log(args):
    """Hook mode. Never touches notes and never fails loudly."""
    try:
        vault = vault_of(args)
    except NoVault as e:
        if not args.quiet:
            print("vault.py: {}".format(e), file=sys.stderr)
        return 0
    # The stdin JSON is read only when --stdin asks for it. It used to be read
    # whenever stdin was not a terminal, and that hung the script for good as
    # soon as it was launched from something that leaves stdin open and empty:
    # a script, a scheduled task, another process. As a hook it makes no
    # difference which wins (Claude Code runs the hook inside the project
    # folder, so os.getcwd() gives the same repo), but a hung hook delays the
    # end of every session.
    repo = args.repo or os.getcwd()
    if args.stdin and not args.repo:
        try:
            data = json.loads(sys.stdin.read() or "{}")
            if isinstance(data, dict) and data.get("cwd"):
                repo = data["cwd"]
        except Exception:
            pass
    repo = os.path.abspath(repo)

    # Only a git repository is logged, and git is asked to confirm it: the log
    # exists to check commits against, so without commits there is nothing to
    # record. rev-parse rather than looking for .git because in a worktree or
    # a submodule .git is a file, not a folder.
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    if not branch:
        return 0
    # A session started in a subfolder belongs to the working tree that holds
    # it; without this, `src/ui` would be logged as a worktree called `ui`.
    top = git(repo, "rev-parse", "--show-toplevel")
    if top:
        repo = os.path.abspath(top)

    # One log per repository: worktrees write to the main repository's.
    main = main_repo(repo)
    name = slug(os.path.basename(main.rstrip("\\/")))
    log = read_log(vault, name)
    folders = log.setdefault("folders", {})

    # New commits are counted from the last one recorded in this same folder.
    # A worktree's first session starts from the last one recorded for the
    # repository, so main's last ten commits are not repeated for every new
    # worktree. If that commit does not exist here (rewritten history), the
    # last ten, as on the first run.
    since = ((folders.get(repo) or {}).get("last_commit")
             or log.get("last_commit"))
    if since and not known_commit(repo, since):
        since = None

    span = "{}..HEAD".format(since) if since else "-10"
    commits = git(repo, "log", span, "--pretty=format:%h %s") or ""
    files = git(repo, "diff", "--name-only", span) if since else ""
    dirty = git(repo, "status", "--porcelain")
    head = git(repo, "rev-parse", "HEAD")

    session = {
        "date": today(),
        "time": dt.datetime.now().strftime("%H:%M"),
        "branch": branch,
        "commits": [c for c in commits.split("\n") if c.strip()],
        "files": [a for a in files.split("\n") if a.strip()][:40],
        "uncommitted": len([l for l in dirty.split("\n") if l.strip()]),
    }
    if repo != main:
        session["worktree"] = os.path.basename(repo.rstrip("\\/"))
        session["folder"] = repo
    log.setdefault("sessions", []).append(session)
    log["sessions"] = log["sessions"][-MAX_SESSIONS:]
    log["project"] = os.path.basename(main.rstrip("\\/"))
    log["path"] = main
    log["last_commit"] = head or since or log.get("last_commit")
    log["last_session"] = today()
    folders[repo] = {"branch": branch, "last_commit": head or since,
                     "last_session": today()}

    write(log_path(vault, name), json.dumps(log, ensure_ascii=False, indent=2))
    if not args.quiet:
        print("Session logged: {}".format(log_path(vault, name)))
    return 0


def cmd_log_merge(args):
    """Fold the logs left by worktrees into their repository's log.

    A one-off for logs written before the hook grouped by repository. Without
    --apply it only says what it would do. With --apply it deletes nothing: it
    moves the folded logs to `_merged/` inside the logs folder, for the user
    to review and delete if they want.
    """
    vault = vault_of(args)
    folder = os.path.join(vault, config_of(vault)["logs"])
    if not os.path.isdir(folder):
        output({"warning": "The logs folder does not exist", "folder": folder})
        return 0
    plan = []
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".json"):
            continue
        path = os.path.join(folder, name)
        try:
            old = english_keys(json.loads(read(path)))
        except Exception:
            continue
        repo_path = old.get("path") or ""
        main = main_repo(repo_path) if os.path.isdir(repo_path) else None
        if not main:
            m = WORKTREE_PATTERN.match(repo_path)
            main = m.group(1) if m else repo_path
        if not main or os.path.normcase(main) == os.path.normcase(repo_path):
            continue
        target = slug(re.split(r"[\\/]", main.rstrip("\\/"))[-1])
        if target + ".json" == name:
            continue
        plan.append({"from": name, "to": target + ".json",
                     "sessions": len(old.get("sessions", []))})
        if not args.apply:
            continue
        log = read_log(vault, target)
        worktree = re.split(r"[\\/]", repo_path.rstrip("\\/"))[-1]
        for s in old.get("sessions", []):
            s = dict(s)
            s.setdefault("worktree", worktree)
            s.setdefault("folder", repo_path)
            log.setdefault("sessions", []).append(s)
        # Old logs have a date but no time: the stable sort keeps each file's
        # sessions together within the same day.
        log["sessions"].sort(key=lambda s: (s.get("date", ""), s.get("time", "")))
        log["sessions"] = log["sessions"][-MAX_SESSIONS:]
        log.setdefault("project", re.split(r"[\\/]", main.rstrip("\\/"))[-1])
        log.setdefault("path", main)
        log.setdefault("folders", {})[repo_path] = {
            "branch": (old.get("sessions") or [{}])[-1].get("branch"),
            "last_commit": old.get("last_commit"),
            "last_session": old.get("last_session")}
        if (old.get("last_session") or "") >= (log.get("last_session") or ""):
            log["last_session"] = old.get("last_session")
        write(log_path(vault, target), json.dumps(log, ensure_ascii=False, indent=2))
        aside = os.path.join(folder, "_merged")
        os.makedirs(aside, exist_ok=True)
        os.replace(path, os.path.join(aside, name))
    output({"applied": bool(args.apply), "folder": folder, "plan": plan})
    return 0


# ------------------------------------------------------------------ canvas

def new_id(used):
    import random
    while True:
        n = "%016x" % random.getrandbits(64)
        if n not in used:
            return n


def containing_group(node, groups):
    """The group whose rectangle holds the node's centre, or None."""
    cx = node.get("x", 0) + node.get("width", 0) / 2.0
    cy = node.get("y", 0) + node.get("height", 0) / 2.0
    for g in groups:
        gx, gy = g.get("x", 0), g.get("y", 0)
        if gx <= cx <= gx + g.get("width", 0) and gy <= cy <= gy + g.get("height", 0):
            return g
    return None


def canvas_cards(nodes, root):
    """For every file node: its note's `state`, the group holding it, its colour.

    A canvas can store a note's state twice, in the node's position and colour.
    When the `state` changes and the node does not, the canvas does not break:
    it still points at a file that exists, and still shows the old colour. It
    lies quietly, which is worse than breaking.

    This does not interpret colours (that 4 is green is each vault's business).
    It only puts the three facts side by side, which is what it takes to see
    that they disagree.
    """
    groups = [n for n in nodes if n.get("type") == "group"]

    def names(label, word):
        return bool(word) and bool(label) and \
            re.search(r"\b" + re.escape(str(word)) + r"\b", label) is not None

    # First pass: each node's facts, without judging them.
    cards = []
    for n in nodes:
        if n.get("type") != "file":
            continue
        path = os.path.join(root, n["file"].replace("/", os.sep))
        state = None
        if os.path.exists(path):
            try:
                state = parse_frontmatter(split(read(path))[0]).get("state")
            except Exception:
                pass
        if not isinstance(state, str):
            state = None
        g = containing_group(n, groups)
        cards.append({"file": n["file"], "state": state,
                      "group": g.get("label") if g else None,
                      "color": n.get("color")})

    # Second pass: compare. A group "groups by state" if its label names one
    # of the states seen in this canvas. Decided on the whole set, not on the
    # fly, so the result does not depend on the order of the nodes.
    states = {c["state"] for c in cards if c["state"]}
    by_state = {g.get("label") for g in groups
                if any(names(g.get("label"), s) for s in states)}

    mismatches = [c for c in cards
                  if c["state"] and c["group"] in by_state
                  and not names(c["group"], c["state"])]
    return cards, mismatches


def cmd_canvas(args):
    data = json.loads(read(args.file)) if os.path.exists(args.file) \
        else {"nodes": [], "edges": []}
    nodes = data.setdefault("nodes", [])
    data.setdefault("edges", [])
    used = {n.get("id") for n in nodes} | {e.get("id") for e in data["edges"]}

    if args.report:
        root = args.vault_root or vault_of(args)
        broken = [n["file"] for n in nodes if n.get("type") == "file"
                  and not os.path.exists(os.path.join(root, n["file"].replace("/", os.sep)))]
        cards, mismatches = canvas_cards(nodes, root)
        output({
            "nodes": len(nodes),
            "edges": len(data["edges"]),
            "groups": [n.get("label") for n in nodes if n.get("type") == "group"],
            "linked_files": [n["file"] for n in nodes if n.get("type") == "file"],
            "broken_links": broken,
            "file_nodes": cards,
            "state_outside_its_group": mismatches,
            "free_y": max([n.get("y", 0) + n.get("height", 0) for n in nodes] or [0]) + 80,
        })
        return 0

    if not args.add_file and not args.add_text:
        print("Nothing to do: use --report, --add-file or --add-text.", file=sys.stderr)
        return 1

    if args.add_file and any(n.get("file") == args.add_file for n in nodes):
        print("That file is already on the canvas. Not adding it twice.", file=sys.stderr)
        return 1

    # A gap below everything that exists: what is there never moves.
    y = max([n.get("y", 0) + n.get("height", 0) for n in nodes] or [0]) + 80
    x = min([n.get("x", 0) for n in nodes] or [0])

    added = []
    if args.add_file:
        added.append({"id": new_id(used), "type": "file", "file": args.add_file,
                      "x": x, "y": y, "width": 400, "height": 400})
    if args.add_text:
        added.append({"id": new_id(used), "type": "text", "text": args.add_text,
                      "x": x + (440 if args.add_file else 0), "y": y,
                      "width": 400, "height": 120})
    if args.color:
        for n in added:
            n["color"] = args.color

    nodes.extend(added)
    if args.dry_run:
        print("[DRY RUN] Would add {} node(s) at x={} y={}, moving nothing that exists."
              .format(len(added), x, y))
        return 0
    write(args.file, json.dumps(data, ensure_ascii=False, indent=2))
    print("Added {} node(s). Existing positions untouched.".format(len(added)))
    return 0


# -------------------------------------------------------------------- main

def main():
    # --vault works before or after the subcommand.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--vault", default=argparse.SUPPRESS,
                        help="Vault folder (else the OBSIDIAN_VAULT environment variable)")

    p = argparse.ArgumentParser(description="Keep Obsidian project notes in step with Claude Code.",
                                parents=[common])
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scan", parents=[common], help="Inventory of the vault or of one project")
    s.add_argument("--project", help="Name of the project's folder")
    s.set_defaults(func=cmd_scan)

    c = sub.add_parser("section", parents=[common], help="Replace the body of one section")
    c.add_argument("--note", required=True)
    c.add_argument("--heading", required=True, help="Heading, with or without emoji")
    c.add_argument("--content", required=True, help="File holding the new markdown")
    c.add_argument("--mode", choices=["replace", "append"], default="replace")
    c.add_argument("--after", help="If the section does not exist, create it after this one")
    c.add_argument("--touch-updated", action="store_true")
    c.add_argument("--allow-tail", action="store_true",
                   help="Allow rewriting the last section with its whole footer")
    c.add_argument("--dry-run", action="store_true")
    c.set_defaults(func=cmd_section)

    f = sub.add_parser("frontmatter", parents=[common], help="Change single frontmatter keys")
    f.add_argument("--note", required=True)
    f.add_argument("--set", nargs="+", required=True, metavar="key=value")
    f.add_argument("--dry-run", action="store_true")
    f.set_defaults(func=cmd_frontmatter)

    l = sub.add_parser("log", parents=[common], help="Log the session (hook mode)")
    l.add_argument("--repo")
    l.add_argument("--quiet", action="store_true")
    l.add_argument("--stdin", action="store_true",
                   help="Read the hook's JSON on stdin to take the folder from it. "
                        "Hook only: whoever launches it must close the stream, "
                        "or the read waits forever.")
    l.set_defaults(func=cmd_log)

    j = sub.add_parser("log-merge", parents=[common],
                       help="Fold worktree logs into their repository's log")
    j.add_argument("--apply", action="store_true",
                   help="Write. Without it, only show the plan")
    j.set_defaults(func=cmd_log_merge)

    k = sub.add_parser("canvas", parents=[common], help="Inspect or extend a .canvas")
    k.add_argument("--file", required=True)
    k.add_argument("--report", action="store_true")
    k.add_argument("--add-file", help="Path of the note from the vault root")
    k.add_argument("--add-text")
    k.add_argument("--color", help="1-6 or hex")
    k.add_argument("--vault-root", help="Vault root for --report (defaults to the vault)")
    k.add_argument("--dry-run", action="store_true")
    k.set_defaults(func=cmd_canvas)

    args = p.parse_args()
    try:
        sys.exit(args.func(args))
    except Exception as e:
        print("vault.py: {}".format(e), file=sys.stderr)
        sys.exit(0 if args.cmd == "log" else 1)


if __name__ == "__main__":
    main()
