# Resuming in a claude.ai project

What is specific to a claude.ai chat. Here there is no user disk, no repository, no vault and no close-out notes: code runs in an isolated container without the user's files. What remains from earlier sessions is in four places within the project itself: the previous chats, the project memory, its files and its instructions. There is no git here, so the role of "what really happened" is played by the most recent chats.

**No writing.** Do not edit or upload project files, do not change its instructions and do not ask to save anything to memory. Reading chats and files changes nothing, so do not ask permission for it.

## Which project it is

- If the chat is inside a project (there are project instructions or files in the context), that is the project.
- If the chat is outside any project, chat search and memory only reach what is outside projects: a project's chats and memory cannot be seen from outside it. If the user names a project, tell them in one sentence to open the chat inside that project to resume it, and deal with whatever they ask.
- If there is nothing to resume (a project with no previous chats and no files), say so in one sentence and go straight to the handover (step 6 of `SKILL.md`) with whatever the user wants to do.

## Sources, in reading order

**A. Previous project chats.** The most recent and most reliable source on state: the last thing done, what was left half-done and what was decided. Use whatever tools the session has to search or list previous chats: first the project's most recent ones, then a search on the topic that seems pending if needed. For each one, note its date. If the last chat was working on a text (a scene, a chapter, a plan), note which version was the latest and which chat it is in: a text delivered in a chat is not in the project files until the user uploads it.
- If there are no chat search tools (a plan without it, or the "Search and reference chats" option turned off), say so in "Heads-up" and carry on with the rest. Incognito chats cannot be searched.

**B. Project memory.** If it is turned on, it arrives on its own in the context: do not ask for it. It gathers topics and preferences, not a dated log, so use it for the why and for what the user wants, not to decide what is done.

**C. Project files.** Uploaded drafts, notes and exports. They arrive in the context or, if the project is large, through search in the project files. For each one, note its date. Claude cannot see when it was uploaded, so the date comes from the text itself: a generated export states it at the top ("Generated on …"), a draft may carry it in its title or in a header. Without a date, say so: there is no way to know whether it is behind. An export generated from somewhere else (the vault, another repository) is not a source for anything: it describes that place as of its date, and what it says may already be superseded there.

**D. Project instructions.** They arrive on their own in the context. They say what the project is and how it is worked on; they almost never carry a date, so do not take them as state unless they explicitly say "current state" with a date.

## If the sources disagree

- **On state** (what is done, which version of a text is the latest, what is left), the most recent chat wins; among files, the one with the newest date.
- **On the why and the decisions**, the instructions, the files and memory win, even if they are behind on state.
- If the files are older than the last chat in which work was done, they are behind: say so in "Heads-up" with both dates. If a later chat produced a new version of a text that is still old in the files, name it: uploading it can be one of the options in the question.

## What it adds to the summary and the question

**Where you left off** comes from the most recent chat, with its date. There is no "Git" line. In **Pending**, whatever the chats, the files or the instructions leave pending and no later chat considers done. In **Heads-up**, files that are behind the chats, chat search being unavailable, or a text that only exists in a chat.

This skill only reads: if an option in the question is to bring a project file up to date, the session does it afterwards, and uploading it to the project is up to the user.
