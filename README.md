# session-routines

`resume-project`, `skill-picker`, `plan-admin`, `wrap-up` and `obsidian-project-sync`: five routines for [Claude Code](https://claude.com/claude-code) that cover a session from open to close. They are independent skills — each works on its own — but they chain together on purpose, and this repo exists so a change to one does not drift out of sync with the others.

## How they chain

```
resume-project   -> opens a session, summarises where a project stands, asks what to work on today
skill-picker     -> takes that task, recommends which skills fit it and in what order
   ... the work happens ...
wrap-up          -> closes the session: memory, handoff, learnings, vault sync
obsidian-project-sync -> the vault-sync step wrap-up calls, also usable on its own
```

`plan-admin` sits beside this chain rather than inside it: it plans the day and closes it out across several projects at once, and does not hand off to `skill-picker`.

## Which one to use

| | `resume-project` | `skill-picker` | `plan-admin` | `wrap-up` | `obsidian-project-sync` |
|---|---|---|---|---|---|
| When | Opening a session on a project with history | Before any piece of work starts | Start of day, end of day, weekly review | Closing the chat or session | Whenever a vault note needs to catch up with the work |
| Reads | Project manager, session log, git, vault, handoffs, chats, memory | The installed skill list | The project manager and project instructions | Session state across whatever is installed | The vault's own structure and existing notes |
| Produces | A summary of where things stand, and a question: what to work on | A short list of skills and a model tier, waiting for confirmation | Today's plan, a day close, or a weekly review | Updated memory, handoff, learnings and a vault sync | Updated project notes, canvases, or the install of its own sync hook |
| Hands off to | `skill-picker`, with the chosen task | Nothing — waits for confirmation, then the work begins | Nothing | `obsidian-project-sync`, among other steps | Nothing |

## What is in the box

| Path | What it is |
|---|---|
| `resume-project/` | The skill, its evals and a script to build eval fixtures |
| `skill-picker/` | The skill |
| `plan-admin/` | The skill |
| `wrap-up/` | The skill plus the `UserPromptSubmit` hook that nudges Claude to run it when the user is closing the chat |
| `obsidian-project-sync/` | The skill, its tests, and the `SessionEnd` hook that logs each session to the vault |

Each skill folder has its own `SKILL.md`; the hook folders carry a `settings.example.json` showing how to wire that hook into `~/.claude/settings.json`.

## License

MIT, see [LICENSE](LICENSE).
