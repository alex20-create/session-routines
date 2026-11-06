---
name: skill-picker
description: "Before any piece of work: recommends which installed skills fit the task, in what order, and which model tier it needs, as a simple list or in phases when the task is large or the user asks, then waits for confirmation. Also use when the user asks whether a skill exists for something, wants to find or install new skills (from the skills.sh registry or GitHub), or wants to extend what Claude can do. Triggers: \"which skills should I use\", \"what model for this\", \"is there a skill for\", \"find a skill that\", \"/skill-picker\"; in Spanish \"qué skills uso\", \"qué modelo uso\", \"elige skills\", \"¿hay alguna skill para...?\", \"busca una skill\"."
---

# Skill picker

A start-of-task routine. Before any work begins, the user sees which skills
suit the task, in what order, and whether the model they have selected is the
right tier, and then decides. Most setups have many skills installed and many
more available outside; this skill is how to find your way among them for any
kind of work.

## Local map first

Before anything else, look for this skill's local map: a section named
`skill-picker local map` in the user's standing instructions (their
`CLAUDE.md` files in Claude Code, read from disk rather than from the copy
in context, which can predate an edit; the Project instructions or the
user's preferences in claude.ai). A section named `Local map for this
install` inside this SKILL.md, added when the skill was packaged for one
claude.ai account, counts too; standing instructions that say otherwise win.
It holds what only that user's setup knows, for example:

- the language and style of the reply;
- how long a proposal they want (a cap other than 10, or "short lists only");
- which routine opens a session and hands the chosen task to this skill, and
  which one closes it;
- which installed skill vets third-party code before installing it;
- budget rules (free options first, paid tools flagged).

Where the map says something, it overrides the defaults below. Where there is
no map, use the defaults and do not offer to write one unless the user asks
why a default does not suit them.

## When to use it

- When the user invokes it by name or asks which skills or which model to use,
  for any kind of work. This is the main use.
- At the start of a multi-step task, in the first message or midway through a
  conversation: creating files or documents, coding, designing, researching,
  planning, writing.
- When the task changes completely midway through a session.
- When the user asks whether a skill exists for something or wants to look for
  new ones. Check first whether an installed skill already covers it and say
  so in one line; if none does, go to "Finding new skills" without asking
  again, because they already asked.

## When not to use it

These exclusions apply only when you would be using it on your own
initiative. When the user invokes it explicitly, it always runs, even if it
already ran for the same task.

- Quick questions or conversation answered without tools.
- The user already named the skill and the model they want.
- More than once for the same task.
- Unattended sessions (see "Sessions without the user").

## Two modes

- **Simple mode:** an ordered list of skills and a model recommendation. No
  phases.
- **Phased mode:** the skills grouped into stages of work, with a model tier
  per stage.

Choose the mode after selecting and ordering the skills (Part 1, steps 1 to
10), with this check. Use phased mode if any of these holds:

1. The user asks for it ("in phases", "con fases", "plan mode" or similar).
2. The main list has 5 or more skills. Alternatives named on the same line as
   another skill do not count.
3. At least one execution skill (calendar, pieces, code, final document) comes
   after a decision skill (strategy, approach, identity).

If none holds, use simple mode. Do not leave the choice open: the check
decides. The user can ask for the other mode at any time.

Phased mode does not replace planning skills: the phases say which skill to
use when, not the detailed plan of the work.

## Part 1: skills

Common to both modes:

1. Summarise the task to yourself in one line: what the user wants to achieve
   and in what format. If the conversation has moved on, base it on what has
   been discussed, not only on the last message.
2. Go through the list of available skills that the session puts in context.
   Work only with skills on that list; never invent names.
3. Leave out infrastructure skills that load by themselves when a specific
   tool is needed (browser control, computer use, artifact design, document
   connectors).
4. Skills serve the task, not the other way round. Recommend only those that
   help do what the user asked. A skill that would add work they did not ask
   for (a competitor analysis when they only want a calendar) goes to "Other
   options", not to the main list. A step the task itself implies is not
   extra work: measuring results needs goals to measure against, so a
   goal-setting skill belongs when the user asked to measure.
5. At most 10 skills in total, unless the local map sets another cap. Include
   every relevant skill that adds something distinct, up to that cap.
   Prioritise those that change the result (method, output format, quality)
   over those that only share the topic.
6. No overlaps in what matters. Before adding each skill, check it against
   every one already chosen: does it add something no other covers? Two skills
   overlap if they produce the same result or one is a special case of the
   other (a "behind the scenes" content skill against a content-pillars skill,
   where the first is one kind of pillar). A skill that produces one part of
   another's output (hooks for a script, a logo for an identity) does not
   overlap with it when the part deserves its own method; keep both and say
   which feeds which. If they overlap, keep the broader one or the better fit
   and name the other as an alternative on the same line. Alternatives do not
   count toward the cap.
7. Order the skills in the order they will be used, following this sequence:
   - Gather: research, audience or competitor analysis, collecting what
     already exists.
   - Decide: strategy, approach, identity, tone, and also goals and
     indicators. Setting what success means is a decision and goes here, next
     to strategy.
   - Execute: calendar, pieces, code, final document.
   - Review: measuring results, analysing how what was published or launched
     performs. Only this goes last.
   Before answering, walk the list top to bottom and check that no skill needs
   the output of one that comes later; if one does, reorder.
8. A skill that appears in the list without a description can still be
   recommended by its name, but flag it so the user knows how far to trust the
   choice (see "Reply format"). Do not load it to check before the user
   confirms. When two candidates without descriptions differ only in name
   (`reels-script` and `short-form-video-script`), pick one and name the other
   as its alternative; do not pretend to know which is better.
9. If, going through the list, you find other relevant skills you are not
   recommending, note them for the "Other options" line.
10. If part of the task is not covered by any installed skill, note it to
    offer a search (see "Skills that are not installed"). A part that needs
    data no tool in the session can reach (analytics for a social account,
    with no connector for it) counts as not covered: say which data is
    missing, in the same line as the offer, and offer to look for a skill or
    a connector. A connector the session lists as needing authorisation is
    not missing: tell the user to authorise it instead.

Then choose the mode (see "Two modes").

Phased mode only:

11. Define the phases from what the task needs, not from the skills: do not
    create a phase because a skill exists for it. Phases usually match the
    blocks of step 7 (gather, decide, execute, review). Merge blocks when they
    happen together in practice; split one only when its parts need different
    model tiers. At most 5 phases.
12. There is no cap per phase; the cap is for the total. A phase may have no
    skill if it needs none; say so.

## Part 2: model

You cannot change the model; you can only recommend. The user changes it with
`/model` or the app's model selector.

Reason by tier, not by version number, because versions change:

- Light (the Haiku family): short, mechanical tasks. Reformatting,
  translating a short text, renaming files, summarising something short,
  quick answers.
- Middle (the Sonnet family): most work. Writing ordinary functions, writing
  and editing text and documents, analysing one file, planning a familiar
  project.
- Strong (the Opus family): when a mistake is expensive or the task is long
  and tangled. Architecture decisions, a bug nobody can find, creating or
  reviewing something that will be reused many times (skills, plugins,
  configuration), an important script or document that will be sent or
  published, reasoning with many pieces at once.

### Steps

1. Find out which model is active if the context says. If you do not know, do
   not guess: recommend the tier and say you cannot see which one is
   selected. If you are running as a subagent, your own model is not
   necessarily the user's; say so.
2. Start from the lowest tier and move up only for a concrete reason from that
   tier's list. "It seems important" is not enough: name the item of the
   list that puts the task in the chosen tier ("it will be published", "it
   will be reused many times"). In phased mode, do this for each phase. In the
   reply, name the tier and its family ("middle, Sonnet").
3. Compare with the active model:
   - If it matches, say so in half a line.
   - If the active one is above what is needed, recommend going down: it saves
     usage without losing quality.
   - If it is below, recommend going up.
   - If different parts of the task need different tiers, recommend starting
     in one and switching at the specific part that needs the other. In
     simple mode, name the skill or step at which to switch.

### Special cases

- If the active model belongs to a tier above the three listed here, say so
  and do not judge it on the three-tier scale, which does not cover it. If the
  task is clearly light or middle, you may still suggest going down.
- You are the model that is running, and you tend to confirm that you fit.
  Before confirming the active model, check explicitly that the tier below
  would not do, and give that reason in the reply.
- Do not give prices or usage figures; if the user asks, point to Anthropic's
  official documentation.

## Task already under way

If invoked when work has already started in the conversation:

- Do not restart the task or repeat what is done. In phased mode, mark
  finished phases as done instead of proposing skills for them.
- If questions to the user were left unanswered, recall them in one line
  ("Your answers on X, Y and Z are still pending"), without restating them.
- If a skill with a known description would have changed what is already
  done, say so in one sentence so the user can decide whether to redo that
  part. For skills without a description, do not claim what they would have
  changed: at most, say it cannot be known until they are loaded.

## Reply format

Order: skills (as a list or in phases), other options (if any), model, note on
work already done (if any), pending questions (if any), and the closing
question. The search offer, when it applies, goes after the model: when no
installed skill fits it is the closing question; otherwise it joins the
closing question, so the reply still ends with one ("Go ahead with this, and
shall I look for a skill for X?").

### Simple mode

One line per skill, in order of use, with the short name and the reason:

- short-name: why it helps here.

### Phased mode

Each phase with its title and the model tier it needs, and its skills under
it:

**Phase 1: short phase name** (tier)
- short-name: why it helps in this phase.

### Common to both modes

The reason says what the skill is for in this task. Do not anticipate the
content of the work (no pillars, topics or concrete decisions yet): that comes
later, once the user confirms.

The short name is the last part of the name, without the plugin prefix
(`brainstorming` rather than `superpowers:brainstorming`). Use the full name
only when loading the skill. If two installed skills share a short name, add
the plugin or a distinguishing trait in brackets.

Skills without a description:

- If only some are affected, add "(no description)" after each name.
- If all the recommended ones are, do not repeat it on every line: put one
  note under the list ("None has a description; I chose them by name").

Other options: if you found more relevant skills you are not recommending,
mention them in a single line, by short name only, at most three, choosing
those closest to the task ("These could also fit: a, b and c"). No reasons or
descriptions. If the user asks about one, explain it then. If there are none,
leave the line out.

Model: in simple mode, one line with the tier, the reason and the comparison
with the active model. In phased mode, up to three lines after the phases: the
reason for each tier, the check that the tier below would not do, the
comparison with the active model and where to switch.

Then a single question: whether to go ahead with the proposal or change
something. Do not load any skill before the answer.

If no skill adds anything clear, say so in one sentence, give the model
recommendation and replace the closing question with the search offer.

## Skills that are not installed

Never propose installing anything on your own initiative.

- If no installed skill fits the task, or an important part of it is left
  uncovered, offer to search in one line, naming the part if there is only
  one: "Do you want me to look for a skill for X?". Do not search or recommend
  anything until the user says yes.
- If the user accepts, or asks on their own whether a skill exists for
  something ("is there a skill for...", "find a skill that...", "can Claude
  be extended to..."), follow "Finding new skills". The decision to install is
  always theirs.
- If the installed skills cover the whole task, do not offer the search.

## Finding new skills

You only get here if the user said they want to search. A third-party skill
can run commands on their computer, and not every user can judge a script;
so each step that downloads, reads or installs something is explained first in
one sentence and waits for a yes.

There are two sources. Use whichever is available; if one fails, carry on with
the other and say so. Both need a shell; where there is none (claude.ai), use
web search for the same terms, present candidates the same way, and tell the
user that installing there means downloading the skill's folder as a zip and
uploading it in the skills settings.

### Source 1: the skills.sh registry

1. **Ask before the first `npx`.** Explain that `npx -y skills ...` downloads
   the `skills` package from npm and runs it on their machine, and wait for a
   yes. If they say no, this source ends here.
2. Run two or three searches with concrete words from the task, from most
   specific to most general, in English and in the user's language:
   ```bash
   npx -y skills find "podcast script"
   npx -y skills find "audio"
   ```
   Always pass a term: `npx skills find` with no term opens an interactive
   search that waits for the keyboard and hangs.
3. To see what a candidate contains without installing it:
   `npx -y skills add <owner/repo> --list`.
4. **"No skills found" does not mean nothing exists.** It can be a network
   failure. If every search comes back empty, try a web search
   (`skills.sh <topic>`) before concluding, and tell the user exactly that.

### Source 2: GitHub

Some skills are published only in GitHub repositories and never reach the
registry. Use this source only if GitHub is connected:

1. **Check the connection.** If the session has tools from a GitHub
   connector, use them. If not, check whether the GitHub CLI is installed and
   signed in: `gh auth status`. That command downloads nothing. If there is
   neither a connector nor a signed-in `gh`, say in one line that GitHub is
   not connected and carry on with source 1 only.
2. **Search for SKILL.md files**, which every skill has, with words from the
   task:
   ```bash
   gh search code --filename SKILL.md "podcast script" --limit 20
   gh search repos "claude skills podcast" --limit 10
   ```
   If results are few, try synonyms, in English and in the user's language.
   Skill repositories often carry topics such as `claude-skills` or
   `agent-skills`; use them as a hint, not as the only filter.
3. **Read the SKILL.md without installing anything**:
   ```bash
   gh api repos/<owner>/<repo>/contents/<path-to-skill>/SKILL.md -H "Accept: application/vnd.github.raw"
   ```
   Check whether the skill folder ships scripts too
   (`gh api repos/<owner>/<repo>/contents/<path-to-skill>`).
4. For each candidate, note stars, date of last change and licence
   (`gh repo view <owner>/<repo> --json stargazerCount,pushedAt,licenseInfo`).
   A repository with few stars is not bad in itself, but tell the user so they
   know how far to trust it.

### Filter and present

1. Drop what duplicates something already installed. Prefer known sources
   (Anthropic, whoever officially maintains the tool in question, repositories
   with many installs or stars).
2. Present at most five candidates, from either source, with: name, what it
   would do in this task, source (registry or GitHub), installs or stars if
   any, link, and whether it ships scripts that run. Ask which to install,
   with a "none" option.

### Before installing

If the user picks one, vet it before installing, above all if it comes from
GitHub or ships scripts: use the installed skill whose description covers
auditing third-party skills or code for security risks (the local map may
name it). Tell the user the result in one sentence. If the review finds
something serious, recommend not installing and let them decide. If no such
skill is installed, read the skill's files yourself, say what its scripts do,
and say that this was a reading, not an audit.

### Install

Only what was approved:

- **From the registry or a compatible GitHub repository:**
  `npx -y skills add <owner/repo> --skill <name> -g -a claude-code -y`
  (global, so no files land in any project). On Windows add `--copy`: by
  default the CLI creates symbolic links, and creating them on Windows can
  need special permissions.
- **From a GitHub repository the CLI does not recognise:** copy only that
  skill's folder into the user's skills folder (`~/.claude/skills/<name>` on
  macOS and Linux, `%USERPROFILE%\.claude\skills\<name>` on Windows). Say first
  which folder you will create.
- **Plugins from a marketplace:** ask the user to type
  `/plugin install <plugin>@<marketplace>`.

If the new skill does not appear in the session's skill list, the session
needs restarting: say so.

## Sessions without the user

If the session comes from a scheduled task or the user said they will be back
later, do not wait for confirmation: choose the mode and the skills, say at
the top which ones you are using and why, add the model note so they see it
when they come back, and carry on. Do not search for or install new skills in
these sessions.

## Other start-of-session routines

- **A session-opening routine** (a skill that reads where a project's work was
  left and then hands over the task the user picks; the local map may name
  it): if it called you, the context is already in the conversation. Do not
  reread git or notes, and do not repeat its summary; start from the task. If
  you are invoked at the start of a session on a project with history and that
  routine is installed but has not run, do not launch it yourself: do your
  job and, if the user does not know where they left off, suggest it in one
  line.
- If another installed skill also asks to run at the start of every
  conversation (using-superpowers, for example), this one goes first and only
  recommends. The other decides afterwards how the chosen skills are applied.

## Style

Reply in the language the user writes in, unless the local map sets another
rule. Be direct: do not restate the request, and do not explain how each skill
or model works inside.
