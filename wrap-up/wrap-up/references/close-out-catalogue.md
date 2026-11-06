# Close-out catalogue

Categories of work that a session close-out can persist, in execution order.
Each category says what it is for, how to recognise a skill that does it, the
members known at the time of writing (hints only; discover the real set each
run), and the near-misses that share a word but do something else.

The known members and near-misses are the author's own install (plugins and
gstack), kept as a worked example; the local map or discovery (`SKILL.md`,
section 1) gives the real set. A near-miss shares a word with a category but
does something else: read the whole description before matching, the flagged
ones only show the pattern. In claude.ai or a cloud session the members are
usually absent; that is a "skip, not installed", not an error. How each
category runs there is in `SKILL.md`, section 2; this file only says what
each category is for and in what order it goes.

The order is a dependency chain, not a preference:

```
1 memory  →  2 learnings  →  3 vault sync  →  4 knowledge graph  →  5 context save
   (facts)     (lessons)      (reads 1+2)      (reads the vault)     (describes final state)
```

Optional categories (6, 7) go after 2 and before 3 when they apply.

## Settled decisions

Decisions the user has taken about this routine. The store the user's
instructions name for settled decisions (a vault note, for one) is the
source; when it says something different, trust it and correct this list.
The entries below are the author's, kept as the shape to follow.

- The knowledge graph of the vault is retired: nobody queried it and every
  changed note cost about 85k tokens to re-extract. Only code repositories
  keep a graph. Skip category 4 for the vault and report only code graphs.
- Without a vault graph, a normal close is the cheap steps only.

## Reference costs

Measured in Claude Code on the author's Windows machine, 2026-09-20. They are orders
of magnitude, not quotes: what a step reads and writes moves them, and the
report at the end of each close is where corrections come from. In claude.ai
the steps are different (reading memory files, staging vault files), so
these figures are only an estimate from another setup; say so or leave the
figure out. On a new install they are another machine's figures everywhere,
until your own closes correct them.

| Category | Typical cost | What moves it |
|---|---|---|
| 1a Auto-memory | ~2k | number of facts; re-reading existing memory files |
| 1b Handoff note (`remember`) | ~3k | flat |
| 2 Learnings | ~2-4k | one shell call per learning |
| 3 Vault sync | ~10k when only the log and a check are due; ~30k when notes need editing | `scan` output, notes read before editing, dry-run diffs, each question asked |
| 4 Knowledge graph | ~85k per changed note, flat regardless of note length; ~0 for code-only or deletions | one subagent per batch of notes; a rebuild from scratch was ~480k for 86 notes |
| 5 Context save | ~3-5k | git state and the summary |
| 6 Memory consolidation | ~10-20k | reads every memory file |
| 7 CLAUDE.md revision | ~5-10k | reads the file and the session |

Skipped steps carry no figure; "skip" and the reason is enough. A close with
nothing to graph runs around 20-45k; each changed note adds ~85k on top.
When the plan has conditional steps, give the total without them and each
one's own add-on: one number would hide an expensive decision.

## 1. Session and user memory

**Purpose:** facts the next session must know without being told again:
who the user is, how they like to work, what was decided, what is in flight.

**Recognise by:** "memory", "remember", "handoff", "session state",
"continuation", "persist across sessions".

**Known members:**
- Auto-memory directory (not a skill): the `memory/` folder named in the
  system prompt. Write one file per fact with the frontmatter the prompt
  specifies, then add its line to `MEMORY.md`. Check for an existing file
  first and update it rather than duplicating. This directory exists only in
  Claude Code; in claude.ai memory is the memory tools plus a background
  pass, and the close only checks it (`SKILL.md`, section 2).
- `remember` (plugin `remember`): writes a first-person handoff note for the
  next session. Its hooks also capture automatically; running the skill
  explicitly makes the note deliberate.

**Run both members** where both exist. They write to different places for
different readers: auto-memory is what Claude loads at the start of every
session, the handoff note is what `remember` replays. One does not replace
the other. Run both means neither replaces the other, not that each always
writes: a member with nothing of its own to hold this session (auto-memory
when a pointer already rides the handoff note) is an honest skip.

**What goes in auto-memory:** only what the user's named stores and the
repos do not already record. A decision the vault sync (step 3 of this same
plan) will write into the decisions store counts as recorded: a one-line
pointer at most, not a second copy. But if the user strikes that later step
from the plan, this step inherits the fact; adjust before executing. Save
the things that live nowhere else: a preference the user stated, a
correction, a tool gotcha.

**Near-misses:** `anthropic-skills:consolidate-memory` is a periodic
clean-up, see 6. `anthropic-skills:import-memory` imports from another
assistant. `remember:doctor` only diagnoses the plugin. `caveman-compress`
rewrites memory files to spend fewer tokens; it saves nothing new.

## 2. Project learnings

**Purpose:** lessons about the project itself: a gotcha, a pattern that
worked, a thing that must not be repeated.

**Recognise by:** "learnings", "what have we learned", "retro", "lessons".

**Known members:**
- `gstack-learn`: manages the project's learnings file.

**Recommend "run" when:** the session taught something about working on
the project: a gotcha, a pattern that held, a thing not to repeat.
**Recommend "skip" when:** it taught nothing of the kind; a product or
design decision is material for categories 1 and 3, not a learning.

**Near-misses:**
- `anthropic-skills:learn` teaches the *user* a concept (ELI5, flashcards).
  Not a close-out step.
- `gstack-retro` is a weekly engineering retrospective, not a per-session
  save. Skip unless the user asks.
