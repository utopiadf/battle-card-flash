# Battle Card Flash

## Product Overview

Battle Card Flash is a cross-platform desktop application (PC / iOS / Android) that generates PowerPoint comparison reports — "battle cards" — for **TiDB** against other databases, tailored by industry vertical.

### What It Does

1. User selects a target database to compare against TiDB
2. User picks an industry vertical (AI, Gaming, eCommerce, etc.)
3. User customizes which features to compare and selects an AI model
4. The app generates a PPT report with feature comparison tables, case studies, and LLM-powered analysis

### Supported Databases

TiDB (default baseline), MySQL, PostgreSQL, CockroachDB, Amazon Aurora, Google Spanner, MongoDB, PlanetScale, SingleStore, OceanBase

### Supported Industries

| Industry | Strategy Class | Focus Areas |
|----------|---------------|-------------|
| AI | `AIAgentStrategy` | Vector search, RAG pipelines, HTAP, real-time inference |
| Gaming | `GamingStrategy` | Low latency, high throughput, global distribution, failover |
| eCommerce | `ECommerceStrategy` | ACID transactions, flash sale scaling, MySQL compat, HTAP |
| Fintech | `FinancialServicesStrategy` | Strong consistency, RPO=0, encryption, compliance |
| SaaS | `SaaSMultiTenantStrategy` | Elastic scaling, tenant isolation, managed service, cost |
| Retail | `RetailStrategy` | Real-time inventory, POS, omnichannel analytics |

### Supported LLM Providers

| Provider | Env Variable | Model | API |
|----------|-------------|-------|-----|
| **Qwen** (default) | `DASHSCOPE_API_KEY` | qwen3.5-plus | DashScope OpenAI-compatible |
| ChatGPT | `OPENAI_API_KEY` | gpt-4o | OpenAI |
| Claude | `ANTHROPIC_API_KEY` | claude-sonnet-4-20250514 | Anthropic SDK |
| Gemini | `GEMINI_API_KEY` | gemini-2.0-flash | Google OpenAI-compatible |
| DeepSeek | `DEEPSEEK_API_KEY` | deepseek-chat | DeepSeek OpenAI-compatible |

---

## Quick Start

### Prerequisites

- Python 3.9+
- pip

### Install & Run

```bash
pip install -r requirements.txt

# Set at least one LLM API key (Qwen is the default)
export DASHSCOPE_API_KEY="your-key-here"

python main.py
```

The app works without an API key — LLM analysis will show "unavailable" but the rest of the report generates normally.

---

## Architecture

### Project Structure

```
CardGen/
├── main.py                          # Entry point → BattleCardApp
├── models/
│   └── entities.py                  # 8 dataclasses (Product, Industry, Feature, etc.)
├── db/
│   ├── schema.py                    # SQLite schema (7 tables), auto-seeds on first run
│   └── repository.py                # AbstractRepository → SQLiteRepository
├── services/
│   ├── comparison_service.py        # Orchestrates comparison workflow
│   ├── industry_strategy.py         # 8 industry strategies (Strategy pattern)
│   ├── llm_service.py               # 5 LLM providers (Strategy + Factory)
│   └── ppt_generator.py             # Slide builders (Builder + Factory)
├── ui/
│   ├── app.py                       # AppState (Observer), BattleCardApp (routing)
│   ├── step1_select_db.py           # Step 1: Select target database
│   ├── step2_select_industry.py     # Step 2: Select industry
│   ├── step3_features.py            # Step 3: Customize features + pick LLM
│   └── step4_generate.py            # Step 4: Generate PPT
├── seed_data.sql                    # Initial products, industries, features, mappings
├── BattleCardFlashTmp.pptx          # PPT template
├── requirements.txt                 # flet, python-pptx, anthropic, openai
└── output/                          # Generated PPT files
```

### Design Patterns

| Pattern | Where | Purpose |
|---------|-------|---------|
| **Repository** | `db/repository.py` | `AbstractRepository` → `SQLiteRepository` — swap to TiDB without touching services |
| **Strategy** | `services/industry_strategy.py`, `services/llm_service.py` | Per-industry comparison logic; per-provider LLM calls |
| **Factory** | `RepositoryFactory`, `StrategyFactory`, `LLMProviderFactory`, `PPTGeneratorFactory` | Centralized object creation |
| **Observer** | `ui/app.py` → `AppState` | Shared wizard state with listener callbacks |
| **Builder** | `services/ppt_generator.py` | `SlideBuilder` ABC → `FeatureTableSlideBuilder`, `CaseStudySlideBuilder`, `LLMSuggestionSlideBuilder` |

