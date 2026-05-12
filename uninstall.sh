#!/usr/bin/env bash
# uninstall.sh — removes dwsearch launchers installed by install.sh

set -e

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
RESET="\033[0m"

info()  { echo -e "${BOLD}${GREEN}[+]${RESET} $*"; }
warn()  { echo -e "${BOLD}${YELLOW}[!]${RESET} $*"; }
error() { echo -e "${BOLD}${RED}[x]${RESET} $*" >&2; }

LAUNCHERS=(
    "/usr/local/bin/dwsearch"
    "/usr/local/bin/dwsearch-cli"
    "$HOME/.local/bin/dwsearch"
    "$HOME/.local/bin/dwsearch-cli"
)

removed=0
for f in "${LAUNCHERS[@]}"; do
    if [ -f "$f" ]; then
        if [ -w "$f" ]; then
            rm "$f"
        else
            sudo rm "$f"
        fi
        info "Removed: $f"
        removed=$((removed + 1))
    fi
done

if [ "$removed" -eq 0 ]; then
    warn "No Dwsearch launchers found — nothing to remove."
else
    info "Uninstall complete."
fi