- `caveman-learn` (with or without a plugin prefix) acts on token-cost
  reports; it has nothing to do with project learnings.

## 3. Vault sync

**Purpose:** carry what happened in the session into the Obsidian vault's
project notes, respecting that the notes are hand-written.

**Recognise by:** "Obsidian", "vault", "project notes", "sync", "canvas".

**Known members:**
- `obsidian-project-sync`: updates the project note, its automation note,
  and the session log where no hook already writes it. It asks before each
  write; that is its own rule, let it.

**Near-misses:** `obsidian-inbox-promote` moves notes around inside the
vault; it carries nothing from the session.

**Why after 1 and 2:** the vault note should record the decisions and
lessons in their final wording, so write those down first.

**Recommend "run" when:** a project's code or notes changed (by anyone,
including edits made by hand during the session), a decision was taken, or
a tool note went stale. When the notes were already edited in-session, the
sync's remaining work is the session log plus a check that the project
note reflects the decision: budget the low end. **Recommend "skip" when:**
the session touched no project and no tooling note. In Claude Code, when a
`SessionEnd` hook already logs the raw session data (the local map or
`settings.json` says whether one does), skipping loses nothing; without
such a hook, and in claude.ai where none runs, what is not synced now was
never captured.

## 4. Knowledge graph

**Purpose:** keep any `graphify-out/` current with the files it was built
from. Per "Settled decisions", this now means code repositories only; the
vault has no graph to keep current.

**Recognise by:** "graphify", "knowledge graph", "graph.json".

**Known members:**
- `graphify` skill, invoked with `--update` on each directory that
  `scripts/find_graphs.py` reports as stale. Code-only changes need no
  LLM; changed notes or docs dispatch extraction subagents, so mention the
  token cost in the plan when notes changed. When a repository's own
  instructions name a dedicated rebuild command, that command is the member
  for that repository, never the generic update: a graph can carry edges
  the generic update drops.

**Why after 3:** a graph built from notes reads the notes. Updating it
before the sync would graph the old notes.

**Skip when:** `find_graphs.py` reports every graph unchanged. The script
compares the disk against the manifest graphify wrote on its last run, so
it is authoritative even when you remember editing a graphed file this
session: if the graph was updated after that edit, the file is current. A
mismatch between the session's story and the disk (files said to have
changed, a clean tree) does not lower the manifest's authority; it is its
own discrepancy, named in the plan.
Where the script cannot run (no shell on the machine that holds the
graphs), the graph is unchecked, which is a different thing from unchanged.

**Recommend "run only if" when:** files changed but nothing this session
depends on the graph being current. The graph is a query tool; a stale one
answers slightly worse, it does not break anything. Batching several
sessions' edits into one update costs the same per file and saves the
fixed overhead, so deferring is a reasonable default when the budget is
tight. Recommend "run" when the session's own work was graph-related, or
when the user is about to ask the graph something.

## 5. Context save

**Purpose:** a resumable snapshot (branch, open files, where the work
stopped) for the next session to restore.

**Recognise by:** "context", "save", "restore", "resume", "working state".

**Known members:**
- `gstack-context-save` (restored later with `gstack-context-restore`).
- Where the project instructions name one place for "where I left off" (a
  field in a project database, for one), that place is the context save,
  and a skill that owns writing there (a daily close routine) is the step.
  See `SKILL.md`, section 2.

**Against 1b:** when both a handoff note and a context save run, "where
the work stopped" belongs here; the handoff carries what the next session
must know and points at the rest. Neither copies what a named store holds.

**Near-misses:** `gstack-context-restore` is the read side of the pair. A
daily close routine (`plan-admin`, for one) is this step only where the
project instructions name the place it writes as where "where I left off"
lives; closing a session is not closing the day.

**Why last:** it should describe the state after every other step wrote.

## Work in progress (feeds 1 and 5, not a step)

**Purpose:** some skills spread one job over several sessions and keep
their progress in a file on disk. When a close happens halfway, the next
session should learn about it from the handoff, not by stumbling on it.

**How to find it:** in the repositories the session worked in, look for the
progress files listed below, in the working folder and in every worktree
(`git worktree list` shows them). Read only enough to say where things
stand.

**Known members:**
- `code-cleanup`: `.cleanup/report.md`, next to `.cleanup/baseline.md`.
  Its blocks table gives each block a status (applied, skipped, reverted,
  or the same words in the user's language); a block with none is pending.
  If any are pending, the line to carry is the branch, the folder (say so
  when it is a worktree), the pending blocks by number and topic, and the
  report's path.

**What to do with it:** add that line to the handoff note (1b) and the
context save (5). If neither step runs, mention it in the report at the
end. Cost: ~1k, reading one table. If nothing is pending or no such file
exists, say nothing about it. Only the files listed here count: a skill's
own rolling buffers (a `remember` daily note, for one) are its business,
not work in progress.

## 6. Memory consolidation (optional)

**Purpose:** merge duplicate memories, prune stale ones.

**Known members:** `consolidate-memory`.

**When:** only when the memory directory has grown noticeably or the
session corrected something a memory got wrong. Not every close.

## 7. CLAUDE.md revision (optional)

**Purpose:** fold a convention that changed this session into a
`CLAUDE.md`: the project's, or the global `~/.claude/CLAUDE.md` when the
change is a tool or rule that applies everywhere (a new skill, a hook).

**Known members:** `claude-md-management:revise-claude-md`.

**Near-misses:** `claude-md-management:claude-md-improver` is a general
audit of the file, not a session fold-in.

**When:** only when a rule, command, or layout one of those files describes
changed. Otherwise skip; both files are curated by hand.