### Data Flow

```
User Input → AppState (Observer)
                ↓
         ComparisonService
           ├── Repository.get_*()        → feature values, expert advice, case studies
           └── builds ComparisonResult
                ↓
         LLMService.generate_comparison_summary()
           ├── StrategyFactory → industry-specific LLM prompt
           └── LLMProviderFactory → provider.call(prompt)
                ↓
         PPTGenerator.generate()
           ├── Clone template slides
           ├── FeatureTableSlideBuilder   → comparison table
           ├── CaseStudySlideBuilder      → customer stories
           └── LLMSuggestionSlideBuilder  → AI analysis + expert quotes
                ↓
         output/*.pptx
```

---

## Wizard Flow (4 Steps)

1. **Select Database** (`/step1`) — Dropdown of all non-default products. TiDB is always the baseline.
2. **Select Industry** (`/step2`) — Card grid of 6 industries with icons and descriptions.
3. **Customize Features** (`/step3`) — Checkboxes for industry-mapped features (pre-checked), dropdown to add extra features, LLM provider selector.
4. **Generate** (`/step4`) — Background thread runs: build comparison → LLM summary → PPT generation. Progress bar with status updates. Result shows file path + "Open File" / "New Comparison" buttons.

---

## How to Extend

### Add a New Database

1. Add an `INSERT` to `seed_data.sql` in the `products` table
2. Add `product_features` rows for the new product (all 27 features)
3. Optionally add `expert_advice` entries for relevant industry matchups
4. Delete `battlecard.db` and restart to re-seed

### Add a New Industry

1. Add an `INSERT` to `seed_data.sql` in the `industries` table (with `icon_name` from Flet Icons)
2. Add `industry_features` mappings with weights
3. Create a new strategy class in `services/industry_strategy.py` extending `ComparisonStrategy`
4. Register it in `StrategyFactory._registry`
5. Add the icon mapping in `ui/step2_select_industry.py` → `_ICON_MAP`

### Add a New LLM Provider

1. Create a new class in `services/llm_service.py` extending `LLMProvider`
2. Implement the `call(prompt) -> str` method
3. Register in `LLMProviderFactory._registry` and `ENV_KEYS`

### Add a New Slide Type

1. Create a new class in `services/ppt_generator.py` extending `SlideBuilder`
2. Implement `build(slide, result)` method
3. Add it to `PPTGeneratorFactory.create_builders()` list

---

## Configuration

### Environment Variables

| Variable | Provider | Required |
|----------|----------|----------|
| `DASHSCOPE_API_KEY` | Qwen (default) | For AI analysis |
| `OPENAI_API_KEY` | ChatGPT | If selected |
| `ANTHROPIC_API_KEY` | Claude | If selected |
| `GEMINI_API_KEY` | Gemini | If selected |
| `DEEPSEEK_API_KEY` | DeepSeek | If selected |

### Database

- SQLite at `battlecard.db` (auto-created on first run)
- Schema defined in `db/schema.py`, seed data in `seed_data.sql`
- To reset: delete `battlecard.db` and restart

### PPT Template

- `BattleCardFlashTmp.pptx` in project root
- Slide 0: Title page, Slide 1: Content template (cloned per section), Last slide: Thanks page

---

## Flet 0.28.x Notes

- Use `ft.Icons.X` (capitalized enum), not `ft.icons.x`
- Use enum values (`ft.MainAxisAlignment.CENTER`), not strings
- `TextField.value` must be `str`
- Navigation via `page.views`, `page.on_route_change`, `page.go()`

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `No module named 'openai'` | `openai` package not installed in the Python env Flet uses | `pip install openai` in the correct environment |
| `The read operation timed out` | LLM API response took too long | Increase timeout in `llm_service.py` (currently 120s) |
| `LLM analysis unavailable` | API key env var not set | `export DASHSCOPE_API_KEY=...` before running |
| Database not seeding | `battlecard.db` already exists | Delete `battlecard.db` and restart |
| PPT template error | `BattleCardFlashTmp.pptx` missing | Ensure the template file is in the project root |
