# Project files

Read this when setting a project up for directing, when taking over, or when unsure where something belongs.

A directed project keeps its whole state in files, so any session, including a new director, can pick it up from an opening line. Nothing is handed over in a chat.

## The five files

| File | What it holds | Who writes it | How often it changes |
|---|---|---|---|
| `DIRECTING.md` | The standing setup: where the other files are, the exclusive resources and how each is handed over, how sessions must start, the model policy, the clock's decision points, how work lands, the opening line for a new director | The director, with the user | Rarely |
| `STATUS.md` | The live list of everything open, in progress, done, cut or parked | The director only | After every report |
| Briefs | One per piece of work: what to read, what to build, the acceptance check, how to close out and report | Whoever plans the work; the director writes three kinds (below) | When planned |
| Role files | One per standing role (a design lead, an architect): what it is for, how it works, its tasks and its «State» | The role's holder | As the role works |
| The log | What was done, by whom, what failed | Each work session at close-out | After every piece |

Templates for the first four are in `../templates/`. The log is the project's own (a dev log, git history, PR descriptions); the director never keeps a second one.

## Setting a project up

1. Look for what the project already has before proposing anything. A plan, a briefs file, a spec folder, a dev log or a task list in the repository all count; use their names and point at them from `DIRECTING.md` instead of creating duplicates.
2. Check that there is a plan split into pieces. Without one there is nothing to direct: offer to open a design or planning session, and direct nothing until the plan exists.
3. Propose `DIRECTING.md` and `STATUS.md`, filled from what you found, and show them to the user before writing. The user's yes to setting them up covers the director updating and committing these two files, and only these, for the rest of the project. Every other write still asks.
4. Commit both by path.

## The briefs the director writes

The director builds and designs nothing, but it writes three kinds of brief:

- **A fix brief**, a few lines: the symptom, what was ruled out, the names involved, one goal. For a bug that survived the work session's own attempts, or a fix found in an acceptance check.
- **A design-question brief**, when a brief cannot be built as written: the question, the facts, the sections to read, what to write back. It goes to a design session; the director does not answer it.
- **The shortened version of a brief**, once the user has chosen that cut. The director trims the brief to the chosen version and says what was left out.

Everything else in a brief is the planner's or a design session's.

## STATUS.md

Order and names are fixed (see the template): `Updated: <date> <time> · <project>` line, then `## Resources`, `## In progress`, `## Yours`, `## Next`, `## Blocked`, `## Unverified`, `## Done`, `## Cut`, `## Parked`.

- **Resources**: each exclusive resource, who holds it since when, who is next.
- **In progress**: piece, session title, what it waits on.
- **Yours**: what only the user can do (acceptance checks, manual steps in tools, recording, submitting, merging), each with what it blocks. Mark with `! ` anything at risk of being forgotten: work with no date, a check nobody asked for yet, a step that only matters at the very end.
- **Next**: in order of priority. Only the user reorders it.
- **Blocked**: with what it needs.
- **Unverified**: claims nobody has checked: a session's own «not verified» lines, a build nobody ran, a sound nobody heard.
- **Done**: recent pieces with commit or PR, start and end (with the date), and how long the user's check took when the user says.
- **Cut** and **Parked**: with the date and who chose.

One item per line: `- `, an optional `! `, then fields joined by ` · `. The first field is the ID or short name, the second says what it is, and every later field starts with its label (`held by`, `session`, `since`, `next`, `needs`, `blocks`, `waiting on`, `cut by`, `parked`), except a commit, PR or time range in «Done». A session title always goes inside `«...»`, and a ` · ` inside `«...»` belongs to the title. The format is fixed so other tools can read the file; do not add sections, labels or separators.

### Keeping «Yours» honest

Things get lost when nobody owns them. When setting up or taking over, and again at each decision point, add to «Yours» the checks a project needs before it ships that nobody has asked for yet, marked `! `: a check by someone who has not seen the work, running the final build or release once before shipping it, a manual clean-up before a release, anything only a person can submit. Add each as soon as it is known, with what it blocks.

At each report, repeat only the «Yours» item that decides the schedule. Do not nag the rest. If the user does not answer a status question while busy, keep the work moving and repeat that one item next time.

### Ticks and log entries

Ticks in the plan and entries in the log are the work session's close-out, written in its brief. When one is missing, the director does not write it: that file is not one of its two. Say it in the report and send it back to the session, or ask the user whether to add it.

**The rule that keeps things from getting lost:** before archiving a session, move every open item in its report into `STATUS.md`. A «not verified» line goes to «Unverified», a manual step to «Yours», an idea to «Parked». Nothing pending lives only in a chat or in a log entry.

Keep it short enough to read at a glance: «Done» holds today's and yesterday's pieces; older ones are in the log.

## Where STATUS.md lands

- In a shared checkout, commit it by path like any other file, so a session's commit never picks it up.
- In a project where each session works on its own branch, each session runs in its own worktree and the director's checkout stays on the main branch. Commit `STATUS.md` there, straight to the main branch by path: it is not code, and it must be readable without checking out a branch. Push the main branch only when `DIRECTING.md` says so. If the main branch is protected and refuses the commit, say so to the user and ask how they want it kept.
