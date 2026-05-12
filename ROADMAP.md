# dwsearch — Roadmap

Goal: максимально практичный инструмент для поиска/агрегации результатов из **нецензурных** (unfiltered) движков + удобный CLI/Web, быстрый локальный запуск, стабильная работа через Tor.

Принцип: никаких “safety-gate” и ограничений по движкам — упор на функциональность и контроль со стороны пользователя.

---

## Phase 0 — Clean Baseline (now)

- Единая точка входа `./run.sh` (web/cli) + автозапуск Tor через `torrc.dwsearch`.
- Удаление мусора из репо (`__pycache__`, окружения) через `.gitignore`.

Done/keeping stable: чтобы дальнейшие изменения не ломали запуск “из коробки”.

---

## Phase 1 — Project Packaging (1–2 days)

Цель: нормальная структура проекта и удобный запуск без “магии”.

- Разнести код в пакет `dwsearch/` (модули: engines, http, scrape, export, utils).
- Сделать запуск `python -m dwsearch` и консольную команду `dwsearch` (entrypoint).
- Переименовать/структурировать `dwsearch-web` как модуль `dwsearch_web/`.
- Унифицировать конфиги/пути: один “root locator”, никаких хардкодов имён файлов.
- Добавить `pyproject.toml` (минимально) и оставить `requirements.txt` как вариант.

Deliverables:
- `dwsearch` как пакет
- простая установка/запуск без привязки к текущей папке

---

## Phase 2 — Config + Profiles (2–3 days)

Цель: управляемость поведения без правок кода.

- Конфиг файл `dwsearch.yml` (или `config.toml`) с настройками:
  - proxy/Tor (socks host/port), timeouts, retries, concurrency
  - user-agent, headers presets
  - лимиты по результатам, дедуп, формат экспорта
- Профили:
  - `uncensored` (по умолчанию)
  - `fast` (меньше проверок/скрапа)
  - `deep` (скрап + изображения + расширенный парсинг)
- CLI флаги всегда имеют приоритет над конфигом.

Deliverables:
- `dwsearch --config ... --profile ...`
- предсказуемые дефолты

---

## Phase 3 — Engine Layer v2 (3–6 days)

Цель: добавить движки/источники без переписывания ядра.

- Единый интерфейс движка (Engine API): `search(query, amount, proxy, ...) -> results`.
- Реестр движков + авто-дискавери (простая “плагинность”):
  - встроенные движки
  - кастомные движки из папки `engines.d/` (optional)
- Стандартизировать результат:
  - `id`, `engine`, `url`, `title`, `snippet`, `timestamp`, `score?`, `raw?`
- Улучшить устойчивость парсеров:
  - нормальные таймауты
  - retries/backoff
  - fallback парсинг (например, если HTML меняется)

Deliverables:
- движки как модули, легко добавлять новые
- стабильный формат результата для Web/CLI/экспорта

Status: started — added `dwsearch/engines.py` as a minimal typed engine layer wrapper.

---

## Phase 4 — Networking + Tor Reliability (2–4 days)

Цель: максимально стабильная работа через Tor.

- Проверка готовности Tor “по делу”:
  - SOCKS доступен
  - (опционально) проверка IP/exit через внешний чекер
- Отдельные настройки сетевого слоя:
  - connection pool
  - retries/backoff per engine
  - ограничение параллелизма per domain/engine
- Логи Tor в отдельный файл + удобная команда:
  - `./run.sh tor-log` (tail)
  - `./run.sh tor-restart` (optional)

Deliverables:
- меньше “подвисаний” и необъяснимых падений
- удобная диагностика

Status: started — added config-driven retry/backoff primitives and `./run.sh tor-log`.

---

## Phase 5 — Storage / Cache / Sessions (3–5 days)

Цель: повторяемость, скорость, история.

- Кэш запросов/ответов (sqlite):
  - `query + engine + params -> results/raw`
  - TTL + принудительный refresh
- Сессии запуска:
  - `run_id`, время, параметры, статистика
  - экспорт “bundle” (zip) с JSONL + логами
- JSONL как основной формат для больших объёмов.

Deliverables:
- `--cache on/off`, `--cache-ttl`, `--session-dir`
- история и реплей результатов

---

## Phase 6 — Scrape / Enrich Pipeline (4–8 days)

Цель: сделать результаты “богаче”, но управляемо.

- Пайплайн этапов:
  1) search
  2) normalize/dedup
  3) scrape (optional)
  4) enrich (emails/metadata/files)
  5) export
- Дедуп:
  - по URL canonicalization
  - по (title+snippet) как fallback
- Скрейп:
  - выделение email/phones/links
  - метаданные документов (если скачиваются)
  - опционально сбор изображений

Deliverables:
- `--scrape`, `--images`, `--enrich`
- предсказуемая скорость (лимиты/параллельность)

---

## Phase 7 — Web UI Upgrade (4–7 days)

Цель: удобная работа в браузере без боли.

- История запросов и результатов (из sqlite sessions).
- Прогресс + отмена задачи.
- Фильтры/сортировка/дедуп в UI.
- Presets (“one click”):
  - `TorDex + proxy`
  - наборы движков
- Экспорт из UI: json/csv/jsonl/zip bundle.

Deliverables:
- web интерфейс как “рабочая станция”

---

## Phase 8 — Distribution (2–5 days)

Цель: легко ставить и запускать где угодно.

- Docker образ (опционально) с Tor внутри и пробросом портов.
- “One-liner” installer (обновить `install.sh`) под `dwsearch`:
  - ставит `dwsearch` и `dwsearch-web`
- Документация под WSL2/Ubuntu/Termux proot (реальные команды).

Deliverables:
- `docker run ...` / install script / понятная дока

---

## Phase 9 — Quality / CI (ongoing)

Цель: не ломать работающее.

- Тесты:
  - дедуп, нормализация, экспорт
  - минимальные smoke-тесты движков (без реального интернета, через фикстуры)
- Линт/формат:
  - `ruff` + `black` (или только `ruff format`)
- CI workflow:
  - unit tests + lint
  - build package

Deliverables:
- стабильные релизы, меньше регрессий

---

## Backlog — Ideas (optional)

- Multi-engine search одним запросом (параллельно по движкам) + merge/dedup.
- “Focus mode”: поиск по списку ключевых слов/доменов пакетно (batch).
- Export templates: готовые отчёты (md/html) для OSINT-репорта.
- “Artifacts”: сохранение сырого HTML ответа движка для дебага.
- Rate-limit profiles per engine (у некоторых движков более жёсткие ограничения).
- Простая система “blocks/allowlists” для доменов/оніонів (это не safety, а фильтрация по задаче).
