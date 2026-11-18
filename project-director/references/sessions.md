# Sessions

Read this before opening, naming, messaging or archiving a session.

## Titles

The first words say what the session is, so the sidebar reads at a glance:

- a work session: `<ID> · <what it does>`, for example `B3 · order history page`;
- a standing role: the role's name, for example `UX lead`;
- the director: `Director · <project>`, so two directed projects do not show two sessions with one name.

Write titles in the user's language, and quote them as they are, inside «...», in `STATUS.md`. Never start them with the project's name: the project is the sidebar group. While a session holds an exclusive resource, its title ends `· <resource>` (`B3 · order history page · e2e port`); rename it when the turn passes.

## Groups

One sidebar group per project, named after the project in the user's language. Check the existing groups first and reuse one with that name, or one the user clearly made for this project; create one only if none does. `start_session` takes no group. File your own session in the group once: the sessions you start move with it, and moving one of them alone is refused.

## Models

- Open each session on the model its brief names, or the one `DIRECTING.md`'s policy gives. A brief that names a tier (light, middle, strong) needs a model id: `DIRECTING.md`'s «Models» maps each tier to one; if it does not, ask the user once and write the answer there.
- A session can be started only on a model at or below the director's own. Run the director on a model at least as high as any session it must start. When it cannot start one, or you cannot tell whether your model ranks above the one asked for, (a design session on a higher model), give the user the exact opening line and let them start it.
- `list_sessions` does not show a session's model; `get_session` does. Confirm it there after opening, before telling the user a model cannot be verified.

## Starting a session

- **The user's word opens sessions.** A session can only be started in a turn the user's own message opened. So every report ends with the next opening ready (which pieces, on which model, holding which resource), and the user's single yes starts them: in the turn that yes opens, start each with `start_session` as something the user asked for (`initiation: "user_asked"`). The user may approve several at once; start them all in that turn. Archiving works the same way: the app archives a session only after the user agreed to archive that session, so the report names the sessions ready to archive and the same yes covers them. Wake-ups, when a session finishes or writes to you, are for checking, reconciling and reporting, never for starting or archiving.
- **No session tools at all** (a terminal without the desktop app, or the tools not loaded): say so at once, and do not fall back to building in your own context or in subagents, which is what this skill exists to avoid. Give the user each opening line to start the session by hand, and keep directing from the files.
- Start the session in the folder where the project's tools are configured, as `DIRECTING.md` says. A session started one folder up may have none of the project's tools and not say so. Your own working folder can drift (a shell command run elsewhere resets it): pass `cwd` whenever it is not the project's. Put the first tool check from `DIRECTING.md` at the start of every prompt that needs it, written with the project's absolute path.
- The prompt points at the brief and adds only three things: the first tool check, the version of the brief the user chose (after a cut), and the turn's way back. `Build brief <ID> from <briefs file> in <folder>. Read the shared rules, your own brief, and <named sections>. Nothing else.` The `background` a fresh session needs holds the project in one line, the resource it holds, and where `STATUS.md` is; not the brief again.
- Open the next session early, read-only, when it will need a resource that is still taken (see `resources-and-turns.md`).

## Talking to sessions

- The user may talk to any session directly. A session that takes a request from the user tells the director what changed, so `STATUS.md` stays true.
- A message sent to a session in the middle of a turn waits until that turn ends, which can be a long time. When it cannot wait, stop the session (`stop_session`): the queued message then runs next, and the session keeps its context.
- Never poll a session or the board on a timer. The app wakes the director when a turn the director started in a session ends. A turn the user drives there does not wake it: that report waits for the user's next message to the director, so ask the user for one line when such a session says `DONE`.
- Read a session's report with `list_events` at a limit of 10 or more, never by searching the disk: a small limit returns only the closing line, and a wake-up quotes only the first 400 characters.
- A message from a session you did not start is the user's request relayed: plan it into `STATUS.md` and the right brief, answer the sender, tell the user in the next report, and start nothing on it.
- Under a deadline, expect a stream of small requests from the user in the last hour. Price each in minutes, with a way back, before it is built.

