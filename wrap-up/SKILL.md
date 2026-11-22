---
name: wrap-up
description: Use when the user is about to archive the chat, close the session or finish for now ("voy a archivar", "cierro el chat", "wrap up", "/wrap-up"), in Claude Code or in claude.ai, even when they name none of the skills that save state, and also when the chat being closed is days old and later sessions have moved on. Not for the end of one task while the user keeps working, not for the daily close routine ("cierro el día", which belongs to the planning skill), and not for logging out of a website ("cerrar sesión" in that sense).
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill
---

# Wrap-up

The user is about to archive this chat. Anything that lives only in the
conversation is about to be lost: what was decided, what changed on disk,
what the next session should pick up. Several installed skills each save one
slice of that. This skill's job is to find them, run the ones this session
needs in the right order, and stop after one confirmation.

A close costs in proportion to the session. A chat that only answered a
question should not pay for the checks that a day of work across three
repositories needs, so the level of the close is settled first (section 1),
and the level decides what is read, checked and run. This file is what every
close reads. The others are read only when they apply:

| File | Read it when |
|---|---|
| `references/close-out-catalogue.md` | the close is full, or there is no local map (section 2). Otherwise only the one section a step needs |
| `references/other-environments.md` | the chat is not Claude Code on the user's machine |
| `references/stale-and-repeat-closes.md` | the session's last real work was on an earlier day than today, or this chat already holds an earlier close |

The set of skills is not fixed: plugins come and go, the user writes new
skills. Never hardcode names; a local map or discovery gives the real set
(section 2). The catalogue says what each category is, in what order and at
what cost; this file says how a close runs. If the two seem to disagree,
follow the catalogue for what and order, this file for how, and name the
disagreement in the report so the user can fix it.

## 1. Where, how old, which level

Settle three things from what is already in the conversation, without
reading anything for it, and say them in the first line of the plan.

