---
name: obsidian-project-sync
description: "Keeps the project notes of an Obsidian vault up to date with work done in Claude Code, respecting the vault's own structure and the hand-written prose of each note. Use whenever Obsidian, the vault, a project note or a canvas comes up: \"update the note\", \"document this\", \"sync the vault\", \"write this down\", \"where was I?\", or when a stretch of work ends and what changed should be recorded. Also to review which projects exist and in what state, add notes to a project's folder, update a canvas, and install or fix the hook that logs sessions. In Spanish: \"actualiza la nota\", \"documenta esto\", \"sincroniza\", \"apunta esto\", \"¿por dónde iba?\"."
allowed-tools: Bash, Read, Edit, Write, Glob, Grep
---

# Obsidian project sync

**The vault describes itself.** Where the projects are, where finished ones
go, where the hook leaves its logs and which note declares the vault's
conventions: all of that comes from `.claude-vault.json` at the vault's root,
and `scan` returns it. This skill assumes no folder names.

**A vault is not only projects**, and its conventions note says what each
folder holds. Keep that in mind when offering where to put something new: a
decision or a fact that affects several projects does not go in one
project's note.

## Local map first

Look for this skill's local map before anything else: a section named
`obsidian-project-sync local map` in the user's standing instructions (their
`CLAUDE.md` files in Claude Code, read from disk rather than from the copy in
context, which can predate an edit; Project instructions or the user's
preferences in claude.ai). A section named `Local map for this install`
inside this SKILL.md, added when the skill was packaged for one claude.ai
account, counts too; standing instructions that say otherwise win. It holds
what only that setup knows: the vault's path, the user's own
conventions on top of the vault's (companion notes every project carries,
callout styles), other files that point at the vault and must change with it.
Follow it where it speaks; it overrides the defaults here.

## The script and the vault

The script is `scripts/vault.py`, next to this SKILL.md: build its path from
the skill's own folder (Claude Code states the base directory when the skill
loads). Every example below writes it as `vault.py`. It needs Python 3.8 or
later; if `python` is not found, try `python3`, then `py`.

The vault's path comes, in this order, from the local map, from the
`OBSIDIAN_VAULT` environment variable, or from asking the user. Pass it with
`--vault`, before or after the subcommand. The script has no built-in default
on purpose: without a vault it stops and says so.

## Always first: look before writing

```bash
python vault.py scan --vault "<vault>"
```

With no `--project` it returns the vault's inventory: which projects exist, in
which zone and with what `status`. `statuses_in_use` lists the values the
user already uses; **pick one of those and do not invent labels**.

Then the project itself:

```bash
python vault.py scan --vault "<vault>" --project "<folder name>"
```

It returns the folder, the main note, its frontmatter, **the exact list of its
headings**, the other files in the folder, the session log (and which log
file it read, in `session_log_file`), and
`sessions_since_note_changed`: the logged sessions newer than the note's last
change on disk. That last list is where "what is not in the note yet" starts,
not proof of it: check it against the note before claiming anything is
missing.

`--project` takes the name of the project's folder in the vault, matched
without case or accents. When working from a code repository, the folder
usually has the repository's name; if not, run `scan` without `--project` and
match by the main note's frontmatter (a `path` or `url` key, if the vault
uses one), and ask when nothing matches.

A project in the archive zone is finished. Do not recreate it among the live
ones or update it without asking.

### Second: read the vault's conventions

`scan` returns a `config` block:

```json
"config": {
  "source": ".claude-vault.json",
  "projects": "Projects",
  "archive": "Archive",
  "logs": "Toolbox/Claude Sync",
  "conventions": "/path/to/vault/Meta/Conventions.md"
}
```

**`conventions` is the note that rules.** Read it before writing in any other:
it declares the frontmatter schema, how notes are written in that vault, what
may change without asking and what may not. This skill deliberately carries
no copy of that: a copy ages, and an earlier version of this skill ended up
pointing at a folder that no longer existed.

If `conventions` is `null`, the vault declares none. **Ask before writing in
any note.**

The same block says where the folders came from. If `source` is `defaults`,
the vault has not described itself and you are working on assumptions: say
so, and offer to write `.claude-vault.json` (format in
`references/mechanics.md`). If a `warning` appears, the config is broken and
needs fixing before going on.

Each project folder is different: some hold only the note and a canvas, others
carry loose notes. Trust `scan`, never what was there last time.

## Writing in a note

Notes are written by hand. There is no template and no hidden markers, and
none are added. The body of one specific section is replaced:

```bash
python vault.py section --vault "<vault>" --note "<path>" --heading "Deploy" --content "<file>" --dry-run
```

The heading is matched without emoji and by partial match, so `Deploy` finds
`## 🚀 Deploy`. If there is no match, the script lists the headings that exist
instead of making one up.