## Branches and pull requests

Where each session works on its own branch, approving a brief authorises its session to push that branch and open its pull request. Merging is always the user's word, every time. The director checks the pull request exists; it never merges.

## Archiving

- Archive only on the user's yes to that session (see «Starting a session»).
- At take-over, sessions left by an earlier director, or still holding a resource, stay on the board until the user says what happens to them.
- Before archiving, move every open item of the session's report into `STATUS.md` (see `project-files.md`).
- Archiving a session also archives the idle sessions it started. Detach those first if they should live on.
- Never archive a session that reported `BLOCKED` while it waits on the user or may still be resumed. Once a fresh session takes the piece over, archive the blocked one.
- Archive in a response of its own, and open new sessions in the response after it: when an archive is refused, a `start_session` sent beside it is refused too.

## App limits

Observed in the Claude desktop app in November 2026; recheck when something behaves differently.

- `start_session` accepts a model only at or below the starting session's own; a higher one is ignored.
- A turn started by another session's message or by an automated event, including the wake-up when a session the director started ends its turn, cannot start a session. It can only propose a card, and a card cannot carry a working folder. The app states one exception: a wake-up that comes right after the user's own turn may start a step the user asked to have in its own session.
- A message to a session in mid-turn is queued until that turn ends; `stop_session` makes it run next.
- Archiving a session archives the idle sessions it started.
- An `archive_session` refused because something changed its input (a hook, a permission mode) passes when repeated with the input the refusal quotes.
- A session gets the project's tools only if started in the folder where they are configured. A session started before a tool's server is up, or whose server restarts, loses that tool until the user reconnects it (`/mcp` in that session).
- The app wakes a session when a turn it started in another session ends; nothing needs polling. It does not wake it for a turn the user drove there, and it holds wake-ups after many in a row with no message from the user, or after a turn of the director's that was stopped or failed. Those reports arrive with the user's next message.
- `get_usage` reports the account's 5-hour and weekly limits and any session's context fill. The 5-hour limit stops every session at once.
- Sessions can be renamed (`set_session_title`) and filed into sidebar groups; a title the user set may ask the user first. A session moves with the session that started it.
- `archive_session` is to be called only after the user explicitly agreed to archive that session, and the app asks for approval in most permission modes.

## Tool names and parameters

Observed in November 2026. The tools are often deferred: load them with the tool-search tool first.

| What | Tool | Notes |
|---|---|---|
| Start | `mcp__ccd_session__start_session` | `initiation: "user_asked"`; `context: "fresh"` needs `background` (80 characters at least); `use_worktree: true` for its own worktree, `false` to share this checkout; `cwd` whenever your own folder is not the project's; `model` is a model id at or below yours; `title`; `wake_when_done` |
| List | `mcp__ccd_session_mgmt__list_sessions` | `linked: true` for the sessions you started |
| One session | `mcp__ccd_session_mgmt__get_session` | Shows its model |
| Read a report | `mcp__ccd_session_mgmt__list_events` | `limit` of 10 or more |
| Message | `SendMessage` with `to` set to the session's `local_...` id | `mcp__ccd_session_mgmt__send_message` is the older form |
| Stop | `mcp__ccd_session_mgmt__stop_session` | A queued message then runs next |
| Rename | `mcp__ccd_session_mgmt__set_session_title` | |
| Detach | `mcp__ccd_session_mgmt__detach_session` | Before archiving a parent whose idle side sessions should live on |
| Archive | `mcp__ccd_session_mgmt__archive_session` | Only after the user agreed to that session; in a response of its own |
| Usage | `mcp__ccd_session_mgmt__get_usage` | `session_id: "self"` for your own context |
| Groups | `mcp__ccd_sidebar__list_groups`, `mcp__ccd_sidebar__create_group`, `mcp__ccd_sidebar__move_sessions` | File your own session; the ones you start follow |
