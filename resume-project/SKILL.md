---
name: "resume-project"
description: "Session-opening routine for a project with history, or for an umbrella project that holds several: gathers what earlier sessions left behind (a project manager such as Notion, a session log if the setup writes one, git, an Obsidian vault, handoffs, chats, memory and project files), cross-checks it, summarises where everything stands, asks what to work on today and hands the answer over to a skill-selection skill if one is installed. Chooses its sources from the tools available in the session, not from the name of the environment. Use it when opening a session even if the skill is not named, with phrases such as \"let's pick up\", \"where were we?\", \"carry on with my-app\", \"open a session on X\", \"let's start\", \"/resume-project\", or the equivalent in the user's language (in Spanish, for example, \"retomamos\" or \"¿por dónde íbamos?\"). Do not use it midway through a session that is already working, or to create a project from scratch."
allowed-tools: Read, Glob, Grep, Bash, Skill, AskUserQuestion
---

# Resume project

When a session opens, what matters from the earlier ones is spread across several places. This skill makes the way back: it gathers it, checks it against the most recent information available and tells the user in a few lines, so they can decide what to work on today without having to remember anything.

Four things shape how it works:

- **Read only.** It writes to no file, note, database or memory. That is why it does not ask permission for each step: reading changes nothing. Copying a file from the user's computer into the session to read it counts as reading. The only write allowed is `git fetch --prune`, and only where `references/claude-code.md` says so. Giving the session access to a new repository is not just reading: do not do it on your own (see the GitHub row in step 0). Hooks from other plugins may write when the session opens (consolidating memory, saving logs): that is not this skill writing and needs no mention, unless it changes a source you are about to read.
- **Reads files, does not launch workflows.** Several skills, when launched, write telemetry or state, create folders, ask for their own output format or end with their own question. When you know where a skill stores its data, read that file directly. Launch the skill only if there is no other way, and in that case take its data, skip its final question and its format, and stop any step that writes.
- **Project instructions take precedence.** If the project instructions, a `CLAUDE.md` or the user's preferences say where state lives, which folders can be read, how conflicts are resolved or how the day is planned, that comes before this skill.
- **Ends with a question and a handover.** A session close-out skill (for example wrap-up) ends by saying the session can be archived; this one ends by asking what to work on today and passing the answer on (step 6).

## 0. Inventory: what you can actually read

Do not choose the sources from the name of the environment. The same session can be in the cloud, inside a claude.ai project and linked to the user's computer all at once. Before reading anything, look at the tools the session has (deferred ones too, by searching for them) and note which of these capabilities are present:

| Capability | How to recognise it | Sources it opens |
| --- | --- | --- |
| Terminal in the repository | The working folder is one of the user's repositories, or there is a terminal on their computer (`device_bash` or similar) with the repository in a connected folder | Git and the remote (C), with `references/claude-code.md` |
| Computer files without a terminal | Tools to list and copy files from the computer, without a terminal | Vault (D), session log (B, if the setup writes one) and handoffs (E) if they are in a connected folder, and the `CLAUDE.md` of a repository whose folder is connected (D). **Not** local git |
| GitHub without a terminal in the repository | `gh` installed in the session, or a tool to add repositories to the session | Pull requests, branches and commits on the remote (C2) |
| Project manager | A Notion connector or another project manager, plus instructions or a `CLAUDE.md` that say which database or page holds the projects | Status, next action and tasks (A) |
| Previous chats | Tools to search or list chats | Chats (F), with `references/claude-ai.md` |
| Claude Code sessions | Tools to list or search the desktop app's sessions (`list_sessions`, `search_session_transcripts`, `list_events` or similar) | Previous sessions (F2), with `references/claude-code.md` |
| Published artifacts | Tools to list published artifacts, pages or documents (`Artifact` with `list`, or similar) | Deliverables outside the repository (I) |
| Memory | Memory in the context, or memory tools | Memory (G) |
| claude.ai project | Project instructions or files in the context, or a project tool | Instructions and files (H) |

The references give the detail for git (`references/claude-code.md`), for claude.ai chats (`references/claude-ai.md`) and for a per-project session log written by a hook (`references/session-log.md`). Read only the one opened by a capability you have, and `session-log.md` only if the setup writes such a log. If a reference says something is not there (vault, disk, git) and the inventory says it is, the inventory wins. If a reference is missing, carry on with what this file says.

