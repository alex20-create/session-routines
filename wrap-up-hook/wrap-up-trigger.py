"""UserPromptSubmit hook: nudge Claude to run /wrap-up when the user is closing the chat.

Claude Code pipes the prompt in as JSON on stdin. If the text says the user
is about to archive or close the chat or session, we answer with
additionalContext so Claude invokes the wrap-up skill before doing anything
else. Any other prompt gets an empty reply and costs nothing.

Deliberately narrow: "archivar" and "cerrar/close" next to "chat/sesión"
only. Words like "termino" or "acabo" appear in ordinary sentences ("cuando
termino el build") and would fire on every other message.

Two guards against false fires, both measured in real sessions:
- A phrase inside quotes, code or a blockquote is someone else's words
  (a pasted document, a quoted scenario, an agent's report), not the
  user's intent; quoted spans are stripped before matching.
- A closing message is short, or closes with the phrase. In a long
  message only the first and last stretches are searched, so a document
  that mentions archiving in its middle does not fire.
"""
import json
import re
import sys

PATTERNS = [
    # "voy a archivar": the infinitive is unambiguous. "archivo" alone is not —
    # it usually means a file — so the conjugated forms need chat/sesión next
    # to them.
    r"\barchivar\b",
    r"\barchiv[oae]\b.{0,20}\b(chat|sesi[oó]n|conversaci[oó]n|esto|este)\b",
    r"\barchiv(e|ing)\b.{0,20}\b(chat|session|conversation|this)\b",
    # cierro / cerrar / cerramos ... el chat / la sesión / esta conversación
    r"\bcerr(ar|amos)?\b.{0,20}\b(chat|sesi[oó]n|conversaci[oó]n)\b",
    r"\bcierr[oa]\b.{0,20}\b(chat|sesi[oó]n|conversaci[oó]n)\b",
    # close / closing this chat / the session
    r"\bclos(e|ing)\b.{0,20}\b(chat|session|conversation)\b",
]

# "wrap up" / "wrap-up" as a phrase — not as a file or path
# ("notes/wrap-up.md", "skills/wrap-up/") and not the slash command, which
# is handled separately. Checked apart from PATTERNS because its guard
# needs more than a lookbehind: the NAME of the skill ("the wrap-up skill",
# "mi skill wrap-up", "la nueva wrap up") must not fire, and a determiner
# may sit one word away from the phrase.
WRAP_UP = re.compile(
    r"(?<![\w/\\.-])wrap[\s-]?up(?!\s+skill)(?![\w/\\.-])", re.IGNORECASE
)
# A determiner or the word skill in the couple of words before the phrase
# means it is being talked about, not invoked; the optional middle word
# covers an adjective ("la nueva wrap up", "the updated wrap-up").
NAMED_BEFORE = re.compile(
    r"\b(skills?|la|el|los|las|un|una|mi|tu|su|este|esta|esa|ese|"
    r"nuevo|nueva|the|a|an|my|your|its|this|that|new|de|del)\s+(\S+\s+)?$",
    re.IGNORECASE,
)


def wrap_up_invoked(text: str) -> bool:
    return any(
        not NAMED_BEFORE.search(text[max(0, m.start() - 30):m.start()])
        for m in WRAP_UP.finditer(text)
    )

# Spans that carry someone else's words: fenced and inline code, double
# quotes (straight, curly, guillemets) and markdown blockquote lines.
QUOTED_SPANS = [
    re.compile(r"```.*?```", re.DOTALL),
    re.compile(r"`[^`\n]*`"),
    re.compile(r'"[^"\n]*"'),
    re.compile(r"“[^”\n]*”"),
    re.compile(r"«[^»\n]*»"),
    re.compile(r"^[ \t]*>.*$", re.MULTILINE),
]

# In a long message, only the opening and the closing stretch count as the
# user's own words about what they are doing now.
SHORT_PROMPT = 400
HEAD_TAIL = 200


def searchable_text(prompt: str) -> str:
    for span in QUOTED_SPANS:
        prompt = span.sub(" ", prompt)
    if len(prompt) <= SHORT_PROMPT:
        return prompt
    # The double newline stops a pattern's .{0,20} gap from bridging the
    # seam ('.' does not match a newline here).
    return prompt[:HEAD_TAIL] + "\n\n" + prompt[-HEAD_TAIL:]

NUDGE = (
    "The user is about to archive or close this chat. Invoke the `wrap-up` "
    "skill now, before answering anything else, so session memory, project "
    "learnings, the Obsidian vault and any knowledge graph are brought up to "
    "date. If the message turns out not to be about closing the chat, ignore "
    "this note."
)


def main() -> int:
    # Claude Code sends UTF-8; on Windows the default stdin codec is not.
    # Without this, "sesión" arrives mangled and never matches.
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    prompt = str(data.get("prompt", ""))
    # A skill invocation is already the explicit form; do not double-trigger.
    if prompt.lstrip().startswith("/"):
        return 0
    text = searchable_text(prompt)
    if any(re.search(p, text, re.IGNORECASE) for p in PATTERNS) or wrap_up_invoked(text):
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": NUDGE,
            }
        }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
