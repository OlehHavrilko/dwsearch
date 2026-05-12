#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

port_open() {
  # /dev/tcp works in bash. If it fails, return non-zero.
  (exec 3<>"/dev/tcp/127.0.0.1/9050") >/dev/null 2>&1
}

# Start Tor (local config) if SOCKS port is not listening.
if ! port_open; then
  echo "[+] Starting Tor (SOCKS 9050 / Control 9051) ..."
  "$HERE/start-tor.sh" >/tmp/tor-darkdump.log 2>&1 &
  for _ in $(seq 1 80); do
    if port_open; then break; fi
    sleep 0.25
  done
fi

echo "[+] Darkdump web: http://127.0.0.1:50001/?engine=tordex&proxy=1"
exec "$HERE/.venv/bin/python" "$HERE/darkdump-web/app.py"
