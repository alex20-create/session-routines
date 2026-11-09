---
name: plan-admin
description: "Work-planning routines for people who run several projects in parallel: a daily plan (today's blocks, each with its next action and a first step), a day close (where each block was left and the next actions for the next working day) and a weekly review (what went well, collisions, priorities). Reads the schedule, rules and project status from the user's project manager and project instructions, in claude.ai or in Claude Code. Use it whenever the user says 'what's on today', 'what should I do today', 'plan my day', 'where do I start today', 'I'm done for today', 'closing the day', 'weekly review', 'what have I got this week', 'what's on today for my-app', or the equivalent in their language (in Spanish, for example, 'qué toca hoy', 'cierro el día' or 'revisión semanal'), even if the skill is not named. Do not use it to open a session on a project with history (that is a session-opening skill such as resume-project), to archive or close the chat, or to choose skills for a task."
---

# Plan admin

Three routines for running several projects in parallel: starting the day, closing it and reviewing the week. The skill provides the method; each project provides the data (schedule, rules, which project goes on which day, where the next action is stored) in its instructions and its project manager. That way the same skill works in any project without copying its data, and every piece of data still lives in one place only.

Talk to the user in the language they use, including the labels of the formats below.

## Before any routine

### Check the date

Get the current date and time from whatever tool is available (a clock tool in the session, or `date` in a terminal), in the user's time zone. Do not infer it from the conversation or the latest note: a wrong day throws the whole plan off.

### Gather the project's data

Check which tools the session has (deferred ones included) and read, in this order:

1. **Project instructions, `CLAUDE.md` and user preferences.** They say which phrases start each routine, which block always comes first, which days are off, where status lives and what can be written without asking. Whatever they say takes precedence over this skill.
2. **The schedule and rules page**, if the instructions name one (for example, a weekly review page in Notion with the current schedule, the rules, items pending review and a review template). It tells you which project goes in which block on each day.
3. **The projects database**: status, priority, key date and next action for each project.
4. **The tasks database**, if there is one: unfinished tasks with a date.
5. **If there is no project manager**, the status and pending sections of `CLAUDE.md`, or the project's note in the user's notes app.

Do not ask for anything those sources already hold. If you do not have the address of a database or page, search for it by the name the instructions give; if it does not turn up, say so in one line and carry on with what there is.

If one source contradicts another (the instructions say one thing about the schedule and the page says another), flag it and do not choose for the user.

### Which routine

A phrase from the description or the instructions picks the routine. If the skill is invoked bare (its name or slash command with nothing after it), or the phrase fits more than one routine, ask in one line which of the three the user wants, offering first the one the day and time make likelier: the daily plan before the first block, the day close after the last. Do not choose from the clock alone.

### Which projects

The scope comes from, in this order:

1. **The user's words.** A project named in the request, or "the whole day", sets it.
2. **Where the session is.** If the working folder belongs to exactly one project, the routine covers that project only. It belongs when it is the project's repository or sits inside it, when it holds it (a project folder with its repository and side material in subfolders), or when its name, a repository link or a path matches one project in the projects database, the instructions or the notes vault, case-insensitively. In claude.ai, a Project that holds one project's work counts the same. Say in the first line that the plan covers that project only, and offer the whole day in the same line.
3. **Otherwise, everything the schedule names.** At the root of a workspace with several projects, in a Project that organises all the work, or when the folder matches none or more than one project.

