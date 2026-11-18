# Project files

Read this when setting a project up for directing, when taking over, or when unsure where something belongs.

A directed project keeps its whole state in files, so any session, including a new director, can pick it up from an opening line. Nothing is handed over in a chat.

## The five files

| File | What it holds | Who writes it | How often it changes |
|---|---|---|---|
| `DIRECTING.md` | The standing setup: where the other files are, the exclusive resources and how each is handed over, how sessions must start, the model policy, the clock's decision points, how work lands, the opening line for a new director | The director, with the user | Rarely |
| `STATUS.md` | The live list of everything open, in progress, done, cut or parked | The director only | After every report |
| Briefs | One per piece of work: what to read, what to build, the acceptance check, how to close out and report | Whoever plans the work; the director writes five kinds (below) | When planned |
| Role files | One per standing role (a design lead, an architect): what it is for, how it works, its tasks and its «State» | The role's holder | As the role works |
| The log | What was done, by whom, what failed | Each work session at close-out | After every piece |

Templates for the first four are in `../templates/`. The log is the project's own (a dev log, git history, PR descriptions); the director never keeps a second one.

## Setting a project up

1. Find where the project lives. If it has no folder or no git repository yet, propose them in the same bundle as the two files, under the same yes: the folder, `git init`, and the plan file that will hold the briefs, which starts with the shared rules and the briefs you write. Creating them is yours, at setup only. If the user declines git, check file times, or whatever version history the project has, in place of commits, and mark every such check «Unverified».
2. Look for what the project already has before proposing anything. If it already describes a way of directing (a section of instructions for an earlier director), say which parts `DIRECTING.md` would replace and which it keeps, and let the user decide. A plan, a briefs file, a spec folder, a dev log or a task list in the repository all count; use their names and point at them from `DIRECTING.md` instead of creating duplicates. List the neighbouring folders on disk, with their dates, before trusting a map, an index or a note that says what exists: an index can be older than the work, and a stale one found this way goes to «Yours», marked `! `. Search the project's notes, instructions and memory for past collisions (two writers on one file, a port taken twice): they are the best source for the list of exclusive resources.
3. Check that there is a plan split into pieces. A list of phases, or of skills per phase, is input to a planning session, not a plan. A partial plan is enough to start when the user has already approved the pieces that gather (research, tooling), each can be given a deliverable and an acceptance check, and one planning or design piece writes the rest. With less than that, offer a planning session, whose brief is yours (below), and direct nothing else until the plan exists.
4. Propose `DIRECTING.md` and `STATUS.md`, filled from what you found, and show them to the user before writing, with the deliverable and acceptance check of each first piece, the sidebar group and your own session's title. «Next» starts in the plan's order (in a partial plan, the gather pieces and then the piece that writes the rest), with one exception: a gather piece whose scope hangs on a decision of the user's that nobody has asked for yet waits for a short scoping round with the user (five to ten choices, each with its trade-off written out), and the answers go into its brief. The round comes after the setup yes, as the first item in «Yours», not inside the setup report. The user confirms or changes the order at setup, and after that only the user reorders it. Decision points come from the plan's own times; you may propose one more, and the user confirms it. With no «Done» times yet, take costs from the log and git, and say so. Tell the user that a session they talk to at length reports to you only when they next write to you: «when that session says DONE, write one line here». The user's yes to setting them up covers the director updating and committing these two files, and only these, for the rest of the project. Every other write still asks.
5. Commit both, and any other file of the setup bundle, by path. If the checkout is not on a branch (a detached HEAD), say so and ask where they should land.

## The briefs the director writes

The director builds and designs nothing, but it writes five kinds of brief:

