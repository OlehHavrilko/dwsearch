#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
Usage:
  ./run.sh
  ./run.sh web
  ./run.sh tor-log

Commands:
  (default)     Run the web UI on http://127.0.0.1:50001
  web           Run the web UI on http://127.0.0.1:50001
  tor-log       Tail Tor log (/tmp/tor-dwsearch.log)

Tor:
  If 127.0.0.1:9050 is not listening, Tor is started automatically using torrc.dwsearch
EOF
}

port_open() {
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

ensure_tor() {
  if port_open; then
    return 0
  fi
  echo "[+] Starting Tor (SOCKS 9050 / Control 9051) ..."
  mkdir -p /tmp/tor-dwsearch
  tor -f "$HERE/torrc.dwsearch" >/tmp/tor-dwsearch.log 2>&1 &
  tor_pid="$!"
  started_tor=1
  for _ in $(seq 1 80); do
    if port_open; then return 0; fi
    sleep 0.25
  done
  echo "[!] Tor did not open 127.0.0.1:9050 in time. Check /tmp/tor-dwsearch.log" >&2
  return 1
}

cmd="${1:-web}"
shift || true

case "$cmd" in
  web)
    ensure_tor
    echo "[+] Dwsearch web: http://127.0.0.1:50001"
    exec "$HERE/.venv/bin/python" -m dwsearch_web "$@"
    ;;
  tor-log)
    tail -f /tmp/tor-dwsearch.log
    ;;
  -h|--help|"")
    usage
    exit 0
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    usage >&2
    exit 2
    ;;
esac
