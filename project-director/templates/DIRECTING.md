# Directing

<!--
The standing setup for directing this project. It changes rarely; STATUS.md
holds what changes every hour. Replace the example lines with this project's
own and delete this comment.
-->

## Where things are

- Plan and briefs: `docs/plans/checkout.md`, one `## <ID>` entry per brief
- Status list: `STATUS.md`, written only by the director
- Log: git history and the PR descriptions
- Session reports: the PR descriptions; hand-over notes of sessions that end `BLOCKED`: `docs/notes/<ID>.md`
- Standing roles: `docs/roles/ux.md`

## Exclusive resources

One session at a time each. Handing over: the holder saves, leaves the tool usable, commits its own files, writes a note, and tells the director; only then does the next holder start.

- e2e port: the end-to-end suite runs on a fixed port; two runs at once test the wrong build. Free means no test server is listening on it.
- docs PR: only one pull request per batch touches `CLAUDE.md` and the README.

## Starting a session

- Working folder: the repository root, `<absolute path>`, where the project's tool configuration lives. A session started elsewhere may lack the project's tools and not say so.
- First step of every work session: `git status` in `<absolute path>` shows its own branch and a clean tree, and `npm run e2e -- --list` lists the suite; anything else means stop and report `BLOCKED`.
<!-- Where pieces share one checkout, word the check as "the main branch, and
nothing changed under your own brief's paths": a clean tree fails as soon as
two pieces run at once. A project with no tools to check keeps the git
line alone. -->
- Sessions that run in parallel each get their own worktree, cut from `main`; the director's own checkout stays on `main`.

## Models

- Each brief names its model. A bug that survived two fixes goes one tier up.
- Tiers to model ids: light `<model id>`, middle `<model id>`, strong `<model id>`.

## Clock

- No deadline: order only.
<!-- With a deadline, list the decision points instead, e.g.
- Fri 18:00: look at what fits; propose cuts if the list does not
- Sun 23:00: content freeze
- Mon 01:00: final build
-->

## How work lands

- One branch per session, cut from `main`, each in its own worktree; approving a brief lets its session push its branch and open its PR. Merging is the user's word every time.
- `STATUS.md` is committed straight to `main` by path, from the director's checkout. Pushing `main`: only when the user says (or write "after every update" here if the user chose that at setup).

## Opening line

For a new director: `You are the director for <project> in <folder>. Read DIRECTING.md and STATUS.md and take over.`
