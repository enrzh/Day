#!/bin/zsh
# Copies the built changelog pages to Day's own server (aiity.de/day/changelog/), which is reachable where GitHub Pages
# isn't (mainland China). Run after `python3 scripts/changelog.py` and pushing to GitHub. Needs the `vps` SSH host.
# Keeps a dated backup of the live copy on the server before overwriting; never deletes files there.
set -euo pipefail
cd "$(dirname "$0")/.."
target=/root/apps_edge_vps/caddy/sites/aiity/day
ssh vps "cd $target/.. && tar czf /root/day-changelog-backup-\$(date +%Y%m%d-%H%M).tgz day/changelog"
rsync -rlt changelog "vps:$target/"
curl -fsS -m 10 https://aiity.de/day/changelog/releases.json | python3 -c 'import json,sys; r=json.load(sys.stdin)["releases"]; print("aiity.de serves", len(r), "releases, newest", r[0]["id"])'
