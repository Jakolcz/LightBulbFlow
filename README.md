# LightBulbFlow (WIP)

Minimal starter for a pipeline that:

- Scrapes idea/product discussions from various sources.
- Stores items (default SQLite; can expand later).
- Sends saved items to an LLM (local via Ollama or external via Gemini) for quick assessment.
- Saves the LLM output for later review and optional export.

## Status

Early work-in-progress. Interfaces, commands, and modules are not finalized yet.

## Planned MVP flow

1) Scrape selected sources.
2) Normalize to a simple Idea schema.
3) Persist to the database.
4) Run analysis via an LLM adapter (Ollama or Gemini).
5) Store analysis results; optionally export.

## Tech

- Python (>=3.13), Poetry for dependency management.
- SQLite for initial storage.
- LLMs: Ollama (local) or Gemini (Google API).
