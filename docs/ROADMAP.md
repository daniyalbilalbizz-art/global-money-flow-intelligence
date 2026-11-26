# Roadmap

## Phase 0 — Foundation
- [x] Streamlit application shell
- [x] Source and asset registries
- [x] Public Binance ticker adapter
- [x] Initial configuration tests and data policy

## Phase 1 — Data layer
- [x] Canonical observation validation and quality statuses
- [x] Bounded HTTP retry/backoff for transient failures
- [x] SQLite persistence and normalized observation storage
- [x] FRED series adapter and dashboard workflow (runtime use requires owner's free API key)
- [x] DefiLlama stablecoin overview fetcher
- [x] SEC submissions metadata adapter
- [x] Configurable CFTC Socrata adapter (exact dataset ID must be verified before use)
- [x] Treasury Fiscal Data generic endpoint adapter (exact dataset endpoint must be verified before use)
- [x] Unit tests and GitHub Actions CI (latest run: 7 passed)
- [ ] Runtime-verify each provider endpoint, schema, units, publication timestamps, pagination, limits and failure modes
- [ ] Implement and verify Federal Reserve H.4.1 parser
- [ ] Verify exact Treasury dataset endpoints and CFTC report dataset ID before enabling scheduled ingestion
- [ ] Add source-specific freshness policies and integration tests

## Phase 2 — Intelligence engines
- [ ] Macro regime and liquidity analytics
- [ ] Institutional positioning and reported flow datasets
- [ ] Crypto market structure and stablecoin analytics
- [ ] Evidence-graded asset rotation hypotheses
- [ ] Risk dashboard and scenario analysis

## Phase 3 — Research and delivery
- [ ] Evidence-cited research analyst
- [ ] Alerts, scheduled reports and exports
- [ ] Backtests, integration tests and security review
- [ ] Streamlit deployment and operational monitoring

A code adapter is not considered production-verified until its real endpoint, schema, units, timestamps, pagination, limits, and failure behavior pass tests. Data availability and publication frequency vary by provider.
