# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Battle Card Flash — a cross-platform (PC/iOS/Android) database product comparison tool built with Python and Flet. Compares TiDB against other databases under user-selected industries, generating PPT reports with feature comparisons and LLM-generated analysis.

## Running the App

```bash
pip install -r requirements.txt
python main.py
```

Set `ANTHROPIC_API_KEY` environment variable to enable AI-generated comparison summaries (optional — app works without it).

## Architecture

- `main.py` — Entry point, delegates to `BattleCardApp`
- `models/entities.py` — Dataclasses (Product, Industry, Feature, ComparisonResult, etc.)
- `db/schema.py` — SQLite schema definition and initialization
- `db/repository.py` — Repository pattern: `AbstractRepository` ABC with `SQLiteRepository` implementation, `RepositoryFactory`
- `services/industry_strategy.py` — Strategy pattern: per-industry comparison logic (`AIAgentStrategy`, `GamingStrategy`, etc.) with `StrategyFactory`
- `services/comparison_service.py` — Orchestrates comparison: fetches data via Repository, builds `ComparisonResult`
- `services/llm_service.py` — Claude API wrapper for generating comparison summaries
- `services/ppt_generator.py` — Factory/Builder pattern: `SlideBuilder` ABC with `TitleSlideBuilder`, `FeatureTableSlideBuilder`, `LLMSuggestionSlideBuilder`
- `ui/app.py` — `AppState` (Observer pattern), `BattleCardApp` (routing), 4-step wizard flow
- `ui/step1_select_db.py` through `ui/step4_generate.py` — Flet views for each wizard step
- `seed_data.sql` — Initial products, industries, features, mappings, and expert advice

## Design Patterns

- **Repository**: `AbstractRepository` → `SQLiteRepository` (swap to TiDB without touching services)
- **Strategy**: `ComparisonStrategy` → per-industry classes (different feature priorities and LLM prompts)
- **Factory**: `RepositoryFactory`, `StrategyFactory`, `PPTGeneratorFactory`
- **Observer**: `AppState` with listener callbacks for shared wizard state

## Flet 0.28.x Notes

- Use `ft.Icons.X` (capitalized), not `ft.icons.x`
- Use enum values (`ft.MainAxisAlignment.CENTER`), not strings
- `TextField.value` must be `str`
- Navigation via `page.views`, `page.on_route_change`, `page.go()`

