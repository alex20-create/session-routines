#!/usr/bin/env bash
set -eu
cp -R "$(dirname "$0")/files/." .
git init -q
git checkout -q -b main 2>/dev/null || true
git -c user.name=dev -c user.email=dev@example.com add -A
git -c user.name=dev -c user.email=dev@example.com commit -q -m "chore: set up directing"
git switch -q -c b2-payment-form
echo "form" > form.txt
git -c user.name=dev -c user.email=dev@example.com add form.txt
git -c user.name=dev -c user.email=dev@example.com commit -q -m "feat: start the payment form"
git switch -q main