**Where.** In Claude Code on the user's machine there is a shell on that
machine, skills in `~/.claude/skills`, hooks that run, repositories on
disk; this file applies as written. Anywhere else (claude.ai, a cloud
session: the chat runs in a container, with or without a shell tool for the
user's computer) read `references/other-environments.md` before going on;
it says how each step runs there. Signals: the platform and working
directory, which tools are listed (device shell, device file tools, memory
tools), what the system prompt says about memory and about a Project. If
you cannot tell, say so and ask, because a wrong guess writes to the wrong
place.

**How old.** When the session's last real work was on an earlier day than
today, or the chat already holds an earlier close, read
`references/stale-and-repeat-closes.md` before planning. It says how to
tell whether the session is stale (later sessions changed what it touched),
which changes what may be written at all.

**Which level.**

| Level | The session | Steps | Checks |
|---|---|---|---|
| Minimal | wrote nothing: questions, reading, a review. No file, commit, note, store entry or install | a memory, only when the user corrected something or stated a preference or a fact that lives nowhere else; plus any step a local map says runs at every level | none |
| Light | short work in one project or repository; no decision bound for a decisions store, no notes, standing instructions or skills changed | memory when there is something to hold, handoff note, context save; plus any step a local map places at this level. The vault sync only when no `SessionEnd` hook already logs the session, and then for the log alone | section 3, the light list |
| Full | anything more: several repositories or projects, a decision to record, notes, instructions or skills changed. Always when the session is stale | every category of the catalogue | all of section 3 |

- Pick from what the conversation shows. Between two levels, pick the
  higher: a close that is too small loses state, one that is too large only
  costs tokens.
- The first line of the plan names the place, the level, the reason and the
  words that change it: `Claude Code on this machine. Light close: one
  repository, short work, no decisions. Say "minimal" or "full" to change
  it.`
- The user changes the level with one word when confirming. Lower: drop the
  steps that level does not have and run the rest. Higher: the word
  approves that level's steps, so do its added reads and checks, say each
  added step in one line and run it without a second question. Ask again
  only when a check turns up something the user has to decide: a choice
  between stores, or a note edit they have not seen.
- No level cuts two things: checking the writes the session claimed, when
  it claimed any (section 3), and the plan's "left broken" line when a
  check finds one (section 4).
- When a check finds more than the level assumed (a second repository with
  changes, a failed write that carried a decision), say so and raise the
  level before proposing.
- A local map may carry its own thresholds and costs per level; they
  replace the ones here.

## 2. The local map, or discovery

Before discovering anything, look in the environment's standing
instructions for a local map of this routine: a short section naming which
installed skill covers each category, the stores, what is retired, measured
costs, any step of its own and the levels it runs at. In Claude Code it
lives in a `CLAUDE.md` file or in auto-memory; elsewhere,
`references/other-environments.md` says where.

In Claude Code read the map from disk, not from context: an injected copy
can predate an edit, and a stale one sends you into full discovery and an
offer to write a second map over one that already exists. Read only the
map, never the whole files. In each `CLAUDE.md` that applies (the user's,
the workspace's, the project's), search the headings for this skill's name
with Grep, and read from the matching heading to the next heading of the
same level. No heading matches: list that file's headings (`^#+ `) and look
for one that reads as a map of the close routine before concluding there is
none.

**With a map,** it replaces discovery. Verify that the skills it names for
the steps this level runs are still installed, against the skill listing
already in context, and treat what it retires as settled. At the minimal
and light levels do not read the catalogue: the map and this file are
enough. Costs come from the map's own figures; when it has none, read only
the catalogue's "Reference costs" section. When a step's run-or-skip call
is not obvious, read that category's section of the catalogue and nothing
else.

**Without a map, or with a partial one** (stores or retirements named, but
no skill per category), read `references/close-out-catalogue.md` whole and
follow its "Discovering without a local map" section.

The skill listing in context can be truncated, and a second one injected
later in the same chat can show fewer skills than the first: before
reporting that a skill the map names has gone, confirm it with a
skill-listing tool when the session has one, and say which source you
checked. A skill shown with a plugin prefix, with or without a bare twin,
is the skill the map names by its bare name: call it by the bare name in
the plan, invoke it with the exact name the listing shows. A step the map
adds may name a tool instead of a skill; when the session does not have
that tool, do what the map says for that case, or skip the step and say
so. A step whose skill is not installed goes in the plan as
"skip, not installed"; do not improvise a replacement.

## 3. Check what the level calls for

**Minimal:** nothing to check. Go to section 4.

**Light:** Git and Claimed writes below, in the one repository the session
worked in. Graphs only if that repository has one: the local map says so,
or a `graphify-out/` folder sits at its root. Work in progress only if the
session itself ran a skill that spreads a job over several sessions.

**Full:** everything below, in every repository the session touched.

- **Git.** `git status`. Uncommitted work is not this skill's to commit;
  it goes in the plan's "stays with the user" line. When the session's
  story and git disagree (files changed in the session, a clean tree),
  name the discrepancy instead of reconciling it silently.
- **Claimed writes.** List what the session said it wrote, created,
  installed or changed (files, notes, commits, settings, packages), and
  check each with a read-only look: it exists, and its content is the one
  the session wrote (a distinctive line or the size, since a failed
  overwrite leaves the old file in place). A tool that reported success is
  not proof. Content that still matches what the session saw before
  writing means the write never landed, whatever the modification time
  says. Otherwise the modification time decides: changed after the
  session's last work means a later session changed it, so the session is
  stale (`references/stale-and-repeat-closes.md`); not changed means the
  write never landed. A file that should exist and does not never landed
  either, unless a later commit or note records removing it. A write that
  never landed, or work left half done (installed in some places and not
  others, a step promised and not run), goes in the plan's "left broken"
  line. A session that claimed no writes skips this.
- **Graphs.** In a light close, only for a repository that has a graph;
  with none, there is nothing to run. Run `python
  scripts/find_graphs.py <root>` (path relative to this skill's
  directory; any Python works), where the root is that repository in a
  light close and the workspace in a full one. It prints
  one line per graph: CURRENT, STALE with counts, or UNKNOWN. Only a STALE
  graph of a repository the session worked in becomes a step; CURRENT is
  never one, even if you remember editing a graphed file. With no Python
  on the machine the graphs are unchecked; say so. The catalogue's
  category 4 has the rest (the workspace root, what the counts mean, when
  to defer).
- **Work in progress** that another skill spreads over several sessions:
  the catalogue's "Work in progress" section says how to find it. Not a
  step of its own; it goes into the handoff note and the context save.
- **Where state already lives.** The local map or the project
  instructions may name the stores the user treats as the source: a vault,
  a project database, one field that holds the next action. Know them
  before planning any write. When two named stores could hold the same
  fact, the plan names which one the write targets, and the single
  question settles it when the instructions do not.

Two rules about stores hold at every level and in every environment.

**Each fact lives in one place.** Before writing a decision into any
store, check whether a store the user already treats as the source holds
it, and write a pointer instead of a second copy. Nothing becomes a store
because it is handy: a Project's documents, a new note or a summary in
chat count only when the project instructions name them. The handoff note
and the context save point at such facts; they do not copy them. A fact a
later step of this same plan will write counts as recorded; if the user
strikes that step when confirming, the earlier steps inherit it.

**The context save goes where the project says.** A place the project
instructions or the local map name for "where I left off" (a field in a
project database, for one) is the context save, and wins over a generic
snapshot skill; without one, the installed snapshot skill is the step. If
an installed skill owns that place (a daily close routine), that skill is
the step, skipped if it already ran this session. Otherwise write there
yourself, with the exact text in the plan. If no project entry covers what
the session worked on, say so and propose nothing. Do not add a second
snapshot elsewhere for the same fact.

## 4. Propose, ask once

Present the plan as a short ordered list, in the language the user is
writing, starting with the first line of section 1. Each step carries the
skill or command that does it, one line on what it will write and where,
an estimated token cost, and a recommendation the user can overrule in one
word: run, skip, or run only if some condition holds. When the "where"
cannot be known without running the skill, name it generically ("its
handoff note"), never an invented path. Close with the total, which is the
sum of the steps listed, not a level's typical range, and a single
question in plain chat; yes, no, a level word or an edited plan are all
full answers, and buttons may accompany the question, never replace it. A
choice the instructions did not settle rides the same question: the plan
names your pick and the answer can overrule it.

How much else appears depends on the level:

- **Minimal:** the first line, its one or two steps, the total, the
  question, and one closing line for what the level leaves out ("not run
  at this level: handoff, vault sync, graphs, context save"). With nothing
  to write, say so in one line and that the chat can be archived: there is
  nothing to confirm.
- **Light:** its steps, one line naming what it skips, and the three lines
  below.
- **Full:** every category, including the ones skipped and why ("graph:
  not installed here"), and the three lines below.

The three lines: what stays with the user because only they can do it,
what could not be checked from here, and any mismatch between the
session's story and the disk, named rather than silently reconciled.

At any level, when a check found any, add **left broken**: one line per
item, saying what the session promised and what the disk shows. The close
does not fix them: a fix is work with its own checks, and the confirmation
meant for saving state must not also approve changes nobody reviewed. The
one exception is a write this close would have made anyway (a note the
session agreed on that never reached the disk is the vault sync step, run
with the failed write named plainly). The handoff note and the context
save carry these lines, and any store write that mentions one words it as
it stands ("not installed yet"), never as done. A fix the user wants now
is a new task after the close.

Costs: the user sees a price before paying it. A local map's own
measurements need no hedging. The catalogue's figures were measured on its
author's machine: in Claude Code scale them to what the session touched
and say the assumption when you cannot know; elsewhere quote them as
estimates from another setup, or leave them out. Never present an invented
figure as measured. Write "~85k", not a fake-precise number.

One confirmation covers the whole plan: where the environment's
instructions require asking before writes, this question is that ask, made
once for the batch. Where they require seeing what a write keeps, changes
and removes, that goes in the plan itself. If a step's own skill insists
on asking (a vault sync skill may, by design), let it: that is its
contract. If the user edits the plan, apply the edits and go. If they say
no, stop.

## 5. Execute in order

Later steps read what earlier ones wrote: memory and learnings first, then
the optional clean-ups when they apply, then the vault sync, then any
graph, then the context save last so it describes the final state. A step
a local map adds runs where the map places it.

Before refreshing a graph, look in the repository's own instructions and
the local map for a dedicated rebuild command: when one is named, that
command is the step, not a generic update.

Invoke each skill with the `Skill` tool and each command with Bash, or
with the device shell when the command belongs on the user's machine. In
Claude Code, auto-memory is the memory directory the system prompt names:
one file per fact in the form it specifies, after checking that no
existing file already holds it. On Windows, write those files with the
Write and Edit tools,
never through a shell heredoc: Bash strips backslashes there, and memory
files carry Windows paths. If a step fails, report it and continue with
the rest.

## 6. Report

One line per step: what ran, what it wrote (path or "nothing to write"),
or the error, and the real cost where a tool reported one, so the
catalogue's or the local map's figures can be corrected when they drift.
Then, in at most three lines, what is left for the user, what was left
broken and what could not be checked. No summary paragraph; a minimal
close reports in one or two lines. When discovery ran without a local map,
offer once to add one (the catalogue says what goes in it). End by saying
the chat can be archived.
