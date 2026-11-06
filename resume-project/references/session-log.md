# Session log (source B)

**This reference applies only if a hook writes per-project session logs in the format below.** If the setup has no such log, skip this file: `SKILL.md` works without it. In the setup this skill was first written for, the hook comes with a vault-sync skill, `obsidian-project-sync`; any hook that writes the same files works the same way.

The log tells you what really happened in each project and when, as recorded by the hook each time a session closed. It is a quick snapshot of git written to disk, so it is useful above all where there is no terminal in the repository.

## Contents

- What the hook writes
- Where the log lives
- Matching by path
- Reading rules
- Where it fits among the other sources

## What the hook writes

To build such a hook, make it write this. Logs written by older versions of `obsidian-project-sync` use Spanish keys; read them as aliases of the English ones (`proyecto` project, `ruta` path, `ultimo_commit` last_commit, `ultima_sesion` last_session, `carpetas` folders, `sesiones` sessions, `fecha` date, `hora` time, `rama` branch, `archivos` files, `sin_commitear` uncommitted, `carpeta` folder), and the `_juntados/` subfolder as `_merged/`. A log is rewritten with English keys the next time the hook records a session for it.

- **When.** The hook runs when a Claude Code session closes, in whatever folder it ran in (the repository or one of its worktrees). A session that is still open, or that was cut off without closing, writes nothing.
- **One file per project**, named after the project, at the root of the logs folder. A session in a worktree updates its project's file; older versions of the hook wrote a separate file per worktree, and a merge step (`log-merge`) later moves those into the project's file and keeps the originals in a `_merged/` subfolder as history.
- **Top level of each file:**
  - `project`: the project name.
  - `path`: the project folder's path.
  - `last_commit`: the `HEAD` of the folder that closed the last session, on whatever branch it was on.
  - `last_session`: the date of the last session.
  - `folders`: one entry per folder, keyed by the folder's path (each worktree and, with the current hook, the repository's own folder too), each with `branch`, `last_commit` and `last_session` for that folder.
  - `sessions`: one entry per closed session.
- **Each session:**
  - `date` and `time` (local, `HH:MM`). Older versions of the hook did not write `time`.
  - `branch`: the branch the folder was on when the session closed.
  - `commits`: the new commits in that folder since its previous recorded session, each with at least its subject line, because the rules below read merge subjects such as `Merge pull request #N from <owner>/<branch>`.
  - `files`: the files changed by those commits, not the ones left uncommitted.
  - `uncommitted`: how many lines `git status` showed on closing (modified and untracked files), as a number.
  - `worktree` and `folder`: only for sessions run in a worktree.

An illustrative file (the exact shape of each commit entry and of the dates is up to the hook, as long as the fields above are there):

```json
{
  "project": "my-app",
  "path": "/home/user/code/my-app",
  "last_commit": "a1b2c3d feat: home screen",
  "last_session": "2026-11-03",
  "folders": {
    "/home/user/code/my-app": { "branch": "main", "last_commit": "a1b2c3d feat: home screen", "last_session": "2026-11-03" },
    "/home/user/code/my-app/.claude/worktrees/feat-x": { "branch": "feat/x", "last_commit": "d4e5f6a feat: x", "last_session": "2026-11-02" }
  },
  "sessions": [
    { "date": "2026-11-02", "time": "17:40", "branch": "feat/x", "commits": ["d4e5f6a feat: x"], "files": ["x.txt"], "uncommitted": 0, "worktree": "feat-x", "folder": "/home/user/code/my-app/.claude/worktrees/feat-x" },
    { "date": "2026-11-03", "time": "11:05", "branch": "main", "commits": ["a1b2c3d feat: home screen"], "files": ["home.txt"], "uncommitted": 2 }
  ]
}
```

What each field means when reading it:

- The top-level `last_commit` is the `HEAD` of the folder that closed the last session, on whatever branch it was on, not the tip of the main branch nor the newest commit in the project. The one in each `folders` entry is that folder's `HEAD` when its last session closed.
- `commits` are the new commits in that folder since its previous recorded session.
- `files` are the files changed by those commits, not the ones left uncommitted. If a session has `files` but no commit, it is the difference between two branches caused by a branch switch: do not read it as that session's work.
- `uncommitted` is how many lines `git status` showed on closing. It does not say which ones.
- `date` and `time` are when the session closed, not when the work was done: a session opened one day and closed the next carries, under the closing date, commits from the day before. To date the work, with a terminal use the commit dates (`git log -1 --format=%ad --date=iso-local <commit>`) or the reflog.

## Where the log lives

The log sits inside the vault. The log folder is given by the `logs` key of `.claude-vault.json` (`registros` in older files), at the root of the vault; the same file's `projects` key (`proyectos` in older files) gives the folder of the project notes (D in `SKILL.md`). If that file does not exist, look for a `Claude Sync` folder inside the vault's top-level folders (for example `4 Toolbox/Claude Sync`).

## Matching by path

This is the first key in "How the same project is matched across sources" (step 1 of `SKILL.md`): the log's `path` against the `path:` field in the frontmatter of the vault note (D). Compare them case-insensitively, treating `\` and `/` as the same.

In an umbrella, **a log that matches no project in the project manager and no note in the vault does not appear in the summary**: these are usually skills, templates, third-party tools or the root folder. Bring it up only if the user names it.

## Reading rules

