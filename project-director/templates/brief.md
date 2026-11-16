<!--
One brief per piece of work, as a "## <ID> <title>" entry in the project's plan
or briefs file. Rules every work session follows go once at the top of that
file, not in each brief, for example:

## Rules for every work session
1. Read only these rules, your own brief and the sections it names.
2. Start with the first check in DIRECTING.md; no answer means BLOCKED.
3. Build only what the brief lists; ideas go in the report, one line each.
4. Done is the user's acceptance check, not yours.
5. Commit at the end of each piece, by path, so a usage stop loses nothing.
6. Your last message starts with the report the brief describes.

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

**Close-out.** Commit by path, push the branch, open the PR, note what was done by hand in the PR description, tick `B3` in the plan's checklist.

**Report.** The first lines of the last message: `DONE` or `BLOCKED`; the acceptance check line by line as pass or fail; what was done by hand; what the user still has to do; anything not verified.
