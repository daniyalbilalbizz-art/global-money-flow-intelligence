# Architecture

Streamlit is the presentation layer. `engines/` contains provider adapters and calculations; `config/` stores source and asset metadata; `data/` is reserved for local persistence; `tests/` validates core contracts.

## Initial runtime
`app.py` loads YAML registries and can request a Binance public 24-hour ticker through `engines/providers.py`. Provider errors are surfaced; no synthetic market values are substituted.

## Planned domains
Global Money Map, Macro Intelligence, Institutional Flows, Crypto Intelligence, Asset Rotation, Risk Intelligence, AI Research Analyst, Alerts and Reports.

## Deployment target
Streamlit Community Cloud, with GitHub Actions for automated tests. Store secrets only in deployment secret storage.
