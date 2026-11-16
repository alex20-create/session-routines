# session-routines

`resume-project`, `skill-picker`, `project-director`, `plan-admin` and `wrap-up`: five routines for [Claude Code](https://claude.com/claude-code) that cover a session from open to close. They are independent skills — each works on its own — but they chain together on purpose, and this repo exists so a change to one does not drift out of sync with the others. `obsidian-project-sync`, the vault-sync step `wrap-up` can call, lives in its own repo, [obsidian-project-sync-skill](https://github.com/alex20-create/obsidian-project-sync-skill): it is useful on its own often enough that it did not belong bundled in here.

## How they chain

```
resume-project   -> opens a session, summarises where a project stands, asks what to work on today
skill-picker     -> takes that task, recommends which skills fit it and in what order
   ... the work happens ...
project-director -> when the work spans several sessions: opens each piece as its own session, checks it, keeps the status list
wrap-up          -> closes the session: memory, handoff, learnings, vault sync (obsidian-project-sync, installed separately)
```

`plan-admin` sits beside this chain rather than inside it: it plans the day and closes it out across several projects at once, and does not hand off to `skill-picker`.

## Which one to use

| | `resume-project` | `skill-picker` | `project-director` | `plan-admin` | `wrap-up` |
|---|---|---|---|---|---|
| When | Opening a session on a project with history | Before any piece of work starts | Work that spans several sessions, phases or parallel lanes | Start of day, end of day, weekly review | Closing the chat or session |
| Reads | Project manager, session log, git, vault, handoffs, chats, memory | The installed skill list | The project's `DIRECTING.md`, `STATUS.md`, briefs and log, and git | The project manager and project instructions | Session state across whatever is installed |
| Produces | A summary of where things stand, and a question: what to work on | A short list of skills and a model tier, waiting for confirmation | One session per piece, checked and archived; a status list; cuts proposed with numbers | Today's plan, a day close, or a weekly review | Updated memory, handoff, learnings and a vault sync |
| Hands off to | `skill-picker`, with the chosen task | Nothing — waits for confirmation, then the work begins | A new director, with one opening line, when its own context fills | Nothing | `obsidian-project-sync`, among other steps (installed separately) |

`project-director` needs the Claude desktop app's session tools, so it is for Claude Code only.

## What is in the box

| Path | What it is |
|---|---|
| `resume-project/` | The skill and its evals |
| `resume-project-scripts/` | A script to build the evals' fixtures; not part of the installed skill |
| `skill-picker/` | The skill |
| `project-director/` | The skill, its templates for a directed project, and its evals |
| `plan-admin/` | The skill |
| `wrap-up/` | The skill |
| `wrap-up-hook/` | The `UserPromptSubmit` hook that nudges Claude to run `wrap-up` when the user is closing the chat; not part of the installed skill |

Each skill folder holds exactly what gets installed and packaged: `SKILL.md` plus whatever it references. The two `-scripts`/`-hook` folders are tooling for one skill each, kept out of its folder so building its `.skill` package never picks them up; `wrap-up-hook/settings.example.json` shows how to wire the hook into `~/.claude/settings.json`.

## License

MIT, see [LICENSE](LICENSE).
