# Stale sessions and repeat closes

Read when the session's last real work was on an earlier day than today,
or when the chat already holds an earlier close. A close is usually asked
for at the end of the work, but a chat can sit open for days and be closed
later, after other sessions have worked on the same files, notes and
skills.

## Is the session stale?

The session is **stale** when anything it touched changed after its last
real work: compare the date of that work (the conversation's timestamps or
dated notes) with the modification times of the files and store entries it
touched, a later commit, a store entry dated later, or a skill it used
that the listing now shows renamed or no longer shows. One such change is
enough. The age alone is a reason to look, not a verdict: a week-old chat
nobody built on is not stale, and closes at the level its own work calls
for.

A stale session closes at the full level, and the first line of the plan
says so with the gap ("last active on 4 Nov; files it touched changed
since").

## What changes in a stale session

The disk and the stores are newer than the conversation, so they win:

- Before planning any write, read the current version of each file and
  store entry the step would touch, and plan against what is there now,
  not against what the conversation remembers.
- A decision the session took that a later session already recorded is
  done: point at it, do not write it again. One a later session changed or
  reversed is not this close's to restore: name it as superseded and drop
  it. When the later record covers only part of the decision, or it is
  unclear how much it covers, drop only the part it clearly covers and
  name the rest as possibly superseded; which way it goes rides the single
  question.
- Paths, names and skills the session used may have moved or been renamed.
  Resolve each again before using it. A new form counts only when
  something written since states it (memory, a note, a commit, a skill's
  own description saying what it was called before); use that form and say
  so. When nothing states it, name the old one as no longer resolving
  instead of guessing, and do not write it into a store as if current.
- What is left to propose is what the session decided and nothing since
  has recorded, changed or contradicted. That can be very little; a stale
  close that writes one line, or nothing, is a correct close.

## An earlier close in the same chat

The same chat may already hold an earlier close, run before the user kept
working. Then this close builds on that one instead of starting over: take
its plan and mark each step done (its report says so and the disk agrees),
superseded, or still pending, and check only what happened after it. The
level comes from the work done since that close, raised by whatever it
left pending. A plan the earlier close proposed that the user never
answered was not approved: carry its pending steps into this plan, checked
again against the disk and the rules above, instead of running them or
dropping them silently, and say in the first line that an earlier close
exists.
