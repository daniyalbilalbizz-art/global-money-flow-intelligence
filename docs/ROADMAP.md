# Roadmap

## Phase 0 — Foundation
- [x] Streamlit application shell
- [x] Source and asset registries
- [x] Public Binance ticker adapter
- [x] Initial configuration tests and data policy

## Phase 1 — Data layer
- [x] Schema validation, retry/backoff, freshness status and quality checks (initial implementation)
- [x] SQLite persistence and normalized observation storage
- [x] FRED ingestion adapter and dashboard workflow (runtime use requires owner's free API key)
- [x] DefiLlama public stablecoin fetcher
- [x] SEC submissions and configurable CFTC Socrata fetchers
- [x] Treasury Fiscal Data generic endpoint adapter
- [ ] Runtime-verify each provider endpoint, schema, rate limits, publication timestamps and failure modes
- [ ] Implement and verify Federal Reserve H.4.1 parser
- [ ] Verify exact Treasury dataset endpoints and CFTC report dataset ID before enabling scheduled ingestion
- [ ] Add source-specific units, frequency and freshness policies; automated integration tests

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
