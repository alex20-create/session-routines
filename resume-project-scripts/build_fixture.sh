#!/usr/bin/env bash
# Build one test fixture for the resume-project evals in
# resume-project/evals. This script lives in scripts/.
# Usage: build_fixture.sh <case-name> <target-dir>
# Layout: <target>/remote.git (bare "origin"), <target>/colleague (another clone
# used to move the remote after the local state is set), <target>/project (the
# session's repository) and, for worktree cases, <target>/project-wt.
set -eu
CASE="$1"; T="$2"
rm -rf "$T"; mkdir -p "$T"; cd "$T"
g(){ git -c core.autocrlf=false -c user.name="Test User" -c user.email=test@example.test -c init.defaultBranch=main -c advice.detachedHead=false "$@"; }

g init -q --bare -b main remote.git
g clone -q remote.git project 2>/dev/null
cd project
echo "base" > f.txt
g add f.txt; g commit -qm "feat: base"; g push -q -u origin main 2>/dev/null
cd "$T"; g clone -q remote.git colleague 2>/dev/null

case "$CASE" in
merge-behind-remote)
  # Local main: one unpushed commit with an old plan.
  cd "$T/project"
  mkdir -p docs/plans
  printf '# Plan phase 2 (first draft)\n' > docs/plans/2026-11-01-phase-2.md
  g add docs; g commit -qm "docs: add the phase 2 plan"
  # Colleague: phase 5 lands with a rewritten plan and a CLAUDE.md saying "not merged".
  cd "$T/colleague"
  mkdir -p docs/plans
  printf '# Plan phase 2 (rewritten)\n' > docs/plans/2026-11-03-phase-2.md
  printf '# CLAUDE.md\n\n## Current state\n\n- Phase 5: home screen, on PR #13, not yet merged.\n\n## Pending\n\n- Merge PR #13.\n- User checks phase 5 on a phone.\n' > CLAUDE.md
  echo "phase 5" > home.txt
  g add .; g commit -qm "feat: phase 5 home screen (#13)"; g push -q 2>/dev/null
  # Local: start a pull that stops before committing (merge in progress, no conflicts).
  cd "$T/project"
  g fetch -q
  g merge -q --no-ff --no-commit origin/main >/dev/null 2>&1 || true
  # Colleague: after the local merge started, the remote moves on.
  cd "$T/colleague"
  printf '# CLAUDE.md\n\n## Current state\n\n- Phase 5: home screen, merged into main (PR #13).\n\n## Pending\n\n- User checks phase 5 on a phone.\n- Before deploy: fix the dark first-paint flash.\n' > CLAUDE.md
  g commit -qam "docs: record phase 5 as merged (#14)"; g push -q 2>/dev/null
  ;;
worktree-rebase-conflict)
  cd "$T/project"
  g switch -q -c topic
  echo "topic version" > f.txt; g commit -qam "feat: topic change"; g push -q -u origin topic 2>/dev/null
  g switch -q main
  cd "$T/colleague"
  g pull -q 2>/dev/null
  echo "main version" > f.txt; g commit -qam "feat: main change"; g push -q 2>/dev/null
  cd "$T/project"
  g fetch -q
  g worktree add -q ../project-wt topic 2>/dev/null
  cd "$T/project-wt"
  g rebase origin/main >/dev/null 2>&1 || true
  # After the rebase started: a colleague pushes to topic and to main.
  cd "$T/colleague"
  g fetch -q; g switch -q -c topic origin/topic 2>/dev/null
  echo "more" > extra.txt; g add extra.txt; g commit -qm "feat: colleague adds to topic"; g push -q 2>/dev/null
  g switch -q main; echo "later" > later.txt; g add later.txt; g commit -qm "feat: later main change"; g push -q 2>/dev/null
  ;;
