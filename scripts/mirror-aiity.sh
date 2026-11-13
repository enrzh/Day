#!/usr/bin/env bash
# Copies this site to https://aiity.de/day/ (the IONOS VPS Caddy serves /root/apps_edge_vps/caddy/sites/aiity as aiity.de).
# Day's What's New opens GitHub Pages first, or this copy first on devices in mainland China, and falls back to the other.
# Run it after the site changes (after `python3 scripts/changelog.py`): `scripts/mirror-aiity.sh` (add --dry-run to look).
# Only /day/ on the VPS is written, and --delete only works inside it. Caddy needs no restart: it serves the files as they are.
set -euo pipefail
cd "$(dirname "$0")/.."
DEST="vps:/root/apps_edge_vps/caddy/sites/aiity/day/"
EXTRA=("$@")
rsync -rlt --delete \
  --exclude '.git' --exclude '.github' --exclude 'scripts' --exclude '*.md' --exclude '.DS_Store' --exclude '.nojekyll' \
  ${EXTRA[@]+"${EXTRA[@]}"} ./ "$DEST"
if [[ " ${EXTRA[*]:-} " != *" --dry-run "* && " ${EXTRA[*]:-} " != *" -n "* ]]; then
  # Readable by the web server whatever this Mac's umask was.
  ssh vps 'chmod -R a+rX /root/apps_edge_vps/caddy/sites/aiity/day'
  for path in changelog/ changelog/ja/ changelog/zh-Hans/ ""; do
    printf '%s  ' "https://aiity.de/day/$path"; curl -s -o /dev/null -m 15 -w '%{http_code}\n' "https://aiity.de/day/$path"
  done
fi
