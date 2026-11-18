# Resources and turns

Read this when two pieces of work could need the same thing, when handing a resource from one session to the next, or before opening sessions in parallel.

## Exclusive resources

An exclusive resource is anything only one session can use at a time without breaking the other's work:

- a running tool that sessions drive (an editor, a game engine, a design app, a database console);
- a fixed port or test server (two end-to-end runs on one port test the wrong build);
- a file or artifact only one session may write (a published page, a shared config, the one pull request allowed to touch the project's instructions);
- a step that needs a tool closed (packaging, a migration) while others need it open.

`DIRECTING.md` lists them with how each is handed over. Each brief says which it needs. One that turns up after setup (a signed-in browser, a second port) is added to `DIRECTING.md` and shown to the user in the same report.

## The board

The «Resources» section of `STATUS.md` is the board: each resource, who holds it since when, who is next. A piece readied for the user's yes shows as `free · readied B3 · next B4`; once it starts, `held by «B3 · ...» · since ... · next B4`. The director is the only one who writes it, and every report to the user starts with it.

While a session holds a resource, its title ends with `· <resource>`; the director renames it when the turn passes (see `sessions.md`).

## Running in parallel

Pieces that need no exclusive resource, or different ones, run at the same time. Where each session works on its own branch, each parallel session gets its own worktree (`start_session` with a worktree); two sessions on two branches in one folder move each other's checked-out branch and commit to the wrong one. A worktree carries the project's tool configuration only if that file is tracked in git; if it is not, sessions that need those tools run one at a time from the main checkout. Two pieces that need the same one never do: ready only the first, and put the second on the board as next.

A session that will need a resource soon can be opened early in read-only mode, with the prompt ending "make no call to <resource> until I write". It reads its brief and the files while the current holder works, and starts the moment the turn passes.

## Handing a resource over

1. The leaving session saves its work and leaves the tool in a state the next can use (nothing still running, nothing that blocks saving).
2. It commits its own files, by path.
3. It writes a short note where the project keeps them (the log, the PR description, a notes file).
4. It tells the director it has let go.
5. Only then does the director update the board and write to the next holder.

**When a holder's report is sent back**, the resource stays with it: the piece is not done, and it will need the resource again to finish. The next piece waits as next on the board. If the session cannot settle it on that one send-back, it saves, commits what it has, lets go, and the piece moves to «Blocked» with a fix brief for a fresh session; only then does the resource pass on.

Every turn gets a way back, written before it starts: "if this does not pass the user's check (or, under a deadline, is not right by <decision point>), revert to <commit> and go on with <next piece>".

## Things that break turns

- Telling the user to close a tool before asking whether more work on it is wanted. A step that waits for the tool to close may fire when the user closes it for another reason.
- A background step that starts on its own when a condition holds ("package when the editor closes"). Start such steps on the user's word instead.
- Two sessions each believing the other let go. The board is the only record; if it is unclear, ask the user who is in the tool right now.
