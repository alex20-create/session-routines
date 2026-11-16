Updated: 2026-03-14 18:20 · Checkout

<!--
Only the director writes this file. Before a session is archived, every open
item in its report is here: nothing pending lives only in a chat or a log entry.

Format, kept fixed so other tools can read it:
- the first line is "Updated: YYYY-MM-DD HH:MM · <project>";
- the nine "## " headings below, in this order, with these names;
- one item per line: "- ", then an optional "! " for something at risk of being
  forgotten, then fields separated by " · ";
- the first field is the ID or short name, the second says what it is; every
  later field is optional and starts with its label: "held by", "session",
  "readied", "since", "next", "needs", "blocks", "waiting on", "status", "cut by",
  "parked", "why", or is a
  commit, PR or time range in «Done»;
- a session title is always written inside «...», and a " · " inside «...» is
  part of the title, not a separator;
- times carry their date when the item is not from today.
Delete this comment and the example lines when you set the file up.
-->

## Resources

- e2e port · held by «B2 · checkout form · e2e port» · since 17:50 · next B3
- docs PR · free

## In progress

- B2 · checkout form · session «B2 · checkout form · e2e port» · since 17:50 · waiting on the user's acceptance check

## Yours

- ! B1 · try the address form on a real phone · blocks the release
- ! Release · run the release build once on a clean machine before shipping · blocks the release
- B4 copy · approve the line for the empty basket · blocks B4

## Next

- B3 · order history page · needs e2e port
- B4 · empty basket state · needs B4 copy

## Blocked

- B5 · payment errors · needs the provider's test keys

## Unverified

- B1 · the form keeps its values after a reload · session «B1 · address form» · status claimed, not checked

## Done

- B1 · address form · PR #12 · 2026-03-14 15:10 to 16:40 · check took 25 min

## Cut

- Saved addresses · not built · cut by the user 2026-03-14 · why the full version did not fit before the freeze

## Parked

- Dark theme · for the checkout · parked 2026-03-13 · why after the release
