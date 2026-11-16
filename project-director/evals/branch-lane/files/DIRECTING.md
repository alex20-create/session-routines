# Directing

## Where things are

- Plan and briefs: `docs/plans/checkout.md`
- Status list: `STATUS.md`
- Log: git history and PR descriptions

## Exclusive resources

- e2e port: the end-to-end suite runs on one fixed port; two runs at once test the wrong build.
- docs PR: only one pull request per batch touches the README.

## Starting a session

- Working folder: the repository root.

## Models

- Each brief names its model.

## Clock

- No deadline: order only.

## How work lands

- One branch per session from `main`. Approving a brief lets its session push its branch and open its PR. Merging is the user's word.
- `STATUS.md` is committed to `main` by path.

## Opening line

`You are the director for the checkout work in this folder. Read DIRECTING.md and STATUS.md and take over.`
