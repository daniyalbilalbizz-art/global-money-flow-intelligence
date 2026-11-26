# Verification Log

Updated: 2026-11-26

## Automated tests
- GitHub Actions workflow: `GMF OS tests`
- Latest verified run: [Run 6](https://github.com/daniyalbilalbizz-art/global-money-flow-intelligence/actions/runs/45786635154)
- Result: **7 passed**
- Test scope: source/asset configuration, evidence validation, invalid numeric rejection, invalid evidence class rejection, delayed-data status, and SQLite write/read round trip.
- CI environment: GitHub-hosted Ubuntu runner, Python 3.11.

## Provider verification status

| Provider | Adapter present | Runtime/schema verified | Notes |
|---|---:|---:|---|
| Binance public ticker | Yes | Pending separate live-feed checks | Public spot ticker used by dashboard |
| FRED | Yes | Pending owner API key and live request | Free API key required |
| Treasury Fiscal Data | Generic adapter | Pending | Exact official dataset endpoint must be selected and checked |
| Federal Reserve H.4.1 | No dedicated parser yet | Pending | Weekly release; parser deliberately not guessed |
| SEC EDGAR submissions | Yes | Pending live request | Filing metadata, not fund flow |
| CFTC Socrata | Configurable adapter | Pending | Exact COT dataset identifier must be verified |
| DefiLlama stablecoins | Yes | Pending live request | Aggregated stablecoin data; supply change is not automatically a capital transfer |

## Known limitations
- Passing unit tests do not establish provider uptime, data correctness, or production readiness.
- No direct institutional order-flow feed is claimed.
- Data from public APIs can be delayed, revised, rate-limited, or unavailable.
- No credentials are stored in this repository.
