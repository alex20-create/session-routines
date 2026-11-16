#!/usr/bin/env bash
set -eu
cp -R "$(dirname "$0")/files/." .
git init -q
git checkout -q -b main 2>/dev/null || true
c() { git -c user.name=dev -c user.email=dev@example.com "$@"; }
c add DIRECTING.md BRIEFS.md STATUS.md
c commit -q -m "chore: set up directing"
echo "level one" > level1.txt
c add level1.txt
c commit -q -m "feat: build level one"
echo "level two" > level2.txt
c add level2.txt LOG.md
c commit -q -m "feat: build level two"
