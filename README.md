# darkwebrc

<p align="center">
  <img alt="darkwebrc" src="imgs/darkdump_example.png" width="860">
</p>

<p align="center">
  <a href="https://github.com/OlehHavrilko/darkwebrc/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/OlehHavrilko/darkwebrc/ci.yml?branch=main"></a>
  <a href="https://github.com/OlehHavrilko/darkwebrc/releases"><img alt="Release" src="https://img.shields.io/github/v/release/OlehHavrilko/darkwebrc?display_name=tag&sort=semver"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/OlehHavrilko/darkwebrc"></a>
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-blue"></a>
  <a href="https://github.com/OlehHavrilko/darkwebrc/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/OlehHavrilko/darkwebrc?style=flat"></a>
</p>

## About

`darkwebrc` is a practical fork of **Darkdump**: an OSINT tool for deep web investigation.

It can:
- Search multiple dark-web engines
- Stream results live to a local web UI or CLI
- Optionally deep-scrape result pages (emails, metadata, links, docs, images)
- Always filter results against Ahmia's public abuse blacklist (regardless of engine)

This fork focuses on fast local setup (WSL2 / Ubuntu / Termux proot Ubuntu) and a one-command *uncensored* web launch using TorDex.

Author / maintainer of this fork: **Oleh Havrilko**.

## Quick Start (Recommended)

### 1) Clone + deps

```bash
git clone https://github.com/OlehHavrilko/darkwebrc.git
cd darkwebrc
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pip install -r darkdump-web/requirements.txt
```

### 2) Uncensored web (TorDex + Tor proxy)

```bash
./run.sh web --uncensored
```

Open:

`http://127.0.0.1:50001/?engine=tordex&proxy=1`

### 3) Normal web (no preset)

```bash
./run.sh web
```

## Tor Setup

### Option A: Local Tor for this repo (no systemd)

This repo includes a minimal Tor config:
- `torrc.darkdump` (SOCKS `127.0.0.1:9050`, ControlPort `127.0.0.1:9051`)
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
| `tordex`     | **No**   | No (but recommended) | Fully uncensored — use with caution |
| `tor66`      | **No**   | Yes          | Crawled index with directory — confirmation required |
| `onionland`  | **No**   | Yes          | Indexes Tor, I2P, and clearnet — confirmation required |
| `excavator`  | **No**   | Yes          | General dark web index — confirmation required |

All engines are filtered against Ahmia's abuse blacklist, but *unfiltered engines are still dangerous*. Use strict judgment.

## CLI Usage

```
darkdump-cli [-h] [-v] [-q QUERY] [-a AMOUNT] [-e ENGINE]
             [-p] [-s] [-i] [-d] [-u] [-o FILE]
             [--breach] [--breach-deep] [--breach-delay SECONDS]
             [-y]
```

| Flag | Description |
|------|-------------|
| `-q`, `--query` | Search query |
| `-a`, `--amount` | Number of results to retrieve (default: 10) |
| `-e`, `--engine` | Engine to use (default: `ahmia`) |
| `-p`, `--proxy` | Route requests through Tor |
| `-s`, `--scrape` | Deep scrape each result for metadata, links, emails, documents |
| `-i`, `--images` | Also collect images during scrape (requires `-s`) |
| `-u`, `--unique` | Hide results with duplicate title + description |
| `-d`, `--debug` | Enable debug output |
| `-o FILE`, `--output FILE` | Save results to file — format inferred from extension (`.json`, `.csv`, `.txt`) |
| `--breach` | Run a breach / credential leak intelligence scan for the given target |
| `--breach-deep` | Combine breach scan with deep scraping of each result |
| `--breach-delay` | Seconds between breach queries to avoid rate limits (default: 1.5) |
| `-v`, `--version` | Print version |
| `-y`, `--yes` | Non-interactive: skip confirmation prompts for unfiltered engines |

### Examples

```bash
# Basic search via Ahmia (no Tor required)
darkdump-cli -q "privacy tools" -a 10

# Search and deep scrape each result via Tor
darkdump-cli -q "hacking" -a 10 -s -p

# Search, scrape, and collect images
darkdump-cli -q "marketplaces" -a 15 -s -p -i

# Use Not Evil engine, deduplicate, save to JSON
darkdump-cli -q "security research" -a 20 -e notevil -p -u -o results.json

# Use OnionLand engine, save to CSV
darkdump-cli -q "crypto" -a 10 -e onionland -p -o results.csv

# Breach intelligence scan for an email address
darkdump-cli --breach -q admin@example.com -e ahmia -p

# Breach scan with deep scraping
darkdump-cli --breach --breach-deep -q example.com -e ahmia
```

## Web Interface

Includes a local browser-based interface.

```bash
./run.sh web
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

MIT License (upstream Darkdump by Josh Schiavone; this repo is a fork with additional glue/scripts).