fetch-fails-worktree)
  cd "$T/project"
  g switch -q -c feat/x
  echo "x" > x.txt; g add x.txt; g commit -qm "feat: x"; g push -q -u origin feat/x 2>/dev/null
  echo "x2" >> x.txt; g commit -qam "feat: x, part two (not pushed)"
  g switch -q main
  g worktree add -q ../project-wt feat/x 2>/dev/null
  g fetch -q
  touch -d "2026-10-20 10:00:00" "$(git rev-parse --git-common-dir)/FETCH_HEAD"
  g remote set-url origin https://invalid.invalid/example-test.git
  ;;
squash-and-gone)
  cd "$T/project"
  g switch -q -c feat/sq
  echo "sq" > sq.txt; g add sq.txt; g commit -qm "feat: squash me"; g push -q -u origin feat/sq 2>/dev/null
  g switch -q main
  g switch -q -c feat/other
  echo "o" > o.txt; g add o.txt; g commit -qm "feat: other"; g push -q -u origin feat/other 2>/dev/null
  g switch -q main
  # Remote: feat/sq lands as a squash commit; feat/other is deleted without merging.
  cd "$T/colleague"
  g fetch -q
  g merge -q --squash origin/feat/sq >/dev/null 2>&1; g commit -qm "feat: squash me (#21)"
  g push -q 2>/dev/null
  g push -q origin --delete feat/sq feat/other 2>/dev/null
  ;;
worktree-own-fetch-fails)
  # The last good fetch ran from the worktree, so its FETCH_HEAD is the newest.
  cd "$T/project"
  g switch -q -c feat/y
  echo "y" > y.txt; g add y.txt; g commit -qm "feat: y"; g push -q -u origin feat/y 2>/dev/null
  g switch -q main
  g worktree add -q ../project-wt feat/y 2>/dev/null
  g fetch -q
  touch -d "2026-10-01 09:00:00" "$(git rev-parse --git-common-dir)/FETCH_HEAD"
  cd "$T/project-wt"
  g fetch -q
  touch -d "2026-10-25 18:30:00" "$(git rev-parse --git-dir)/FETCH_HEAD"
  echo "y2" >> y.txt; g commit -qam "feat: y, part two (not pushed)"
  g remote set-url origin https://invalid.invalid/example-test.git
  ;;
rebase-apply-detached)
  # An apply-style rebase started on a detached HEAD, stopped on a conflict.
  cd "$T/project"
  g switch -q -c topic
  echo "topic version" > f.txt; g commit -qam "feat: topic change"; g push -q -u origin topic 2>/dev/null
  g switch -q main
  cd "$T/colleague"
  g pull -q 2>/dev/null
  echo "main version" > f.txt; g commit -qam "feat: main change"; g push -q 2>/dev/null
  cd "$T/project"
  g fetch -q
  g switch -q --detach topic
  g rebase --apply origin/main >/dev/null 2>&1 || true
  cd "$T/colleague"
  echo "later" > later.txt; g add later.txt; g commit -qm "feat: later main change"; g push -q 2>/dev/null
  ;;
cherry-pick-conflict)
  # A cherry-pick of a hotfix onto main stopped on a conflict; meanwhile the
  # remote main received the same fix.
  cd "$T/colleague"
  g switch -q -c hotfix
  echo "fixed" > f.txt; g commit -qam "fix: correct the base line"; g push -q -u origin hotfix 2>/dev/null
  g switch -q main
  cd "$T/project"
  echo "local edit" > f.txt; g commit -qam "feat: local edit of the base line"; g push -q 2>/dev/null
  g fetch -q
  g cherry-pick origin/hotfix >/dev/null 2>&1 || true
  cd "$T/colleague"
  g pull -q --no-rebase 2>/dev/null || true
  echo "fixed" > f.txt; g commit -qam "fix: correct the base line (#30)"; g push -q 2>/dev/null
  ;;
*) echo "unknown case $CASE" >&2; exit 1 ;;
esac
echo "built $CASE in $T"