- **Old hook.** If no session in any log has `time`, not even today's, the hook installed on the computer predates the current version. Say so once in "Heads-up", speaking only about what was recorded, because the hook may have been updated after the last session: "up to the last recorded session (<day>), the log did not store the time; if the hook has still not been updated, it is worth bringing it up to date". Carry on with the rules for sessions without `time`.
- **Only closed sessions are there.** The hook writes when the session closes: one that is still open, or that was cut off without closing, is not there. That is why the log can lag behind the vault note.
- **Read only the files at the root of the folder**, all of them, not just the one named after the project. The `_merged/` subfolder holds the loose worktree logs that the hook has already merged into their project's file: it is history, and reading it duplicates sessions. Do not go into it.
- **Old format.** If there is a file at the root whose `path` contains `.claude\worktrees\` (or `/.claude/worktrees/`), it is a worktree that has not been merged in yet: its project is the folder before `.claude`. Merge it yourself with that project's log.
- **Folders that are gone.** A `folders` entry, or a session with `folder`, whose folder no longer exists or which, with a terminal, does not appear in `git worktree list`, is a removed worktree. Its `uncommitted` no longer means anything, because whatever was left unsaved went with the folder; its branch does count for "Unmerged branches" below. If the folder is still on disk but git no longer knows about it, it is a leftover: say so in "Heads-up" in one line.
- **Session order.** Sort by `date` and `time`. Sessions without `time` predate the hook storing it: within the same day, their position in the array is only reliable if the log has never been merged (there is no `_merged/`), because merging puts the repository's sessions first and then each worktree's, whatever the real order. If it has been merged, treat them as same-day sessions with no order and, if needed, order them by their commits (the session that brings in a branch's merge comes after the one that brings its commits).
- **The file's modification date is not the session time.** Merging logs (`log-merge`) rewrites all of them at once, and then they all show the same time. That date only says that the last session is not later than it. Between projects with sessions on the same day and no `time`, do not decide from the file which comes first: use the date of their vault note or of their page in the project manager, and if there is none, put them together in "Where you left off" with no order. Do not give a time that comes only from the file date.
- **Check the log against the note.** If the project note (D) names commits, PRs or merges that the log does not have (not in `last_commit`, nor in `folders`, nor in its sessions' commits), the log is behind: there was work it did not record. Say so in "Heads-up" with both dates and take the note for the state.
- **And the other way round.** If the log has commits from sessions later than the note's `updated:` that the note does not name, the note is behind. Say so in "Heads-up", on the same line as the other mismatches, with both dates and that it can be brought up to date with the skill that maintains the note and the log (for example `obsidian-project-sync`). For the state, take the log.
- **Sessions with no activity.** A session with no commits, on the same branch and with the same `uncommitted` as the previous one in its folder, does not count as activity: it is usually a session that only read, like this routine. Do not use it for "Where you left off" nor as the last session of its folder. The first of such a series, the one that changed `uncommitted`, does count. No activity in git does not mean no work: if such a session is the project's most recent, look at it in F2 and I of `SKILL.md` before discarding it, because it may have left work outside the repository.
- **What was left uncommitted.** Look at the last session of each folder of the project: the repository's and that of each worktree whose branch is not merged (see the next rule). If it closed with `uncommitted` greater than 0, it goes in "Pending" under its project's item: "when the <day> session closed, `git status` showed N lines on <branch>, to be confirmed". Do not say which files they are, because the log does not know. If that folder is on the main branch and there is an unmerged branch of the same project, say so alongside: they may be changes for that branch made on the main branch. If that session is on the main branch, has no commits and its `uncommitted` is much larger than that of the earlier sessions (dozens of lines), the most likely cause is an unfinished git operation, such as a `git pull` that was left unfinished, and not unsaved work: say it that way, to be confirmed, and put it first in "Pending".
- **Unmerged branches.** Check every branch other than the main one that has its own commits in any session from the last fourteen days, in any folder, even if the project's most recent session is on the main branch: a folder that goes back to the main branch does not merge the branch it leaves. For each one, check in order:
  1. If any later session of the same project, in any folder, has a commit `Merge pull request #N from <owner>/<branch>` or `Merge branch '<branch>'` with that branch, or if its commits end in `(#N)` (they are already the PR's squash on the main branch): it is merged.
  2. If the vault note considers that branch merged, or a PR that describes the same changes as its commits ("merged as", "merged into", the same topic, or the same wording in the note's own language). Merges are often done on GitHub and leave no trace in the log. If it matches, list it as "probably merged in PR #N" only if it matters for what is pending, and otherwise leave it out.
  3. If the note considers it open or unmerged ("open", "not merged", or the same wording in the note's own language): it goes in "Pending" as "PR #N open according to the <day> note, to be confirmed".

  If none of the three says anything, note it as "unmerged branch according to the log", to be confirmed. Branches whose commits already appear in a later session on the main branch are history: leave them out. With a terminal, also leave out those that are no longer either local or on the remote and whose changes are on the main branch (`git branch -a --contains <last commit of the branch>` shows the main branch, or its PR shows as merged).
- **What the log does not know.** It does not say whether a branch was pushed to the remote, whether it has a pull request or whether anything was deployed. Without a terminal or GitHub (C2 in `SKILL.md`), those points go as "to be confirmed".

## Where it fits among the other sources

- **Reading order.** The log is read first, before git and the remote (C), GitHub (C2) and the project manager (A), because it tells you how much each note is worth.
- **Without a terminal**, the log stands in for the quick git snapshot: say so in the summary ("according to the log when the session closed"), because things may have changed since. GitHub (C2) can confirm what the log does not know.
- **With a terminal and a log at the same time**, git wins.