With one project in scope, each routine shrinks to it: its next action and first step, and, when the schedule gives it a block, which day and which block that is (today's, or the next one). Date alerts and collisions cover that project only; anything due today or tomorrow in another project still goes in one line, because missing it costs more than the line. The day close asks only where that project was left, and checks the next action for that project's next block, whatever day it falls on. The weekly review always covers everything; from a project's folder, say so in one line before starting.

With no schedule at all, the same rule applies and the scope is a single block. Do not invent a schedule. If the user wants one, help them write it down in their project manager or instructions, with their approval.

## What counts as a next action

Something physical and concrete that can be done in under two hours, unless the instructions set a different limit. "Write the email asking for a quote" works; "move the project forward" does not. The first step is smaller still: what gets done in the first five minutes ("open yesterday's draft and reread the last paragraph"). It exists to make starting easy on days when starting is hard.

When a project has no next action, suggest one and mark it as a **proposal**, saying where you got it from (the latest note, an open task, the status). Do not write it to the project manager until the user approves it.

## Before calling something pending

Project managers fall behind: work gets done under another name, in another task, or in a session that never recorded it. Before saying something is still pending or overdue, look for signs it was already done: the task marked as done, a later note or session log, a commit, an entry in the weekly review. If there are any, mark it "to be confirmed" instead of pending. One false "this still isn't done" costs trust in everything else.

## 1. Daily plan

Start only when the user asks for it. In any other conversation, do not give the day's plan unless asked.

1. **Day off.** If the rules say today is a day off, say so in one sentence and stop. Do not suggest work or catching up.
2. **Today's blocks.** Take from the schedule which project goes in each block. If the instructions set a block that always comes first, put it first.
3. **For each block**: the project, its next action (from the project manager, or a marked proposal) and a first step of a few minutes.
4. **Date alerts.** Check key dates and dated tasks across every active project in scope (see *Which projects*), not just today's blocks. Anything due today or tomorrow goes at the very top, before the blocks. Anything due in the next seven days goes in a single line at the end. Anything further out stays out, unless preparation has to start now to make it.
5. **Stacking commitments.** If several key dates fall in the same week within the next fourteen days, or two projects need the same resource, person or money at the same time, say so in one line and state exactly what overlaps. Do not say what should give way: that is the user's call.
6. **Coming back after time away.** If the latest recorded activity (the last day close, the last edit to a next action, the last session) is more than three working days old according to the schedule (or more than four calendar days if there is no schedule), open with what fell due in the meantime, in one line, and give the rest as usual. No reproach for the gap. If a session-opening skill has already said this in the session, do not repeat it.
7. **Items pending review.** If the schedule page lists items pending review whose condition has now been met (a date that has passed, a milestone reached), mention it in one line.

Format, short and in this order (leave out anything empty):

```
**Due today:** <only if something is due today or tomorrow>
**<Fixed block, if any>:** <project>. Next action: <...>. First step: <...>.
**Main:** <project>. Next action: <...>. First step: <...>.
**Secondary:** <project>. Next action: <...> (proposal, from <source>). First step: <...>.
**This week:** <dates in the next seven days, on one line>
**Heads-up:** <overlaps, items pending review or sources that disagree>
```

Use the block names the schedule uses; "Main" and "Secondary" are only the default for a two-block day.

## 2. Day close

1. **Ask in one line** where each of today's blocks was left, naming them ("Where did you leave the client proposal and the website copy?"). If the conversation already makes it clear, do not ask.
2. **Acknowledge what got done**, in one concrete sentence: what actually moved forward, without inflating it. If a block did not move, say so plainly and without blame; a slow day is recorded too.
3. **Propose next actions**, following the rule above:
   - For each project worked on today, the next action that follows from where it was left.
   - For the blocks of the next working day (which may be different projects), check that their next action is decided. If it is missing or stale, propose one. If tomorrow is a day off, look at the next working day.
4. **Write only what is approved**, in the field the instructions name (for example, a "Next action" field in the projects database). That field is the only place where it is recorded where each thing was left: do not copy it into notes, memory or any other file.
5. **Check the write.** Read the field back after writing it and say what is there. Do not say "saved" without having seen it.

This routine closes the working day, not the chat. If the user is also about to archive the conversation, that is a job for a session close-out skill, if one is installed.

## 3. Weekly review

1. **Template.** If the schedule page has a review template, follow its sections in order. If not, use: what went well, what got stuck and why, status of each area or project, three priorities for next week.
2. **Fill in what the sources say**: tasks closed this week, next actions that changed, notes and sessions from the week. Mark anything you inferred as a draft.
3. **Ask what only the user knows** (why something got stuck, how the week felt), all together in a single round.
4. **Collisions.** Look at key dates over the next three weeks and at shared resources. Flag each collision and state exactly what overlaps. What gets dropped is the user's decision: do not propose it, and do not propose cutting the number of projects unless they ask.
5. **Priorities.** If the user asks for a recommendation, give yours with its reason, but leave the decision visibly theirs.
6. **Items pending review** on the schedule page: mention the ones now due.
7. **Write with approval.** Show the full review before writing it to the project manager (duplicating the template, if that is how it is done) and check afterwards that it landed.
8. **Finish with the template's closing checklist**, if it has one, item by item.

## Rules for all three

- **How many projects to run is the user's decision.** Do not suggest focusing on fewer projects, dropping areas or "picking one thing" unless they ask.
- **No invented figures.** Dates, deadlines, hours and progress come from a source. Anything without one is marked as a proposal or left as PENDING.
- **Goals are set from the real hours in the schedule**, not from what would be convenient.
- **No blame.** No "you should have", no comparisons and no reproachful tone, including about things that slipped.
- **Writing needs approval**, unless the instructions allow something to be written without asking. Reading does not.
- **One routine, one short answer.** It should take under a minute to read. If it runs past twelve lines, something can go.

## With other skills

- **A session-opening skill** (such as resume-project) may offer the daily plan as its first option. If it hands over to you, the context has already been read: do not read it again.
- **A skill-selection skill**, if one is installed, comes afterwards, when the plan turns into a concrete multi-step task. This skill does not choose the task; the user does.
- **A session close-out skill** closes the chat, not the day.

## Sessions without the user

In a scheduled session, produce the daily plan and leave it at the top of your work. Do not write to the project manager, and do not run the day close or the weekly review, which need the user's answers.

## Setting it up

For the routines to work beyond a single block, the user's project instructions (or `CLAUDE.md`) should say:

- where the schedule and rules live (a page, a file or the instructions themselves), including days off and any block that always comes first;
- where projects live, and which field holds each project's next action;
- where tasks live, if they are tracked separately;
- anything that may be written without asking.

If none of that exists yet, offer once to help the user write it, and keep working with what there is.

## Style

Direct, without repeating what the user said. What to do first, the reasons after, and only if needed.
