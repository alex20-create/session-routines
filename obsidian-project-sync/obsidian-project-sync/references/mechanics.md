# How the script works

What `vault.py` does inside and what it guarantees. **There are no writing
conventions here**: each vault declares those in its own note, and `scan`
gives its path in `config.conventions`. If this file and that note ever
disagree, the note wins; this file only describes the tool.

The split is deliberate. An earlier version of this skill carried a copy of
the vault's conventions inside it; the copy aged and ended up pointing at a
folder that no longer existed.

## Finding the vault

`--vault PATH`, before or after the subcommand, else the `OBSIDIAN_VAULT`
environment variable (`OBSIDIAN_VAULT_CLAUDE`, the name older installs used,
is still read). There is no built-in default. `scan` and the other commands
stop with exit code 1 and a message; `log`, which runs as a hook, exits 0 in
silence instead, because a hook that fails can get in the way of closing the
session.

## The vault's config

`.claude-vault.json`, at the vault's **root**. The location is fixed on
purpose: it is the bootstrap, and any other place would require already
knowing how the vault is organised in order to find it.

```json
{
  "projects": "1 Projects",
  "archive": "4 Archive",
  "logs": "3 Resources/Claude Sync",
  "conventions": "Meta/Conventions.md"
}
```

| Key | What it is |
| --- | --- |
| `projects` | Folder whose subfolders are live projects |
| `archive` | Folder whose subfolders are finished projects |
| `logs` | Where the hook leaves the session JSON files |
| `conventions` | The vault note that declares how notes are written in it |

Forward slashes even on Windows; the script translates them. All four are
paths relative to the vault's root, and any of them may be left out.

Earlier versions used Spanish key names (`proyectos`, `archivo`, `registros`,
`convenciones`). They are still read as aliases; when a file has both, the
English key wins.

Without the file, the fallbacks are `Projects`, `Archive`, `Claude Sync` and
`Conventions.md`, and `scan` says so in `config.source` (`defaults`). If the
file exists but is broken, `scan` warns in `config.warning` and carries on
with the fallbacks: a broken config cannot bring down the hook, but it cannot
go unnoticed either. Keys it does not know are reported in the same warning.

If the conventions note does not exist, `scan` returns `conventions: null`
and a `conventions_warning`. **With no conventions declared, ask before
writing in any note.**

## Which project is which

A project is a **subfolder** of `projects` or of `archive`. Folders whose
name starts with a dot (plugin state such as `.space`) are skipped. The main
note is the one named like the folder; if there is none and the folder holds
exactly one `.md`, that one; if there are several and none matches, the
script returns `null` instead of choosing.

This is the tool's strongest assumption. A vault that identifies its projects
by tag, by link or by an ID does not fit here, and it is better to say so than
to make it fit halfway.

`scan --project` reads the session log named after the project's folder; if
there is none and the main note's frontmatter has a `path` (the repository's
folder), it reads the log named after that folder instead, and says which in
`session_log_file`.

## Frontmatter keys the script knows by name

The schema is the vault's, but four keys are read or written by name:
`status` (collected into `statuses_in_use`), `updated` (set by
`section --touch-updated`), `state` (compared with canvas groups) and `path`
(to find the session log). A vault that uses other names for these simply
gets empty results for the matching feature: say so rather than renaming the
vault's keys.

## Finding a heading

`section --heading` matches **without emoji and by partial match**, so
`Deploy` finds `## 🚀 Deploy`. If nothing matches, the script lists the
headings that do exist instead of inventing one. Headings inside code fences
are ignored.

A section runs to the next heading of the same level or higher.

## The protections

1. **`--dry-run` prints the diff and writes nothing.** Use it first, always.
   If the diff deletes more than expected, `--content` was almost always
   incomplete: `replace` swaps the *whole* body of the section.
2. **The last section is not rewritten whole.** The loose footer links
   usually live below it, belong to no section and would be lost. The script
   stops with exit code 2. `--mode append` is nearly always right, and
   `--allow-tail` exists for the rare case that really needs it.
3. **`frontmatter` touches scalar keys only.** Block lists are refused on
   purpose: changing a note's topics is the decision of whoever wrote it, not
   of the script.
