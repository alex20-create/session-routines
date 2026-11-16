# Sessions

Read this before opening, naming, messaging or archiving a session.

## Titles

The first words say what the session is, so the sidebar reads at a glance:

- a work session: `<ID> · <what it does>`, for example `B3 · order history page`;
- a standing role: the role's name, for example `UX lead`;
- the director: `Director`.

Write titles in the user's language. Never start them with the project's name: the project is the sidebar group. While a session holds an exclusive resource, its title ends `· <resource>` (`B3 · order history page · e2e port`); rename it when the turn passes.

## Groups

One sidebar group per project. Check the existing groups first and reuse one whose name matches the project; create one only if none does. Moving a session other than your own into a group may ask the user first; say so the first time.

## Models

- Open each session on the model its brief names, or the one `DIRECTING.md`'s policy gives.
- A session can be started only on a model at or below the director's own. Run the director on a model at least as high as any session it must start. When it cannot start one (a design session on a higher model), give the user the exact opening line and let them start it.

## Starting a session

- **The user's word opens sessions.** A session can only be started in a turn the user's own message opened. So every report ends with the next opening ready (which pieces, on which model, holding which resource), and the user's single yes starts them: in the turn that yes opens, start each with `start_session` as something the user asked for (`initiation: "user_asked"`), with the working folder set. The user may approve several at once; start them all in that turn. Wake-ups, when a session finishes or writes to you, are for checking, reconciling, archiving and reporting, never for starting.
- **No session tools at all** (a terminal without the desktop app, or the tools not loaded): say so at once, and do not fall back to building in your own context or in subagents, which is what this skill exists to avoid. Give the user each opening line to start the session by hand, and keep directing from the files.
- Start the session in the folder where the project's tools are configured, as `DIRECTING.md` says. A session started one folder up may have none of the project's tools and not say so. Put the first tool check from `DIRECTING.md` at the start of every prompt that needs it.
- The prompt points at the brief and nothing more: `Build brief <ID> from <briefs file> in <folder>. Read the shared rules, your own brief, and <named sections>. Nothing else.`
- Open the next session early, read-only, when it will need a resource that is still taken (see `resources-and-turns.md`).

## Talking to sessions

- The user may talk to any session directly. A session that takes a request from the user tells the director what changed, so `STATUS.md` stays true.
- A message sent to a session in the middle of a turn waits until that turn ends, which can be a long time. When it cannot wait, stop the session (`stop_session`): the queued message then runs next, and the session keeps its context.
- Never poll a session or the board on a timer. The app wakes the director when a session it started ends a turn.
- Under a deadline, expect a stream of small requests from the user in the last hour. Price each in minutes, with a way back, before it is built.

## Branches and pull requests

Where each session works on its own branch, approving a brief authorises its session to push that branch and open its pull request. Merging is always the user's word, every time. The director checks the pull request exists; it never merges.

## Archiving

- Before archiving, move every open item of the session's report into `STATUS.md` (see `project-files.md`).
- Archiving a session also archives the idle sessions it started. Detach those first if they should live on.
- Never archive a session that reported `BLOCKED` while it waits on the user. Once a fresh session takes the piece over, archive the blocked one.

## App limits

Observed in the Claude desktop app in November 2026; recheck when something behaves differently.

- `start_session` accepts a model only at or below the starting session's own; a higher one is ignored.
- A turn started by another session's message or by an automated event, including the wake-up when a session the director started ends its turn, cannot start a session. It can only propose a card, and a card cannot carry a working folder. The app states one exception: a wake-up that comes right after the user's own turn may start a step the user asked to have in its own session.
- A message to a session in mid-turn is queued until that turn ends; `stop_session` makes it run next.
- Archiving a session archives the idle sessions it started.
- A session gets the project's tools only if started in the folder where they are configured. A session started before a tool's server is up, or whose server restarts, loses that tool until the user reconnects it (`/mcp` in that session).
- The app wakes a session when a session it started ends a turn; nothing needs polling.
- `get_usage` reports the account's 5-hour and weekly limits and any session's context fill. The 5-hour limit stops every session at once.
- Sessions can be renamed (`set_session_title`) and filed into sidebar groups; a title the user set, or moving another session, may ask the user first.