If the session has many deferred tools, do not load them all to take the inventory: search for the words in the table (`notion`, `session`, `transcript`, `chat`, `memory`, `project`, `repository`, `artifact`) and load the schema only for those you are going to use. `gh` is not a session tool but a program: check it with `gh auth status`. If the names of the deferred tools are already visible in the context, choose from that list and load only those, without searching.

The source letters in this file (A to I) are not those of `claude-code.md` (A to H): E here is handoffs, while E in that reference is the `CLAUDE.md`. When this file cites a category of `claude-code.md`, it cites it by name; look it up by the name, not by the letter.

**Allowed folders.** Read only the folders the user connected to the session or that their instructions allow you to read, and that the session can actually reach. Do not ask for access to any of them in order to resume. Put everything that is out of reach into a single "Heads-up" line:
- useful sources outside the connected folders (for example `~/.gstack` in the home folder, in a session without a terminal);
- folders the instructions allow you to read but that are not connected (for example a project's own folder). If one belongs to a project that appears in the summary, add that all that is known about that project is what the project manager says.

## 1. Which project it is

- **A repository, a folder or a name.** If the session is in a repository, that is the project. If the user names it, look for it in the project manager (A) and in the vault (D), case-insensitively and trying the aliases that memory gives: the names may not match, and a project may be in the middle of a rename.
- **An umbrella.** If the context is a space with several projects (a claude.ai project that organises all the work, a project manager with a projects database, a vault with several folders) and the user does not name one, do not choose silently. Write a multi-project summary (step 4) with those that have the most recent activity and those the instructions mark as short-term priority.
- **What the user takes for granted.** If the opening message asserts a state (an unfinished git operation, a branch, a PR, a deployment), check it against the sources as soon as you read them: the quick git snapshot, GitHub or, if there is one, the session log. If it does not match, say so in one line before the summary, with what each one says. If what it names belongs to another project (another folder, repository or note), ask which one is being resumed before reading further; in a session without a user, carry on with the working folder's project and say so at the top of the summary.
- **Nothing to resume.** No notes, logs, chats or commits: say so in one sentence and move on to step 6 with whatever the user wants to do.

### How the same project is matched across sources

The project manager, the vault and, if there is one, the session log each name projects in their own way. Match them by keys, in this order, and not by the bare name:

1. **Path.** If the setup writes a session log, its path against the `path:` field in the frontmatter of the vault note (D), as "Matching by path" in `references/session-log.md` describes.
2. **Project manager link.** The project manager field that points to the note (in Notion, for example, a field such as "Obsidian note"), against the note's folder.
3. **Name.** Case-insensitively and with the aliases from memory.

If a project in the project manager does not link its note but the note exists (it matches by path or by name), say so in "Heads-up" in one line.

## 2. Sources, in reading order

First what tells you how much each note is worth (what really happened and when), then what tells you what is next, and finally the why.

**B. Session log, optional.** If the setup writes one, follow `references/session-log.md`.

**C. Git and the remote.** Only with a terminal in the repository. Follow the "Quick git snapshot" and the "Actual state of git and the remote" category of `references/claude-code.md`.

**C2. GitHub without a terminal.** Use it to confirm what the local sources cannot know: whether a branch was pushed, whether it has a pull request and whether it was merged. Get `owner/repository` from the project's vault note (`url:` field or a `github.com/...` line), from the `CLAUDE.md` or, if there is a session log, from its `Merge pull request #N from <owner>/...` commits.
- First check whether the session already has access with a read: `gh api "repos/<owner>/<repo>/pulls?state=all&sort=updated&direction=desc&per_page=10"`. Use the REST API (`gh api repos/...`): `gh pr list` can fail because GraphQL is not always available. Each PR has `created_at` and `merged_at`: when it went in is given by `merged_at`, not by the creation date.
- If it responds, also read the branches (`repos/<owner>/<repo>/branches`) and the latest commits on the main branch (`repos/<owner>/<repo>/commits?per_page=5`). With that, an unmerged branch that another source names becomes "has open PR #N", "merged" or "not on the remote".
- Also read the CI of the main branch (`repos/<owner>/<repo>/actions/runs?branch=<main>&per_page=1`). If the last run failed, it goes in "Pending"; if it passed, do not mention it, and if there is no run at all (the repository has no CI), do not mention that either.
- If it responds that the repository is not enabled for the session, **do not add it on your own**: granting access to a repository is not just reading. Note it in "Heads-up" and offer it as an option in step 5 ("Confirm on GitHub"). In a session without a user, skip it.

**A. Project manager.** If the instructions say that status, priority or next action live in a project manager (Notion or another), read it: it is the source for what is next. Get the database address from the instructions or from the `CLAUDE.md`; do not search for it by name if you already have it.
- In Notion: get the database schema and query the rows with their link (`url`), name, area or branch, status, priority, key date, next action and note.
- **Archived.** Remove the rows Notion has archived and, if the database also has its own checkbox or status for that (for example an "Archived" checkbox or a "Closed" status), also the ones that have it set.
- **Edit dates.** The query does not return the last-edited date. Open the page of the rows you are going to check against another source and, in an umbrella, also those of the projects the instructions mark as short-term priority, even if they have no log or note: that way projects without code can also make it into "Where you left off".
- **Bulk edits.** If several pages in the same database have edit dates a few seconds apart, it was a change made to all of them at once (a new field, an import, a template), not work on those projects. Do not use that date as activity: leave those projects undated, unless another source gives them a date.
- **Tasks.** If the instructions name a tasks database, get its schema and query the unfinished tasks that are overdue or due in the next seven days. Only those of projects that appear in the summary count: those of paused, closed or out-of-summary projects are not pending even if they are overdue. They go in "Pending" under their project's item, with their date. For priority projects with no next action, also query their open tasks with no date filter (see below).
- **Tasks without a project.** They do not go in "Pending". But if one matches a "Heads-up" warning (for example, a task to link the notes when a project does not link its own), name the task in that warning instead of presenting it as a new finding.
- A row with no next action is not a pending item: do not make one up. If the project is a priority one, put it in "Pending" as "no next action". If it has open tasks, with or without a date, name the first one (the one with the nearest date, or the first undated one): "no next action; open task: <task>". This is data from the project manager, not a suggestion. **Priority** means what the instructions mark as short-term priority, plus the first of their long-term priorities; if the instructions set no priorities, the highest priority in the project manager. The project manager saying "High" is not enough when the instructions set others.
- **If they do not fit.** "Pending" has at most five items. If there are more projects to include, the short-term ones and those with a next action or something half-done go in first; priority projects that would only add "no next action" are grouped into one "Heads-up" line: "No next action: X, Y and Z".
- If the project manager's status clearly contradicts another, more recent source (for example, "Idea" in the project manager and the vault note with work done), say so in "Heads-up" with both dates.

**D. Obsidian vault.** The project note, in the vault's projects folder (the instructions or the `CLAUDE.md` usually say which; in a PARA-style vault, for example, `2 Projects/<project>/`), and its `updated:`. Its `path:` field, if it has one, is a key for matching it (see step 1). Read the header and the latest entries, not the whole note. No skill is needed to read it. In Claude Code, the reference says when to launch a vault skill and when not to.
- **The repository's `CLAUDE.md`.** If it can be reached (a terminal, or the repository folder connected), its state and pending sections ("Current state", "Pending") are the most reliable pending list available locally; read only those sections. With a terminal, follow the "Auto memory and CLAUDE.md" category of `claude-code.md`. Without a terminal you cannot know whether the branch is behind: say it as "according to the `CLAUDE.md` of <file date>".

**E. Handoffs and context checkpoints.** Handoff note (the `remember` plugin), context checkpoint and learnings (the `gstack` plugin). This source applies only if those plugins are installed; otherwise skip it. With a terminal in the repository, follow the "Handoff note", "Context checkpoint" and "Project learnings" categories of `claude-code.md`, and read them right after the "Quick git snapshot", which is their place in that reference's order, not at the end.
- **Handoff note.** It lives in the project folder, not in the home folder: `<project folder>/.remember/remember.md`. It can be read with or without a terminal, as long as the project folder is within reach. Its date is the one in the text itself if it has one; if not, the file's. The rest of `.remember/` (`now.md`, `today-*.md`, `recent.md`, `archive*.md`, `core-memories.md`) is the plugin's history, not the handoff: read it only if the user asks about something in the past.
- **Context checkpoint and learnings.** They live in the home folder (`~/.gstack/projects/<slug>/`) and their path comes from a command, so without a terminal they cannot be read: if the folder exists, it goes in the "out of reach" line of "Heads-up".
- **What is not a handoff.** The `logs/` and `tmp/` subfolders of `.remember`, the vault's `.remember` folder and any `.gstack` inside the vault or a project folder hold those tools' logs (browsing, notifications, temporary files). Do not read them. A `.remember` folder without `remember.md` has no handoff.

**F. Previous chats.** If there are chat tools, see `references/claude-ai.md`. If there are none, do not mention it unless they were the only possible source.

**F2. Previous Claude Code sessions.** If there are tools to list or search the app's sessions, see the "Previous sessions" category of `claude-code.md`. They are useful above all for the why and for what was left half-done; the state comes from git, the notes and, if there is one, the session log.

**I. Artifacts and deliverables outside the repository.** If there are tools to list published artifacts (pages, design boards, documents in a connector), list them and keep those that match the project by name or alias. Only those updated after the project's last commit count (or after its last session with activity, if there is no git): this is work that git, the notes and the session log do not see. They go in "Where you left off" with their date, converted to local time. The title and the date are enough; open them only if you need to know what was left half-done. If the most recent session of the project left no commits, look at it in F2 too, for the same reason.

**G. Memory.** It may arrive in full, as an index or only through tools. Read the files that talk about the project. Its files and many of its lines carry dates: use them to tell whether it is behind. It is useful above all for the why, the decisions and name aliases; for the state, only if it is all there is. If a fact in memory (a path, a name, a status, a phase, a count) clashes with a later source, do not take it as good or correct it: name it in "Heads-up" as memory that may be behind, with its date. The same goes if it leaves something for a phase, a PR or a step that a later source considers finished (for example, "moved to D4" when D4 is already merged): do not present it as either pending or resolved.

**H. Project instructions and files.** The instructions say what the project is and how it is worked on, not the state, unless they say "current state" with a date. For the files, see `references/claude-ai.md`.

**The set of skills is not fixed.** Plugins get installed and uninstalled, and the user writes new skills. The skill names in this file and in the references are hints: look them up each time in the session's list. One that fits by description also works, and one that is not there is skipped.

**For each source, note its date** (the one in the frontmatter, the edit date in the project manager, the one in the text itself or, as a last resort, the file's) and **convert them all to local time before comparing them**. Some file tools give dates in milliseconds since the epoch; GitHub and Notion dates arrive in UTC. Without a date you cannot decide which source is behind.

## 3. If the sources disagree

First check whether the project instructions say what to do. If they say to flag it and not choose, do not choose: put both versions in "Heads-up", with their dates, and in "Pending" leave the item marked "to be confirmed" instead of crossing it out or treating it as done.

If they say nothing:

- **On state** (what is done, merged or deployed), what records facts and is most recent wins: git and the remote, or GitHub if it could be read; if not, among the notes (the vault note and, if there is one, the session log), whichever has the newest facts (more commits, PRs or merges), not whichever file was modified last; in claude.ai, the most recent chat.
- **On what is next** (priority, next action), the project manager wins, even though its next action may have gone stale: if a later source considers it done, say so in "Heads-up".
- **On the why and the decisions**, the notes, the instructions and memory win, even if they are behind on state.

Flag the difference in "Heads-up" without fixing it. Bringing things up to date is work for the session and can be one of the options in step 5.

## 4. Summarise

A short block, in this order. Leave out any line that has nothing. Write the labels in the user's language; the English names below are the ones this skill and its references use to refer to them.

**Where you left off:** one or two sentences with the last thing done, with its day (and its time only if a source genuinely gives it), and whatever was left halfway.
**Git:** only with a terminal in the repository; what goes in it is in `references/claude-code.md`.
**Pending:** at most five items, from most to least urgent. It comes from the project manager's next action, its dated tasks and whatever the notes (or the session log, if there is one) leave half-done and nothing later considers done.
**Heads-up:** sources that are behind or that clash, sources out of reach, leftovers, or a learning that applies to what is pending. At most three lines: one for all the sources that are behind (their names, what they say in a few words and their dates, together if they coincide), one for leftovers (branches and folders) and one for everything else. Do not explain each source separately, or split a line into a list. In the leftovers line, name the local branches and count the remote ones. For example: "Leftovers: `feat/x` locally and on the remote (PR #9 closed); 4 remote branches already merged; the folder `.claude/worktrees/y`, which git no longer tracks".

**Coming back after days away.** If the most recent activity on the project (or the umbrella), counting all sources, is more than three working days old according to the schedule in the instructions (or more than four calendar days if there is no schedule), the user is coming back after a gap and the summary changes in three ways:
- "Where you left off" gives the day of that activity and nothing else about the gap: no reproaches and no counting of lost days.
- "Pending" starts with what fell due during the gap (tasks and key dates already past), with its date, before everything else.
- Add at the end a **To get back in:** line with a single small, physical step to get started (for example, "open X's next action and do its first step"), taken from the project manager's next action for the most urgent project. If there is none, mark it as a suggestion and say where it comes from.

Before listing something as overdue, check whether a later source considers it done (step 3): a false overdue item after a gap is more discouraging than on a normal day.

**In an umbrella**, the same block for everything: "Where you left off" with the one or two projects with the most recent activity, counting all sources (the session log if there is one, the vault note and the project manager's edit date when it is not from a bulk edit), not just one of them. If more than two are tied (the same day and no time to order them), the two that have something pending or half-done go in, short-term ones first, and the rest go in a single sentence at the end ("There was also a session today on X"); and "Pending" with one item per project, headed by its name, starting with the short-term priority ones. Projects with no news and nothing pending do not appear.

No explaining which skills or sources you have used, except in "Heads-up" when two clash. If a source was not there or had nothing, do not mention it, unless its absence changes what can be known (for example, git not reachable and only the notes available).

**Test mode.** If the user says this is a test of the skill, add after the summary, separately and outside the line limit, the step 0 inventory: which capabilities you found, which sources you read and which you skipped, each with its reason in a few words. It is there to audit the routine; in a normal session it is not written.

## 5. Ask what to work on today

A single question. If a skill you have read brings its own, do not ask yours.

- **If the project has its own routine for planning the day** (for example, a phrase such as "what's on today" in the instructions, or an installed planning skill such as plan-admin and a schedule it can read), do not make a plan for the day or order blocks: ask what they are going to work on and offer, as the first option, launching that routine with its phrase. If the instructions set an order (a block that always goes first), respect it in the options.
- **If not**, offer as options the most likely pending items (two to four), with their next action if there is one, plus any the reference requires (in git, resolving an unfinished operation). If that operation blocks the main branch, the options that depend on that branch say so in their description ("after resolving the merge").
- If GitHub (C2) was left unread for lack of access and there is something "to be confirmed" that depends on it, add the option "Confirm on GitHub", saying in its description that it gives the session read access to the repository. If the user chooses it, add the repository with read-only access, do the C2 reads, correct the summary in two or three lines and ask again.

In total, at most four options, counting the project's routine and "Confirm on GitHub", because the question tool does not allow more. If they do not fit, remove the least urgent pending items first.

Use the question tool with options if there is one; the user can always write something else. If there is none, ask in text, with the same limit. If the user closes the question without answering, do not ask it again or hand over (step 6): wait for them to write.

## 6. Hand over

With the answer, if a skill-selection skill is installed (one that recommends which skills fit a task), launch it (with the Skill tool where there is one; if not, by reading its `SKILL.md`) and pass it the chosen task in one line, plus whatever is already known that affects it (for example, "there are uncommitted changes on main according to git", "the project manager's next action is behind the vault"). It will not repeat the reading. If none is installed, this skill ends here: start on the chosen task, using what you have already read.

If the user chooses to launch the project's planning routine, launch it (the planning skill if it is installed, passing it what you have already read so it does not repeat the reading; if not, the routine as the instructions describe it) and do not hand over until there is a concrete task. If they reply with something that needs no skills (a quick question), answer it and do not launch a skill-selection skill.

## Sessions without a user

If the session comes from a scheduled task or the user has said they will be back later, do steps 0 to 4, leave the summary at the start of your work and do not ask: carry on with the task the session brings and hand it over as in step 6. Do not add repositories to the session. With an unfinished git operation, do not start anything that touches that branch (see `references/claude-code.md`).

## If something fails

If a source fails, cannot be found or takes too long, skip it, carry on with the others and add a line in "Heads-up". A source that fails must not stop the user from seeing what could be read. If the user's computer does not respond, say it may be switched off or have the app closed, and carry on with the project manager, the chats and memory.

## Style

Reply in the user's language, be direct and do not repeat what the user has said. The summary is meant to be read in ten seconds: if it runs past ten lines, something should go. An unfinished git operation can take three lines in "Git" alone, and then the limit goes up to twelve. In an umbrella, twelve at most. A line is each item or sentence of about thirty words at most, not each screen line: an item longer than that is two. In "Heads-up", each line holds one kind only (sources behind, leftovers or everything else).
