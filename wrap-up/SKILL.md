---
name: wrap-up
description: Use when the user is about to archive the chat, close the session or finish for now ("voy a archivar", "cierro el chat", "wrap up", "/wrap-up"), in Claude Code or in claude.ai, even when they name none of the skills that save state, and also when the chat being closed is days old and later sessions have moved on. Not for the end of one task while the user keeps working, not for the daily close routine ("cierro el día", which belongs to the planning skill), and not for logging out of a website ("cerrar sesión" in that sense).
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill
---

# Wrap-up

The user is about to archive this chat. Anything that lives only in the
conversation is about to be lost: what was decided, what changed on disk,
what the next session should pick up. Several installed skills each save one
slice of that. This skill's job is to find them, run them in the right order,
and stop after one confirmation.

The set of skills is not fixed: plugins come and go, the user writes new
skills. Never hardcode names; discover them each time from what is installed,
then match against the categories in `references/close-out-catalogue.md`.
The catalogue says what each category is, in what order and at what cost;
this file says how each one runs in each environment. If the two seem to
disagree, follow the catalogue for what and order, this file for how, and
name the disagreement in the report so the user can fix the catalogue.

## 0. Know where you are, and how old the session is

Most of what follows changes with the environment and with the age of the
session, so settle both first and say them in one line at the top of the
plan. Three environments:

- **Claude Code on the user's machine.** A shell on that machine, skills in
  `~/.claude/skills`, hooks that run (including, where one is set up, a
  `SessionEnd` hook that logs each session; the local map or
  `settings.json` says whether one is), repositories and vault on disk. Everything below
  applies as written.
- **claude.ai or a cloud session with a device shell.** The chat runs in a
  Linux container, but a shell tool for the user's computer is listed, so
  commands run there, inside the folders the user connected. The vault and
  any script stored in a connected folder are reachable. This skill's own
  files (the catalogue, `scripts/`) live in the container, not on that
  machine. Hooks do not run. Memory goes through the memory tools, and a
  background pass files durable facts after each turn.
- **claude.ai or a cloud session without that shell.** Files on the user's
  computer are reachable only through the tools that stage a file into the
  container and commit it back, and only while the desktop app is linked.
  Otherwise nothing on their disk is reachable. Hooks and memory as above.

Signals: the platform and working directory, which tools are listed (device
shell, device file tools, memory tools), what the system prompt says about
memory and about a Project. If you cannot tell, say so and ask, because a
wrong guess writes to the wrong place.

