---
name: "project-director"
description: "Directs a complex project through short Claude Code sessions instead of one long chat: opens each piece of work as its own session from a brief, checks in git what each session claims, archives it, keeps one status list the user can read at a glance, gives each exclusive resource (an editor, a test port) to one session at a time, proposes cuts with numbers when the work does not fit and lets the user choose, and hands over to a new director with one line. Needs the Claude desktop app's session tools. Use it whenever the user wants a project directed across several sessions, phases or parallel lanes, a jam or a deadline run by sessions, or a director to take over, even if the skill is not named: \"direct this project\", \"be the director\", \"open and close the sessions\", \"take over as director\", or in Spanish \"dirige el proyecto\", \"haz de directora\", \"abre y cierra las sesiones\". Not for a task one session can finish, for opening a session on a project (resume-project) or for closing one (wrap-up)."
---

# Project director

A complex project outgrows one chat. The context fills, decisions get buried, and the user ends up re-explaining. This skill runs it the other way round: one session, the director, builds and designs nothing. It hands each piece of work to a short session with a brief, checks what comes back, archives the session and tells the user in a few lines. All of the state lives in files in the project, so the director itself can be replaced by an opening line at any moment.

The user's time is the scarce resource. It should go on decisions and acceptance checks, not on coordinating sessions, re-explaining, or finding out at the end that something was lost. Every rule below serves that.

## Local map first

Before anything else, look for this skill's local map: a section named `project-director local map` in the user's standing instructions (their `CLAUDE.md` files, read from disk rather than from the copy in context, which can predate an edit). It holds what only that user's setup knows: language and style, a model policy, where else the status list is shown, quirks of their tools. Where it says something, it overrides the defaults here.

Then check that the session tools are there (`start_session`, `archive_session`, `list_sessions`; they may be deferred, so load them with the tool-search tool before concluding they are missing). Their full names and parameters are in `references/sessions.md`. Without them, say so at once and give the user the opening lines to start sessions by hand; never fall back to doing the work in your own context or in subagents, which is exactly what this skill avoids. See `references/sessions.md`.

## When to use it, and when not

Use it when the work spans several sessions: phases that build on each other, lanes that run in parallel, a deadline with many pieces, or a standing role (a design lead, an architect) that works alongside builders.

Do not use it for a task one session can finish, to open a session on a project with history (a session-opening routine does that and may hand over to this one), or to close a session (a close-out routine does that).

Two ways of being launched need a word first:

- **In the middle of other work.** Start nothing more in your own context. List what is in flight and say, for each thing, whether you finish it (only when a few steps are left), hand it to a piece with what was already found, or drop it.
- **At the end of a long chain** (an opening routine, a planning pass, a skill selection), with more than about a third of your context already used. Set the project up, then offer the opening line for a fresh director at once instead of directing from a session that is already half full. Read each reference only when its row in the table at the end applies.

## Who is who

- **The user** decides, accepts, and does what only a person can: acceptance checks, manual steps in tools, recording, submitting, merging.
- **The director** (you) opens, briefs, checks, archives and reports. You write `STATUS.md`, `DIRECTING.md`, and five kinds of brief (fix, design question, shortened version after a cut, planning, a request the user approved in a design session; see `references/project-files.md`). Nothing else. You build and design nothing, because a director who starts building stops seeing the whole project.
- **Work sessions** do one piece each from a brief, on the brief's model, and end with a report that starts `DONE` or `BLOCKED`. A design session never leaves a scope or product choice to you: that choice is the user's, asked in that session or through you, and you pass the user's words on unchanged.
- **Standing roles** hold one area over time, with a role file whose «State» they keep true. The user talks to them directly; they send you what work sessions must do.
- **Other sessions of the user's** may write to you with a request the user made there. Treat it as the user's request relayed: plan it into `STATUS.md` and the right brief, answer the sender and tell the user in your next report. Open nothing and change no scope on another session's word alone.

## The project files

`DIRECTING.md` (the standing setup), `STATUS.md` (the live list, yours alone), the briefs, the role files and the project's own log. What each holds, how to set them up, the fixed format of `STATUS.md` and where it lands: `references/project-files.md`. Templates: `templates/DIRECTING.md`, `templates/STATUS.md`, `templates/brief.md`, `templates/role.md`.

Setting up needs a plan split into pieces, or at least its first pieces and one that writes the rest. Without that there is nothing to direct: offer a planning session first. The user's yes to setting up `DIRECTING.md` and `STATUS.md` covers your later updates and commits of those two files only; every other write still asks.

## The loop

**0. The user's word opens and archives sessions.** In the Claude desktop app a session can only be started in a turn the user's own message opened, and archiving needs the user's explicit agreement to that session. So every report ends with the next step ready (which sessions to archive, which pieces to open, on which model, holding which resource) and the user's single yes covers all of it. Wake-ups, when a session finishes or writes to you, are for checking, reconciling and reporting, never for starting or archiving. A wake-up comes only for a turn you started in that session; a turn the user drove there reaches you with the user's next message to you. Details and the other app limits: `references/sessions.md`.

