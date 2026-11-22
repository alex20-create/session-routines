# Closing outside Claude Code

Read when the chat is not Claude Code on the user's machine: claude.ai, or
a cloud session. `SKILL.md` describes the close as it runs in Claude Code;
this file says what changes. The levels of `SKILL.md`, section 1, apply
here as well: they decide which of the steps below are in the plan.

## Which case this is

- **A device shell is listed.** The chat runs in a Linux container, but a
  shell tool for the user's computer is listed, so commands run there,
  inside the folders the user connected. The vault and any script stored
  in a connected folder are reachable. This skill's own files (the
  catalogue, `scripts/`) live in the container, not on that machine. Hooks
  do not run. Memory goes through the memory tools, and a background pass
  files durable facts after each turn.
- **No device shell.** Files on the user's computer are reachable only
  through the tools that stage a file into the container and commit it
  back, and only while the desktop app is linked. Otherwise nothing on
  their disk is reachable. Hooks and memory as above.

Say which one in the first line of the plan.

## Where the local map lives

There is no `CLAUDE.md` here. Look in the Project instructions, the user's
preferences and memory, and in a `Local map for this install` section that
a packaged copy of `SKILL.md` may carry. A map found there counts exactly
as `SKILL.md`, section 2, describes.

## How each category runs

**1 Memory: check, do not write.** The background pass already files
durable facts after each turn. Read the memory file(s) it is likely to
have used (the listing shows the paths) and say in the plan whether this
session's decisions are there. The pass runs after each turn, so what was
decided in the closing turn itself is not there yet and will be filed
after it; that is normal, not a gap. The platform only allows a memory
write on the user's explicit request, so if something they said is
missing, name it in the plan and let them say "save it"; that sentence is
the request. Inside a Project, writes go in the Project's own subtree, in
the form the memory instructions require.

**1b Handoff note, 2 Learnings: skip when not installed.** There is no
replacement; a Project document, a new note or a chat summary does not
become one (the one-place rule of `SKILL.md`, section 3).

**3 Vault sync: depends on reach.** With a device shell and the vault
folder connected, run the sync skill if it is installed; if it needs
something this environment lacks, it will say so, and then do the sync by
hand. Without a shell, the device file tools still reach the vault while
the computer is linked, so the sync skill is still the step: run it, and
do the sync by hand only when it is genuinely not installed (confirmed
with a skill-listing tool, not from the injected listing alone) or when it
says it cannot write from here (a sync skill may fall back to text for the
user to paste), and then write through the file tools yourself instead of
handing the user text. Either way, read the vault's own conventions note
first (stage it when there is no shell), and put each proposed change in
the plan as what stays, what changes and what disappears, so the single
confirmation covers the writes. After each write that goes through the
file tools, confirm it landed by listing the folder and checking the
file's size, because the commit reports success either way. No hook logs
the session here, so the light level's vault sync is not skipped on that
account: what is not synced now was never captured. Say so.

**4 Graph: unchecked.** The script runs in the container and the graphs
are on the user's disk, so it cannot see them: report every graph as
unchecked, which is not "nothing to update".

**5 Context save.** The rule of `SKILL.md`, section 3, applies unchanged:
the place the project instructions name is the context save.

**6, 7 Optional: skip** unless the session corrected a memory or changed a
rule that a `CLAUDE.md` describes.

## Claimed writes

Check them as `SKILL.md`, section 3, says, with one more caution: a write
committed to the user's computer through the device file tools can come
back with a fresh modification time and the old content, so compare the
size or a distinctive line, never the timestamp alone.

## Costs

The catalogue's figures were measured in Claude Code, where the steps are
different. Here they are only an estimate from another setup: say so, or
leave the figure out.
