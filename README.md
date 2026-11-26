# Global Money Flow Intelligence (GMF OS)

An open-source research workspace for macro conditions, liquidity, institutional positioning, crypto markets, cross-asset rotation hypotheses, and risk monitoring.

## Current status

**Phase 0 foundation is in progress.** The repository currently contains a Streamlit dashboard shell, YAML source and asset registries, Python dependencies, and a public Binance ticker adapter. Other modules are roadmap items until their data pipelines and calculations are implemented and tested.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

No API key is needed for the currently implemented Binance public ticker. FRED integration will require a free API key supplied through local environment or deployment secrets when implemented. Never commit credentials.

## Data integrity rules

- Label observations as reported, estimated, or inferred.
- Preserve source, units, observation/release time, retrieval time, frequency, method, and quality status.
- Never treat price changes, correlation, market-cap changes, or dominance changes alone as proof of capital moving between assets.
- Show unavailable or stale data as unavailable or stale; do not generate placeholder market values.
- Public feeds have different publication schedules and are not all real-time.

## Planned research modules

1. Global Money Map
2. Macro Intelligence
3. Institutional Flows
4. Crypto Intelligence
5. Asset Rotation
6. Risk Intelligence
7. AI Research Analyst
8. Alerts and Reports

See [Architecture](docs/ARCHITECTURE.md), [Data Policy](docs/DATA_POLICY.md), and [Roadmap](docs/ROADMAP.md).

## Stack

Python · Streamlit · Pandas · Plotly · SQLite (planned) · GitHub Actions (planned)

## Disclaimer

GMF OS is a research and analytical tool, not investment advice. Verify source definitions, timestamps, and methodology before making decisions.
