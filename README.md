# Global Money Flow Intelligence (GMF OS)

An open-source research workspace for macro conditions, liquidity, institutional positioning, crypto markets, cross-asset rotation hypotheses, and risk monitoring.

## Current status

**Phase 0 foundation is complete. Phase 1 data-layer implementation is underway.** The application includes a Streamlit dashboard, public Binance ticker view, configurable public-source adapters, observation validation, SQLite persistence, and an FRED ingestion workflow. The CI suite currently passes 7 tests. Provider adapters are not all runtime-verified; see [Verification Log](docs/VERIFICATION_LOG.md).

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

No API key is needed for the Binance public ticker or DefiLlama public stablecoin overview. FRED requires a free API key set as `FRED_API_KEY` in the environment or Streamlit secrets. Never commit credentials.

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

See [Architecture](docs/ARCHITECTURE.md), [Data Policy](docs/DATA_POLICY.md), [Phase 1 Data Layer](docs/PHASE1_DATA_LAYER.md), [Verification Log](docs/VERIFICATION_LOG.md), and [Roadmap](docs/ROADMAP.md).

## Stack

Python · Streamlit · Pandas · Plotly · SQLite · GitHub Actions

## Disclaimer

GMF OS is a research and analytical tool, not investment advice. Verify source definitions, timestamps, and methodology before making decisions.
