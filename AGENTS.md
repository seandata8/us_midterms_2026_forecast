# AGENTS.md

University of Toronto data science course project: forecasting the 2026 US midterms with LLM "silicon sampling" (persona + question -> structured vote answer) via OpenRouter.

## Setup / run
- Python 3.14, managed with `uv` (`uv sync`; add deps with `uv add`). No tests, linter, or CI configured.
- Run scripts from the repo root: `uv run 00-check.py`. `silicon.py` uses `cache/` relative to the cwd, and loads `.env` by searching upward from `silicon.py`'s folder.
- Requires `OPENROUTER_API_KEY` in `.env` (gitignored). Never print or commit it. `silicon.py` raises `KeyError` on import without it.
- Running scripts makes paid API calls, so don't run them casually.

## Architecture
- `silicon.py` is the shared module for the worksheet scripts. It holds the OpenRouter client (OpenAI SDK with `base_url`), `MODELS`, the JSON `SCHEMA` (`vote` enum plus `confidence` 0-100), the `BUDGET_USD` guard, and `ask(model, persona, question, temperature, draw)`.
- Scripts like `00-check.py` do `from silicon import *`. Because of that, use `total_spent()` rather than the `spent` global, which `import *` copies once.
- `src/us_midterms_2026_forecast/` is a uv_build package stub. The `main` named in `[project.scripts]` is not implemented, so the entry point is currently unusable. The real work is in the root scripts.

## Gotchas
- `ask()` caches to `cache/<sha256>.json`, keyed on model, temperature, draw, persona and question. Any change to those creates a new, billed call. To get repeated samples for the same persona and question, vary `draw` and don't loop on identical arguments.
- Failed or unparseable answers are cached as `{"vote": None, "confidence": None}` and are not retried. Delete the cache file to retry.
- `cache/*.json` files are tracked in git (`cache/` is not in `.gitignore`).
- `BUDGET_USD` (2.00) is per process, not persistent. Cache hits are free and don't count toward it.
- `instructions/` holds course materials (worksheet/slides `.qmd`, paper, `references.bib`). It is gitignored, so treat it as the assignment spec and don't modify it.
- Model IDs in `MODELS` are OpenRouter slugs. Check they exist before changing them.
