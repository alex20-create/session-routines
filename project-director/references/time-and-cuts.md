# Time and cuts

Read this when the user asks what something costs, when the work may not fit, or when a decision point comes up.

## No hour targets

Nobody can estimate well what each piece of a complex project costs, least of all the user's own part: acceptance checks, manual steps in tools, fixes after a check, closing sessions. So the director never gives a piece an hour to finish by, and never says how late something is by the clock.

Instead:

- **An ordered list.** «Next» in `STATUS.md`, in the user's order of priority.
- **A few decision points**, only when there is a deadline, written in `DIRECTING.md`: "at 16:00 we look at what fits", the content freeze, the final build, the submission. At each one the director puts the list against the time left and, if it does not fit, proposes cuts.
- Without a deadline there is no clock, only order and what is left.

## Ranges, not numbers

When the user asks what something costs, give a range split in two:

- **the session's part**, from how long similar pieces took (the «Done» times);
- **the user's part**, the acceptance check and anything by hand, from what the user has said before. Say plainly when it is unknown, which it usually is.

Never revise a schedule upward because a session built fast. The building is rarely the slow part; the check is.

## Measuring

Every line in «Done» records when the piece started and ended. When the user says how long a check took, add it. Ask now and then, briefly; do not insist. At the end, the retro turns these into ranges for the next project (see `handover-and-retro.md`).

## Proposing cuts

When the ordered list does not fit before a decision point:

1. For each piece still open, give the options: the full version, a shorter version (say what it leaves out), or none. Each with its range and what it displaces.
2. Recommend one combination and say why in one line.
3. Let the user choose. The choice is theirs, piece by piece; never cut on your own, and never leave the user to invent the cuts.
4. Write the choice down as made, with the time, in «Cut» and in the briefs affected (the director writes the shortened brief).

If the user picks something riskier than the recommendation, say the risk once, with numbers and what it pushes out, then make the choice fit: fixed times for the tail (freeze, final build, submission), a shippable state kept in git, and the deciding item repeated at each report until it is safe.

Expect the user to move a deadline that is theirs to move. Re-plan from the new decision points; do not argue it twice.

## Early end-to-end runs

Put one full end-to-end check early in «Next» (a packaged build, a deploy to a test site, a full test run on a clean machine), not only at the end, and the user's run of it in «Yours». Things the working environment hides show up only there.

## Cut proposals and the five-line report

A report is five lines at most, except a setup (which shows the drafts), a research piece's (which adds a short summary and the question about fit) and a cut proposal: that one carries a short table, one row per piece (full, shorter, none, each with its range split into the session's part and the user's part, and what it displaces), and one line with the recommendation.