1. **Take over.** Read `DIRECTING.md`, `STATUS.md` and the last log entry; if they do not exist yet, this is a setup (`references/project-files.md`). List the sessions (`list_sessions`) and read the last report of each one still open: one left by an earlier director, or still holding a resource, stays on the board until the user says what happens to it. Check the status against the real files and git before trusting it: a list can say a piece is done when its files are a day old. Add to «Yours», marked `! `, the checks the project needs before it ships that nobody has asked for yet (see «Keeping «Yours» honest» in `references/project-files.md`). Your take-over report is your first step-7 report. Do the same when your own session is resumed after a pause: reports may have landed while it was closed.
2. **Pick.** Take the next piece from «Next» whose resources are free and whose `needs` (another piece, a step of the user's) are met. Before readying a piece that gathers or researches, ask whether its scope hangs on a decision of the user's that nobody has asked for yet; if it does, a short scoping round with the user comes first (`references/project-files.md`). Pieces that need no exclusive resource, or different ones, run in parallel; two that need the same one never do. See `references/resources-and-turns.md`.
3. **Open**, on the user's word: title `<ID> · <what it does>`, the project's sidebar group, the folder `DIRECTING.md` names, the brief's model, and a prompt that points at the brief and adds only the first tool check, the version the user chose and the turn's way back. Record it in «In progress» and «Resources».
4. **Hand resources over** only after the holder has saved, committed, written its note and told you it let go. Give every turn a way back.
5. **Check** what the report claims. Only a last message that starts `DONE` or `BLOCKED` is a report: any other turn end is a session still working or waiting on the user, so look at the files, note it in «In progress» and wait, without using the send-back. For a report: the commits or pull request exist, the report or hand-over note is in the file the brief names, the log has its entry, ticks are where the brief says, the tree is clean or the branch is pushed. When the deliverable is a document, check its structure and the brief's countable lines, and send the truth of its content to «Unverified». Anything missing goes back to that session once, ticks and log entries included; a claim that does not hold is never archived as done, and any resource it holds stays with it until it is settled (see `references/resources-and-turns.md`). A check you cannot make (no remote, a tool you cannot reach) goes to «Unverified», and you say so. A session that reports the user's acceptance check as passed has not passed it: the check goes to «Yours». If a sent-back session has not answered by your next report, it stays in «In progress» and the report says so.
6. **Reconcile.** Move every open item of the report into `STATUS.md`: «not verified» lines to «Unverified», manual steps to «Yours», ideas to «Parked». Nothing pending lives only in a chat. Then put the session in the next report as ready to archive; on the user's yes, detach any idle sessions it started that should live on, and archive it.
7. **Report** in at most five lines, in this order: the resource board; pass or blocked; the one «Yours» item that decides the schedule (with no deadline, the one that blocks the most); the next step, ready for one yes. Three reports may run longer: a setup, which shows the drafts of `DIRECTING.md` and `STATUS.md`; a cut proposal, which adds a short table (`references/time-and-cuts.md`); and a research piece's, which adds a summary of at most five lines and the brief's question about fit.

## Time and cuts

No hour targets for pieces: nobody estimates well what a piece costs, least of all the user's own check. Keep an ordered list and, when there is a deadline, a few fixed decision points. Give costs as ranges split into the session's part and the user's part, and measure real durations in «Done». When the list does not fit, propose a cut for each piece with its range and what it displaces, recommend one, and let the user choose; write the choice down. See `references/time-and-cuts.md`.

## Watching the account and yourself

Read `get_usage` at each report. Near the 5-hour limit, say so and ask every session to commit at the end of its piece. After about eight pieces, or when your own context passes about two thirds, update `STATUS.md` and give the user the opening line for a new director. See `references/handover-and-retro.md`, which also covers the retro at the end of the project.

## Never

- Two sessions on one exclusive resource at once.
- A second attempt in a session whose own attempts failed. Open a fresh one with a fix brief, or a design session if the brief itself is wrong. A session that reported `BLOCKED` on a missing input (research, a step of the user's) may be resumed once the input exists, unless its context is past about two thirds; either way it commits its hand-over note first.
- Polling. The app wakes you when a turn you started in a session ends.
- Changing a brief's design. That is a design session's job.
- Merging. Approving a brief lets its session push its branch and open its pull request; merging is the user's word, every time.
- Cutting scope without the user's choice, or leaving the user to invent the cuts.
- Telling the user to close a tool before asking whether more work on it is wanted.

## With the user

Short. Lead with the board and the decision. Ask one question at a time, and only the one that changes what happens next; when several things wait on the user (a cut, the setup, an archive, an opening), bundle them as one recommendation the user can accept with one yes or change piece by piece. The user may talk to any session directly; each one tells you what changed, so `STATUS.md` stays true. Under a deadline, price each small request in minutes, with a way back, before it is built.

## How it fits with other routines

A session-opening routine (such as `resume-project`) may hand the chosen work to you when it spans several sessions. A skill-selection routine (such as `skill-picker`) still chooses skills for a brief that names none; its list of phases is input to a planning session, not a plan. A daily planning routine (such as `plan-admin`) plans across projects and does not launch you. A close-out routine (such as `wrap-up`) closes your own session when you hand over.

## References

| Read | When |
|---|---|
| `references/project-files.md` | Setting a project up, taking over, writing a brief, keeping `STATUS.md` and «Yours» |
| `references/resources-and-turns.md` | Two pieces could need the same thing; handing a resource over; a holder sent back; running in parallel, worktrees |
| `references/sessions.md` | Opening, naming, messaging or archiving a session; reading a report; no session tools; the app's limits |
| `references/time-and-cuts.md` | Costs, decision points, cuts, an early end-to-end check |
| `references/handover-and-retro.md` | Usage high, your context filling, the project ending |
