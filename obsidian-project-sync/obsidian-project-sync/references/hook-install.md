# Installing the session log (`SessionEnd` hook)

With this, every Claude Code session that ends inside a git repository leaves
a record of what happened: date, branch, new commits since last time, files
touched and whether anything was left uncommitted.

**Where it goes:** the logs folder the vault declares in its
`.claude-vault.json`, one JSON per repository. `scan` returns it in
`config.logs`.

**What it does not do:** write in any note. A hook is a script with no model
behind it, so it cannot draft prose. Its job is to keep the trail of what was
done; drafting comes later, when the user asks for an update and Claude has
the log in front of it. Make that clear, so nobody expects the note to change
by itself.

Official hooks documentation: https://code.claude.com/docs/en/hooks

---

## Step 1: find Python, by its absolute path

The hook runs outside any shell profile, so a `python` that works in your
terminal may not be on the PATH Claude Code sees. Use the interpreter's
absolute path in the hook.

macOS and Linux:

```bash
command -v python3
```

Windows (PowerShell):

```powershell
(Get-Command python).Source
```

If nothing comes back, Python is not installed: get it from python.org (on
Windows, tick "Add Python to PATH" in the installer).

## Step 2: find the script

It is `scripts/vault.py` inside the installed skill, usually
`~/.claude/skills/obsidian-project-sync/scripts/vault.py`
(`%USERPROFILE%\.claude\skills\obsidian-project-sync\scripts\vault.py` on
Windows). Note its absolute path.

## Step 3: try it by hand before automating it

From inside a real project's repository:

```bash
python3 /absolute/path/to/vault.py log --vault "/path/to/vault"
```

It should answer with the path of the JSON it wrote. Open it and check the
branch and commits are right. If the folder is not a git repository the
script does nothing, on purpose: the log exists to check commits against,
and without a repository it would only write empty sessions.

Note that there is **no** `--stdin` here: by hand, the folder is wherever you
are. That flag is for the hook only, which receives a JSON from Claude Code on
standard input and closes it at the end. Pass it by hand from something that
leaves standard input open and the script waits for input that never comes.

## Step 4: edit `settings.json`

The file is `~/.claude/settings.json` (`%USERPROFILE%\.claude\settings.json`
on Windows). It may not exist yet. **Back it up first.**

Add this `SessionEnd` block (also in the skill's repository as
`hook/settings.example.json`), with the three absolute paths filled in: the
interpreter, the script and the vault.

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"/usr/bin/python3\" \"/home/you/.claude/skills/obsidian-project-sync/scripts/vault.py\" log --quiet --stdin --vault \"/home/you/Obsidian/MyVault\"",
            "timeout": 20
          }
        ]
      }
    ]
  }
}
```

The same command on Windows:

```json
"command": "\"C:\\Python312\\python.exe\" -X utf8 \"C:\\Users\\you\\.claude\\skills\\obsidian-project-sync\\scripts\\vault.py\" log --quiet --stdin --vault \"C:\\Users\\you\\Obsidian\\MyVault\""
```

If the file already has content, **do not replace it**: add the `"hooks"` key keeping everything else, or put `"SessionEnd"`
inside the hooks already there. Malformed JSON makes Claude Code ignore the
whole configuration, so validate afterwards:

```bash
python3 -c "import json,os;json.load(open(os.path.expanduser('~/.claude/settings.json')));print('JSON OK')"
```

On Windows, backslashes are doubled inside JSON (`\\`) and the quotes around
each path are escaped (`\"`). That is by far the most common mistake. Keep
`-X utf8` after the interpreter on Windows: the hook's input arrives as UTF-8
and the default console codec is not.

Instead of `--vault` in the command, the hook can rely on an
`OBSIDIAN_VAULT` environment variable, but only if it is set where Claude
Code itself starts, not just in one terminal. The explicit flag is the safer
choice.

## Step 5: activate and check

Hooks are read when a session starts: end the Claude Code session and open
another. (`/hooks` reloads the configuration without restarting, but it opens
a terminal dialog that the desktop app does not have; there, restart the
session or run it from an interactive `claude` terminal.)

Then work for a while in a project, end the session, and look at the JSON in
the logs folder: it should have a new entry with today's date.

---

## Details

- It only acts in git repositories, and asks git to confirm it.
- It keeps the last 20 sessions per repository and drops the oldest.
- Commits are counted from the last one recorded, so they are not repeated
  across sessions. The first time it takes the last ten.
- If anything fails, it exits 0 in silence. A hook that returns an error can
  get in the way of closing the session, and a log entry is not worth that.
- `.json` files do not show up as notes in Obsidian, so they do not clutter
  the graph.
- To turn it off, remove the `SessionEnd` block or restore the backup.

## Alternative: `Stop` instead of `SessionEnd`

`Stop` fires every time Claude finishes a reply, far more often. `SessionEnd`
is right for this. Switch only if the user leaves sessions open for days.

## On automating the drafting too

The hook could launch `claude -p` so that a model drafts and updates the note
unattended. It is not set up that way: it spends tokens at every session end,
Claude Code may cut off slow processes started from `SessionEnd` before they
finish, and above all it would write into a hand-curated note with nobody
reviewing the diff. If the user asks for it, explain those three things
before setting it up.