Then the age. A close is usually asked for at the end of the work, but a
chat can sit open for days and be closed later, after other sessions have
worked on the same files, notes and skills. The session is **stale** when
anything it touched changed after its last real work: compare the date of
that work (the conversation's timestamps or dated notes) with the
modification times of the files and store entries it touched, a later
commit, a store entry dated later, or a skill it used that the listing now
shows renamed or no longer shows. One such change is enough. The age alone
is a reason to look, not a verdict: a week-old chat nobody built on is not
stale. Say it in the top line with the gap ("last active on 4 Nov; files it
touched changed since").

In a stale session the disk and the stores are newer than the
conversation, so they win:

- Before planning any write, read the current version of each file and
  store entry the step would touch, and plan against what is there now, not
  against what the conversation remembers.
- A decision the session took that a later session already recorded is
  done: point at it, do not write it again. One a later session changed or
  reversed is not this close's to restore: name it as superseded and drop
  it. When the later record covers only part of the decision, or it is
  unclear how much it covers, drop only the part it clearly covers and name
  the rest as possibly superseded; which way it goes rides the single
  question.
- Paths, names and skills the session used may have moved or been renamed.
  Resolve each again before using it. A new form counts only when
  something written since states it (memory, a note, a commit, a skill's
  own description saying what it was called before); use that form and say
  so. When nothing states it, name the old one as no longer resolving
  instead of guessing, and do not write it into a store as if current.
- What is left to propose is what the session decided and nothing since
  has recorded, changed or contradicted. That can be very little; a stale
  close that writes one line, or nothing, is a correct close.

The same chat may already hold an earlier close, run before the user kept
working. Then this close builds on that one instead of starting over: take
its plan and mark each step done (its report says so and the disk
agrees), superseded, or still pending, and check only what happened after
it. A plan the earlier close proposed that the user never answered was not
approved: carry its pending steps into this plan, checked again against the
disk and the rules above, instead of running them or dropping them
silently, and say in the top line that an earlier close exists.

## 1. Discover

Before discovering anything, check the environment's standing instructions
(in Claude Code the `CLAUDE.md` files and auto-memory, which counts as
standing here; in claude.ai the Project instructions, the user's
preferences and memory, and a `Local map for this install` section that a
packaged copy of this SKILL.md may carry) for a local map of this routine: a short section naming which installed skill
covers each category, the stores, what is retired, measured costs. When
one exists it replaces discovery; verify that each skill it names is
still installed (and a named command or path with a cheap read-only look
where one is handy), and treat what it retires as settled. A partial map
(stores or retirements named, but no skill per category) informs discovery
instead of replacing it: honour what it names, discover the rest, and the
offer of section 5 becomes completing that section, not adding a second
one. When none exists, discover as follows and offer at the end to write
one (section 5). In Claude Code read the `CLAUDE.md` files from disk, not
only from context: an injected copy can predate an edit, and a stale one
sends you into full discovery and an offer to write a second map over one
that already exists.

The candidate list is the `available skills` listing already in context
(name + description). It covers local skills, plugin skills and gstack
alike. Two quirks of the listing: a skill shown both with and without a
plugin prefix, same description, is one skill, so call it by the bare name
in the plan, but invoke it with the exact name the listing shows; and the
listing can grow mid-run when a command touches a folder carrying its own
skills, whose late arrivals change the plan only if they match a category.
The listing can also be truncated, and a second one injected later in the
same chat can show fewer skills than the first: before reporting that a
skill a category needs is not installed, or that one the local map names
has gone, confirm it with a skill-listing tool when the session has one,
and say which source you checked.

Read `references/close-out-catalogue.md`. For every category it defines,
pick the installed skill(s) whose description matches its purpose. Known
members are hints, not the answer: an installed skill not listed there
qualifies if its description fits, a listed one no longer installed is
skipped. Watch the near-misses the catalogue flags. When the listing shows a
skill by name only (both environments do this for some), match on the name and
the catalogue's "Recognise by" words, and mark it "(no description)" in the
plan so the user knows the match is weaker.

A category with no installed skill goes in the plan as "skip, not
installed"; do not improvise a replacement, unless the environment has its
own mechanism for that job (section 2). Some categories are not skills (in
Claude Code, auto-memory is written with the Write tool and a graph refresh
is a command); they are steps in the same plan, only where the environment
has them.

Then check what is actually worth doing this session:

- **Graphs.** In Claude Code on the machine, run
  `python scripts/find_graphs.py <workspace-root>` (path relative to this
  skill's directory; any Python works). The workspace root is the session's
  working folder, or the broader folder the project instructions describe
  as holding every repository, when they do. The script lists every
  `graphify-out/` whose project folder sits at most five levels under it,
  and whether files changed since its manifest: one line per graph,
  CURRENT, STALE with changed and deleted counts, or UNKNOWN (no manifest,
  or graphify not importable), or a single line saying none was found. The
  counts do not say whether the changes are notes, ~85k each to
  re-extract, or code, which needs no LLM; say which from what the session
  touched.
  CURRENT is not a step, even if you remember editing a graphed file: the
  manifest knows whether the graph was rebuilt after that. With no Python
  on the machine, the graphs are unchecked; say so. Anywhere else the
  script cannot see the workspace (it runs in the container, the graphs
  are on the user's disk): report every graph as unchecked, which is not
  "nothing to update".
- **The session.** Decisions, corrections, new facts about the user or the
  project, files created or moved? That decides whether memory and learnings
  steps have anything to write. A session that was pure reading may need
  nothing but a context save.
- **Git.** `git status` in each repository the session touched. Uncommitted
  work is not this skill's to commit; it goes in the plan's "stays with the
  user" line. When the session's story and git disagree (files changed in
  the session, a clean tree), name the discrepancy instead of reconciling
  it silently.
- **Claimed writes.** List what the session said it wrote, created,
  installed or changed (files, notes, commits, settings, installed
  packages), and check each with a read-only look: it exists, and its
  content is the one the session wrote (a distinctive line or the size, not
  existence alone, since a failed overwrite leaves the old file in place).
  A tool that reported success is not proof, and a write committed to the
  user's computer through the device file tools can come back with a fresh
  modification time and the old content, so compare the size or a
  distinctive line, never the timestamp alone. When the content differs
  from what the session wrote but still matches what the session saw there
  before writing, the write never landed, whatever the modification time
  says. Otherwise the modification time decides: changed after the
  session's last work means a later session changed it (section 0, stale);
  not changed after means the write never landed. A file that should exist
  and does not never landed either, unless a later commit or note records
  removing it. A write that never landed, or work the session left half
  done (installed in some places and not others, a step it promised and
  did not run), goes in the plan's "left broken" line (section 3). A
  session that claimed no writes skips this.
- **Work in progress** that another skill spreads over several sessions
  (catalogue, "Work in progress"). Not a step of its own: it goes into the
  handoff note and the context save.
- **Where state already lives.** The project instructions may name the
  stores the user treats as the source: a vault, a project database, one
  field that holds the next action. Read the instructions before planning
  any write (the stores themselves are read by the steps that write them);
  they decide how categories 3 and 5 run. When two named stores could hold
  the same fact (a decisions note and a project note, say), the plan names
  which one the write targets; if the instructions do not settle it, settle
  it in the single question, never silently.

## 2. What changes with the environment

In Claude Code, run each category as the catalogue describes; of what
follows, only the rules that say so bind there too. In the other two cases
of section 0, adjust like this.

**1 Memory: check, do not write.** The background pass already files
durable facts after each turn. Read the memory file(s) it is likely to have
used (the listing shows the paths) and say in the plan whether this
session's decisions are there. The pass runs after each turn, so what was
decided in the closing turn itself is not there yet and will be filed after
it; that is normal, not a gap. The platform only allows a memory write on
the user's explicit request, so if something they said is missing, name it
in the plan and let them say "save it"; that sentence is the request. Inside
a Project, writes go in the Project's own subtree, in the form the memory
instructions require.

**1b Handoff note, 2 Learnings: skip when not installed.** There is no
replacement; a Project document, a new note or a chat summary does not
become one (see the one-place rule).

**3 Vault sync: depends on reach.** With a device shell and the vault folder
connected, run the sync skill if it is installed; if it needs something this
environment lacks, it will say so, and then do the sync by hand. Without a
shell, the device file tools still reach the vault while the computer is
linked, so the sync skill is still the step: run it, and do the sync by
hand only when it is genuinely not installed (confirmed with a
skill-listing tool, not from the injected listing alone) or when it says it
cannot write from here (a sync skill may fall back to text for the user to
paste), and then write through the file tools yourself instead of handing
the user text. Either way, read the vault's own conventions note first
(stage it when there is no shell), and put each proposed change in the plan
as what stays, what changes and what disappears, so the single confirmation
covers the writes. After each write that goes through the file tools,
confirm it landed by listing the folder and checking the file's size,
because the commit reports success either way. The session log a hook
writes does not exist here; say so.

**4 Graph: unchecked**, as section 1 says. Not "nothing to do".

**5 Context save: write where the project says.** This holds in Claude
Code too: a place the project instructions name wins over a generic
snapshot skill, and without one the installed snapshot skill is the step.
If the project
instructions name one place where "where I left off" lives (a field in a
project database, for one), that place is the context save. If an installed
skill owns that place (a daily close routine), that skill is the step; if it
already ran this session, skip. Otherwise write there yourself. The plan
carries the exact text proposed for that place, so the one answer covers
it; that rule applies when you write the place yourself, while a skill
that owns the write composes its own content, in Claude Code or anywhere.
If no project entry covers what the session worked on, say so and propose
nothing: the user decides whether one should exist. Do not also add a
handoff note or a snapshot elsewhere.

**6, 7 Optional: skip** unless the session corrected a memory or changed a
rule that a `CLAUDE.md` describes.

One rule holds everywhere: each fact lives in one place. Before writing a
decision into any store, check whether a store the user already treats as
the source holds it, and write a pointer instead of a second copy. Nothing
becomes a store because it is handy: a Project's documents, a new note or a
summary in chat count only when the project instructions name them. The
handoff note and the context save point at such facts ("decision X, see
the project note"); they do not copy them. A fact a later step of this
same plan will write counts as recorded; if the user strikes that step
when confirming, the earlier steps inherit it, so adjust before running.

## 3. Propose, ask once

Present the plan as a short ordered list, in the language the user is
writing. Start with the one line saying where you are running. Each step
carries four things: the skill or command that does it, one line on what
it will write and where, an estimated token cost (skipped steps carry
none), and a recommendation: run, skip, or run only if some condition
holds. The "where" comes from the skill's description or its own files;
when it cannot be known without running the skill, name the destination
generically ("its handoff note"), never an invented path.
Include the steps you are skipping and why ("graphify: not installed here").
Close with the total, then ask a single question in plain chat; yes, no,
or an edited plan are all full answers. A choice the instructions did not
settle (which store takes a fact, say) rides this same question: the plan
names your pick and the answer can overrule it. The question lives in plain chat
even where the harness draws buttons; buttons may accompany it, never
replace the editable answer.

Also say, in a line each, what stays with the user because only they can do
it, what could not be checked from here, and any mismatch between the
session's story and the disk (section 1, Git), named rather than silently
reconciled. Those lines are part of the plan, not an afterthought.

Add one more when section 1 found any: **left broken**, one line per item,
saying what the session promised and what the disk shows. The close does
not fix them. A fix is work, with its own checks and questions, and folding
it into this plan would let the single confirmation meant for saving state
also approve changes nobody reviewed; it would also make the close depend
on work that can fail. The one exception is a write this same close would
have made anyway: a note the session already agreed on that never reached
the disk is the vault sync step, not a fix, and it runs as that step with
the failed write named plainly. The handoff note and the context save
carry these lines, so the next session meets them first, and any store
write that mentions one words it as it stands ("not installed yet"), never
as done. If the user wants one fixed now, that is a new task after the
close.

The cost matters because the steps are not equal: most cost a few thousand
tokens, a graph update tens of thousands per changed note, and this
skill's own rule is that the user sees a price before paying it. The
catalogue's figures were measured on the author's machine; a local map's
own measurements, where it has them, replace them and need no hedging. In
Claude Code use them scaled to this session: pick within each category's
range from what the session actually touched, and say the assumption when
you cannot know. Elsewhere, quote them as estimates from another setup, or
leave the figure out. Never present an invented figure as
measured. Write "~85k", not a fake-precise number.

The recommendation is your judgement, stated so it can be overruled in one
word: "run" when the step has something to write, "skip" when it does not,
"run only if you want the graph current today" when the cost is high and
the benefit can wait.

On a fresh install the plan may be one real step and six "skip, not
installed". That is a correct close, not a failure: run what exists (in
Claude Code, auto-memory at least), improvise nothing, and make this the
close that offers the local map (section 5).

One confirmation covers the whole plan. This skill asks once before
writing anything to disk; where the environment's instructions require
asking before writes, this question is that ask, made once for the batch.
Do not ask again before each step. Where the project instructions
require seeing what a write keeps, changes and removes, that goes in the
plan itself (section 2), not in a second question. If a step's own skill
insists on asking (obsidian-project-sync does, by design), let it: that is
its contract, not yours to override.

If the user edits the plan, apply the edits and go. If they say no, stop.

## 4. Execute in order

Order matters because later steps read what earlier ones wrote. Follow the
sequence the catalogue gives: capture what was learned first (memory,
learnings), then the optional clean-ups when they apply, then push to the
vault, then refresh any graph built from the vault, then save resumable
context last so it describes the final state. List skipped optionals
wherever reads best; the order only matters for steps that run.

Before refreshing any graph, read the repository's own instructions: when
they name a dedicated rebuild command, that command is the step, not the
catalogue's default invocation. A repository knows what its graph needs;
the catalogue does not.

Invoke each skill with the `Skill` tool. Run each command with Bash, or
with the device shell when the command belongs on the user's machine. In
Claude Code on Windows, write memory files with the Write and Edit tools,
never through a shell heredoc: Bash strips backslashes there, and memory
files carry Windows paths. If a step fails, report it and continue with the
rest; a broken graph update must not block the vault sync.

## 5. Report

One line per step: what ran, what it wrote (path or "nothing to write"),
or the error, and the real cost where a tool reported one (graphify
subagents do; note it so the catalogue's or the local map's figures can be
corrected when they drift). Then, in at most three lines, what is left for
the user, what was left broken and what could not be checked. No summary paragraph. When
discovery ran without a local map, offer once to add one to the
environment's standing instructions: a few lines naming the skill per
category, the stores, what is retired, so the next close skips discovery.
End by saying the chat can be archived.
