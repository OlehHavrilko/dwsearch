# dwsearch

<p align="center">
  <img alt="dwsearch" src="imgs/dwsearch_example.png" width="860">
</p>

<p align="center">
  <a href="https://github.com/OlehHavrilko/dwsearch/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/OlehHavrilko/dwsearch/ci.yml?branch=main"></a>
  <a href="https://github.com/OlehHavrilko/dwsearch/releases"><img alt="Release" src="https://img.shields.io/github/v/release/OlehHavrilko/dwsearch?display_name=tag&sort=semver"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/OlehHavrilko/dwsearch"></a>
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-blue"></a>
  <a href="https://github.com/OlehHavrilko/dwsearch/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/OlehHavrilko/dwsearch?style=flat"></a>
</p>

## About

`dwsearch` is a practical fork of **Dwsearch**: an OSINT tool for deep web investigation.

It can:
- Search multiple dark-web engines
- Stream results live to a local web UI or CLI
- Optionally deep-scrape result pages (emails, metadata, links, docs, images)
- Always filter results against Ahmia's public abuse blacklist (regardless of engine)

This fork focuses on fast local setup (WSL2 / Ubuntu / Termux proot Ubuntu) and a one-command web launch with Tor auto-start.

Author / maintainer of this fork: **Oleh Havrilko**.

## Quick Start (Recommended)

### 1) Clone + deps

```bash
git clone https://github.com/OlehHavrilko/dwsearch.git
cd dwsearch
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
pip install -r requirements.txt
```

### 2) Web launch with Tor

```bash
dwsearch
```

Open `http://127.0.0.1:50001`

### 3) Config profiles (Phase 2)

```bash
cp dwsearch.example.toml dwsearch.toml
```

```bash
dwsearch --config dwsearch.toml --profile fast
```

```bash
dwsearch --config dwsearch.toml --profile deep
```

## Tor Setup

### Option A: Local Tor for this repo (no systemd)

This repo includes a minimal Tor config:
- `torrc.dwsearch` (SOCKS `127.0.0.1:9050`, ControlPort `127.0.0.1:9051`)
Tor is auto-started by `./run.sh` when needed.

### Option B: System Tor

Ubuntu:

```bash
sudo apt update
sudo apt install tor
```

## Search Engines

Engines available via `-e` / `--engine`:

| Engine       | Filtered | Requires Tor | Notes                                          |
|--------------|----------|--------------|------------------------------------------------|
| `ahmia`      | Yes      | No           | Default. Tor Project-endorsed, strict filtering |
| `notevil`    | Partial  | Yes          | Ahmia fork with broader index                  |
| `tordex`     | **No**   | No (but recommended) | Unfiltered — use with caution |
| `tor66`      | **No**   | Yes          | Crawled index with directory — confirmation required |
| `onionland`  | **No**   | Yes          | Indexes Tor, I2P, and clearnet — confirmation required |
| `excavator`  | **No**   | Yes          | General dark web index — confirmation required |

All engines are filtered against Ahmia's abuse blacklist, but *unfiltered engines are still dangerous*. Use strict judgment.

## Web Interface

Includes a local browser-based interface.

```bash
dwsearch
```

Then open `http://127.0.0.1:50001`.

### Features

- Live streaming results as they arrive
- All six engines available via dropdown
- Tor proxy toggle with live exit IP display
- Deep scrape with optional image collection
- Metadata-based deduplication
- Breach intelligence scan mode
- Export results as JSON, CSV, or TXT


## Ethical Notice

This tool is intended for legitimate security research and OSINT investigations only. Do not use it for illegal activity.

## License

MIT License (upstream Dwsearch by Josh Schiavone; this repo is a fork with additional glue/scripts).
