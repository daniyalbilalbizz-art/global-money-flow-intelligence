# Phase 1 Data Layer

## Implemented in this increment
- Shared HTTP session with bounded retries for transient server and rate-limit responses.
- FRED series observations adapter (requires free FRED API key).
- Treasury Fiscal Data generic endpoint adapter; endpoint must be verified against the official dataset catalogue before use.
- DefiLlama stablecoin overview fetcher.
- SEC EDGAR company submissions fetcher. This is filing metadata, not an institutional flow feed.
- CFTC public Socrata fetcher with an explicit dataset ID; dataset selection remains a verification prerequisite.
- Normalized observation validation, UTC retrieval timestamps, deterministic observation IDs, SQLite persistence, and unit tests.
- GitHub Actions workflow for running tests on pushes and pull requests.

## Important limits
- FRED, SEC, Treasury and CFTC observations have source-specific release schedules and are not intraday feeds by default.
- SEC submissions do not represent ETF subscriptions/redemptions or live fund flows.
- DefiLlama stablecoin overview is aggregated provider data; changes in supply are not automatically cross-asset transfers.
- Federal Reserve H.4.1 is published weekly. A dedicated parser is not enabled until its downloadable format and field mapping are runtime-verified.
- CFTC integration requires choosing and verifying the exact report dataset identifier. Do not guess one.
- The Treasury adapter requires a valid official Fiscal Data endpoint. Do not point it at an unverified path.

## Run tests
`pytest -q`

## Required secrets
For FRED only, set `FRED_API_KEY` in local environment or Streamlit secrets. Never commit it or paste it into chat.