`--content` is a file holding the new markdown. Write it to a temporary
folder (the session's scratchpad, or the system temp folder), never inside
the vault or a code repository, and delete it afterwards.

Rules that really matter:

- **`--dry-run` first, always, and the user's yes before the real write.**
  Show the user the dry-run diff, say whether each change is factual or
  prose, and wait. Run the same command without `--dry-run` only after they
  agree; one yes covers the diffs they saw, nothing else.
- **`--content` carries the whole section, not just what changes.** `replace`
  swaps the whole body under that heading. Send only a table and the prose
  under it disappears. Read the current section, work the change into it,
  and send the complete result.
- **The last section of the note is protected.** The footer links usually live
  below it, belong to no section and would be lost. The script stops with
  exit code 2 and says so. Use `--mode append` to add without deleting, which
  is nearly always right for a running log such as *Recent changes*.
- **`append` respects callouts.** When a section is a fenced callout
  (```` ```ad-note ````, from the Admonition plugin), the new text goes inside
  the fence, before its closing line; when it is a native callout
  (`> [!note]`), the new lines are quoted so they stay inside it. The footer
  stays last either way.
- **Imitate what is there.** Language, voice, prose or bullets, length: the
  vault's conventions note declares it, and the note you are about to touch
  confirms it. Read it before drafting.
- **Check before you claim.** A count, a version or a status written into a
  note must come from something you read or ran in this session. If it
  cannot be checked now, leave it out or say it is unverified.

Adding a new section requires saying where it goes:
`--heading "Testing" --after "Gotchas"`. Ask first: a new section changes the
structure of a document the user wrote.

## What you may change without asking

**The vault declares it**, in its conventions note: the part that says what
is factual and checkable (and so corrected without asking) and what is
prose, which is not touched without permission.

Until you have read it, treat everything as prose and ask.

When new information fits no existing section, **offer both ways out and let
the user choose**: extend a section, or a separate note linked from the main
one. Do not decide yourself.

## Frontmatter

The schema belongs to each vault and its conventions note declares it. `scan`
returns each note's real frontmatter, which is the other way to see it.

```bash
python vault.py frontmatter --vault "<vault>" --note "<path>" --set updated=2026-09-13 --dry-run
```

Scalar keys only. The script refuses block lists on purpose: changing a
note's topics is the author's decision. `section --touch-updated` already
sets the date, so this is rarely needed on its own.

A field owned by a plugin (a sticker, an icon) is never touched.

## Canvas

`.canvas` files are JSON with `nodes` and `edges` (JSON Canvas 1.0). The
layout was made by hand, with deliberate groups and connections.

```bash
python vault.py canvas --vault "<vault>" --file "<path>.canvas" --report
```

It gives nodes, edges, group names, which notes are linked and whether any
points at a file that no longer exists.

**And `state_outside_its_group`, the field that really needs watching.** A
canvas that groups notes by their `state` stores that fact twice: in the
frontmatter and in the node's position and colour. Change the `state`, leave
the card where it was, and the canvas does not break; it still points at a
file that exists and still shows the old colour. It starts lying with nothing
to warn anyone.

**So whenever you change a `state`, check whether that project or folder has a
canvas that groups by state, and run the report.** The reverse holds too:
after creating a note, check it has a card. A note that is not on the board
does not exist for whoever reads the board.

Fixing it means moving the node and recolouring it, which is manual editing:
the script reports, it does not rearrange. Say so and propose the change.

```bash
python vault.py canvas --file "<path>.canvas" --add-file "Relative/Path/Note.md" --color 6 --dry-run
```

New nodes land in a gap below everything that exists: **nothing already
there moves**. Placing them inside a group is the user's manual work, and
rightly so. Run it again without `--dry-run` once the user agrees.

If the report shows broken links, say so and stop. Do not delete nodes.

## The session log

A `SessionEnd` hook records the raw data of each Claude Code session in the
logs folder the vault declares (`config.logs`), one JSON per repository:
date, branch, new commits since last time, files touched and whether anything
was left uncommitted. **It writes in no note.**

That is the raw material. When the user asks for an update, `scan --project`
brings it already read, in `session_log` and `sessions_since_note_changed`.
Check those commits against what the note says and propose which sections
have gone stale.

If the hook is not installed yet, read `references/hook-install.md`.

## Notes from a claude.ai conversation

claude.ai projects are not on disk, so there is no script there. Write the
complete markdown in a code block, with frontmatter that follows the schema
of the user's vault (ask for it, or for one existing note to copy, if you do
not know it), and say where to save it. If the project already has a note,
say which section to paste it into rather than creating a loose file.

## When something fails

- **`python` is not recognised**: try `python3`, then `py`. If none works,
  there is no Python; say so and offer to make the edit by hand with the file
  tools, which is slower and riskier.
- **"No vault given"**: the local map has no vault path and `OBSIDIAN_VAULT`
  is not set. Ask the user for the path, and offer to add it to the local map.
- **The script stops with exit code 2**: that is the last-section protection
  doing its job. Switch to `--mode append`.
- **The diff shows more deleted than expected**: do not write. Almost always
  `--content` was incomplete.
- **The project's folder does not exist**: ask. Do not create new folders in
  the projects zone on your own.

## References

- `references/hook-install.md`: installing the session-logging hook, on
  Windows, macOS and Linux.
- `references/mechanics.md`: how the script works and what it guarantees:
  the config file, how a heading is found, the protections, the log format.

The **writing conventions are not here**. They live in the vault, in the note
`scan` returns in `config.conventions`.