4. **Writes are atomic.** The new content goes to a `.tmp` file that then
   replaces the note, so an interrupted write never leaves half a note.

### How `append` places the new text

The footer (one-line paragraphs holding `[[links]]` at the end of the
section) is set aside, the new text goes after the existing body, and the
footer goes back last. When the section's body is a fenced callout
(```` ```ad-note ```` and its closing fence, as the Admonition plugin writes
them), the new text goes inside the fence, before its closing line, so it
renders inside the box. When the body is a native callout (every non-empty
line quoted, the first one `> [!type]`), the new lines are quoted too.

## Canvas

JSON with `nodes` and `edges`, JSON Canvas 1.0 spec. `--add-file` places the
new node in a gap below everything that exists: **nothing already there
moves**. Placing it inside a group is manual work, and rightly so.
`--dry-run` says where it would go and writes nothing.

If the report shows broken links, say so and stop. The script never deletes
nodes.

### What `--report` returns

| Field | What it is |
| --- | --- |
| `nodes`, `edges`, `groups` | Counts, and the groups' labels |
| `linked_files` | Paths of every file node |
| `broken_links` | Nodes pointing at files that no longer exist |
| `file_nodes` | For each node: its path, the note's `state`, the label of the group holding it, and its colour |
| `state_outside_its_group` | Nodes whose `state` does not match the group they sit in |
| `free_y` | The first free `y` below everything |

### The two different ways a canvas fails

`broken_links` detects that the canvas **has broken**: it points at something
that is gone. That is loud and easy to see.

`state_outside_its_group` detects that the canvas **has started lying**. A
canvas that groups notes by their `state` stores that fact twice: once in the
frontmatter and again in the node's position and colour. Change the `state`
without moving the node and nothing breaks: it still points at a file that
exists, and still shows the old colour. Lying quietly is worse than breaking,
because nothing warns.

It happened for real: a note moved to `parked` and its card stayed green,
inside the *installed* group, until someone noticed by eye.

**The script does not interpret colours.** That 4 is green is each vault's
business. It only puts the three facts side by side (`state`, group, colour),
which is what it takes to see they disagree.

The warning only fires on canvases that **group by state**, decided like
this: the `state` of every note on the canvas is collected, and a group
counts as a state group if its label names one of them. On an architecture
canvas the groups are named after something else and
`state_outside_its_group` comes back empty.

## The hook and the log format

`log` records the session and **never touches notes**. It only acts in git
repositories (it asks git with `rev-parse`, so it works in a worktree or a
submodule, where `.git` is a file rather than a folder), keeps the last 20
sessions per repository, counts commits from the last one recorded, and, if
anything fails, exits 0 in silence.

Worktrees write to their main repository's log, so one project's work lives
in one file. `log-merge` folds logs written before that grouping existed;
without `--apply` it only shows the plan, and with it the folded files are
moved to `_merged/` (`_juntados/` in older versions), never deleted. A
session started in a subfolder of a repository is logged under the
repository's own folder, not as a worktree.

`--stdin` is for the hook only. It reads the JSON Claude Code sends to take
the folder from it, and whoever launches it must close the stream. By hand,
without the flag, the folder is the current directory.

One file per repository, `<logs>/<repository-folder-slug>.json`:

```json
{
  "sessions": [
    {"date": "2026-11-06", "time": "17:30", "branch": "main",
     "commits": ["a1b2c3d fix: ..."], "files": ["src/app.ts"], "uncommitted": 0,
     "worktree": "only for a worktree session", "folder": "only for a worktree session"}
  ],
  "project": "my-app",
  "path": "/path/to/my-app",
  "last_commit": "full sha",
  "last_session": "2026-11-06",
  "folders": {"/path/to/my-app": {"branch": "main", "last_commit": "full sha", "last_session": "2026-11-06"}}
}
```

Logs written by earlier versions use Spanish keys (`sesiones`, `fecha`,
`rama`...). The script reads them, and rewrites them with English keys the
next time it logs a session for that repository. Anything else that reads
these files should accept both until every log has been rewritten.

## Encoding

The script reconfigures `stdout` and `stderr` to UTF-8 at start-up. The
Windows console defaults to cp1252, which cannot encode emoji; without this,
`scan --project` dies serialising the heading list, and so does any diff that
touches a line with an emoji.