- **A fix brief**, a few lines: the symptom, what was ruled out, the names involved, one goal. For a bug that survived the work session's own attempts, or a fix found in an acceptance check.
- **A design-question brief**, when a brief cannot be built as written: the question, the facts, the sections to read, what to write back. It goes to a design session; the director does not answer it.
- **The shortened version of a brief**, once the user has chosen that cut. The director trims the brief to the chosen version and says what was left out.
- **A planning brief**, when the plan is missing or partial. It says what the session reads (the user's notes, any list of phases) and what it delivers: the plan as briefs in `../templates/brief.md` format, with the shared rules at the top. It also says that build briefs wait for the design choices they depend on, that an «align the rules» piece follows every design choice and every design review, so the spec and the project's rules say what was chosen before anything is built from them, and that a scope or product choice goes to the user, never to the director. When the planning happened in the director's own session before it took the role, the director also writes the briefs of the gather pieces the user approved there, each with what was already found; input that lives only in the chat (a list of phases, notes) goes into the planning brief itself.
- **A brief from a request the user approved in a design session** that can no longer write it. The director keeps the request's content as given and adds only format, order and resources. An exclusive resource that appears this way, or at any point after setup, is an edit of `DIRECTING.md` shown to the user in the same report.

Everything else in a brief is the planner's or a design session's.

Two things hold for every brief. Its close-out names the file its report is committed to, and the file for its hand-over note if it ends `BLOCKED` (what was decided and how, what it waits for, what is left), in the folder `DIRECTING.md` names; or it says the report stays in the chat. And when the piece is research or a document, its acceptance lines can be counted («every claim carries a URL and the date observed», «at least three sources per section»), with one more line about fit that the user can judge from a five-line summary («this covers what you have to decide about X»). The director checks structure and counts, puts the fit question to the user with that summary, and sends the truth of the content to «Unverified».

## STATUS.md

Order and names are fixed (see the template): `Updated: <date> <time> · <project>` line, then `## Resources`, `## In progress`, `## Yours`, `## Next`, `## Blocked`, `## Unverified`, `## Done`, `## Cut`, `## Parked`.

- **Resources**: each exclusive resource, who holds it since when, who is next.
- **In progress**: piece, session title, what it waits on. A piece whose session reported `DONE` stays here as `waiting on the user's acceptance check`, with the check in «Yours» and what it blocks, until the user accepts it.
- **Yours**: what only the user can do (acceptance checks, manual steps in tools, recording, submitting, merging), each with what it blocks. Mark with `! ` anything at risk of being forgotten: work with no date, a check nobody asked for yet, a step that only matters at the very end.
- **Next**: in order of priority. Only the user reorders it; to add a piece (an early end-to-end check, a fix), propose where it goes. A `needs` field may name another piece (`needs B3`) or a step in «Yours»: a piece is not readied before what it needs is done.
- **Blocked**: with what it needs.
- **Unverified**: claims nobody has checked: a session's own «not verified» lines, a check you could not make, a build nobody ran, a sound nobody heard. When one deliverable leaves many, write one line that points at the deliverable's own «not verified» section.
- **Done**: recent pieces with commit or PR, start and end (with the date), and how long the user's check took when the user says; when they do not, leave that field out.
- **Cut** and **Parked**: with the date and who chose. An idea a session left in its report is `parked by the session`.

One item per line: `- `, an optional `! `, then fields joined by ` · `. The first field is the ID or short name, the second says what it is, and every later field starts with its label (`held by`, `readied`, `session`, `since`, `next`, `needs`, `blocks`, `waiting on`, `status`, `cut by`, `parked`, `why`), except a commit, PR or time range in «Done». In «Resources» the second field is the state, `free` or `held by «...»`. A labelled field may end with a date (`cut by the user 2026-03-14`). A session title always goes inside `«...»`, and a ` · ` inside `«...»` belongs to the title. The format is fixed so other tools can read the file; do not add sections, labels or separators. Rewrite the header line whole, never by pattern, and when the local map names a tool that reads the file, run it after every edit and fix what it flags.

### Keeping «Yours» honest

Things get lost when nobody owns them. When setting up or taking over, and again at each decision point, add to «Yours» the checks a project needs before it ships that nobody has asked for yet, marked `! `: a check by someone who has not seen the work, running the final build or release once before shipping it, a manual clean-up before a release, anything only a person can submit. Add each as soon as it is known, with what it blocks.

At each report, repeat only the «Yours» item that decides the schedule (with no deadline, the one that blocks the most). Do not nag the rest. If the user does not answer a status question while busy, keep the work moving and repeat that one item next time.

When a check of the user's means running something read-only and judging the result, run it yourself and show the output: the user only judges, and judging stays theirs. When one short answer covers several checks («yes to all» for a check with two halves), record only what it covers beyond doubt and ask once about the rest, naming it.

### Ticks and log entries

Ticks in the plan and entries in the log are the work session's close-out, written in its brief. When one is missing, the director does not write it: that file is not one of its two. Say it in the report and send it back to the session, or ask the user whether to add it.

**The rule that keeps things from getting lost:** before archiving a session, move every open item in its report into `STATUS.md`. A «not verified» line goes to «Unverified», a manual step to «Yours», an idea to «Parked». Nothing pending lives only in a chat or in a log entry.

Keep it short enough to read at a glance: «Done» holds today's and yesterday's pieces; older ones are in the log.

## Where STATUS.md lands

- In a shared checkout, commit it by path like any other file, so a session's commit never picks it up.
- In a project where each session works on its own branch, each session runs in its own worktree and the director's checkout stays on the main branch. Commit `STATUS.md` there, straight to the main branch by path: it is not code, and it must be readable without checking out a branch. Push the main branch only when `DIRECTING.md` says so. If the main branch is protected and refuses the commit, say so to the user and ask how they want it kept.
