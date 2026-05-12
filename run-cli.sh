#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

port_open() {
  # /dev/tcp works in bash. If it fails, return non-zero.
  (exec 3<>"/dev/tcp/127.0.0.1/9050") >/dev/null 2>&1
}

started_tor=0
tor_pid=""

cleanup() {
  if [[ "$started_tor" -eq 1 ]] && [[ -n "${tor_pid:-}" ]]; then
    kill "$tor_pid" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT INT TERM

# Start Tor (local config) if SOCKS port is not listening.
if ! port_open; then
  echo "[+] Starting Tor (SOCKS 9050 / Control 9051) ..."
  "$HERE/start-tor.sh" >/tmp/tor-darkdump.log 2>&1 &
  tor_pid="$!"
  started_tor=1
  for _ in $(seq 1 80); do
    if port_open; then break; fi
    sleep 0.25
  done
fi

exec "$HERE/.venv/bin/python" "$HERE/darkdump.py" "$@"
