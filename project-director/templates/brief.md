<!--
One brief per piece of work, as a "## <ID> <title>" entry in the project's plan
or briefs file. Rules every work session follows go once at the top of that
file, not in each brief, for example:

## Rules for every work session
1. Read only these rules, your own brief and the sections it names.
2. Start with the first check in DIRECTING.md; no answer means BLOCKED.
3. Build only what the brief lists; ideas go in the report, one line each.
4. Done is the user's acceptance check, not yours. When the user answers it,
   or the fit question, in your session, record the answer in your report, in
   their words, before you say DONE: otherwise the director asks them again.
5. Commit at the end of each piece, by path, so a usage stop loses nothing.
6. Your last message starts with the report the brief describes. A turn that
   ends before the report starts with STILL WORKING and what you wait for.
7. A scope or product choice is the user's: ask the user, never the director.
8. If you end BLOCKED, commit your hand-over note first: what was decided and
   how, what you wait for, what is left.

A research or document brief writes its acceptance lines so they can be
counted, plus one line about fit that the user judges from a short summary.

Delete this comment.
-->

## B3 Order history page

**Model.** The middle tier.

**Resources.** e2e port.

**Read.** The shared rules at the top of this file, this brief, and `docs/specs/checkout.md` section «Orders». Nothing else.

**Build.**
- A page at `/orders` listing the signed-in user's orders, newest first, 20 per page.
- Each row: date, total, state. A row opens the order.
- An empty state with one line and a link back to the shop.

**Acceptance check (the user's).**
1. With three orders, all three show, newest first.
2. With none, the empty state shows and its link works.
3. The e2e suite passes on the port.

**Close-out.** Commit by path, push the branch, open the PR, note what was done by hand in the PR description, tick `B3` in the plan's checklist. The report also goes in the PR description; a hand-over note, if `BLOCKED`, in `docs/notes/B3.md`.

**Report.** The first lines of the last message: `DONE` or `BLOCKED`; the acceptance check line by line as pass or fail; what was done by hand; what the user still has to do; anything not verified.
