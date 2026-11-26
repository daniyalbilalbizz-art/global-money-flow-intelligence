import os
from pathlib import Path

import streamlit as st
import yaml

from engines.providers import get_binance_ticker
from engines.ingestion import fetch_fred_series, fetch_defillama_stablecoins
from engines.storage import save_observations, latest_observations
from engines.validation import validate_observation

ROOT = Path(__file__).parent
st.set_page_config(page_title="GMF OS | Global Money Flow Intelligence", page_icon="🌐", layout="wide")

@st.cache_data(ttl=300, show_spinner=False)
def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

sources = load_yaml(ROOT / "config" / "sources.yaml")
assets = load_yaml(ROOT / "config" / "assets.yaml")
sections = ["Global Money Map", "Macro Intelligence", "Institutional Flows", "Crypto Intelligence", "Data Engineering", "Asset Rotation", "Risk Intelligence", "AI Research Analyst", "Alerts & Reports"]

st.title("🌐 Global Money Flow Intelligence")
st.caption("Evidence-led macro, liquidity and cross-asset research workspace")
with st.sidebar:
    st.header("Navigation")
    section = st.radio("Research module", sections)
    st.divider()
    st.caption("Reported ≠ estimated ≠ inferred")

st.subheader(section)
if section == "Crypto Intelligence":
    st.markdown("### Public crypto market snapshot")
    symbol = st.selectbox("Asset", ["BTCUSDT", "ETHUSDT"])
    if st.button("Fetch latest public ticker", type="primary"):
        try:
            with st.spinner("Requesting Binance public market data…"):
                data = get_binance_ticker(symbol)
            c1, c2, c3 = st.columns(3)
            c1.metric("Last Price (USDT)", f"{data['last_price']:,.2f}")
            c2.metric("24h Change", f"{data['price_change_pct_24h']:.2f}%")
            c3.metric("24h Base Volume", f"{data['volume_base_24h']:,.2f}")
            st.caption(f"Source: {data['source']} · Retrieved: {data['retrieved_at']} · {data['classification']}")
            st.link_button("Open source endpoint", data["source_url"])
        except Exception as exc:
            st.error(f"Feed unavailable: {exc}")
elif section == "Data Engineering":
    st.markdown("### FRED economic series ingestion")
    st.caption("FRED requires a free API key. Set FRED_API_KEY in Streamlit secrets or the local environment. The key is never displayed.")
    try:
        secret_key = st.secrets.get("FRED_API_KEY", "")
    except Exception:
        secret_key = ""
    api_key = secret_key or os.getenv("FRED_API_KEY", "")
    series_id = st.text_input("FRED series ID", value="DGS10", help="Example: DGS10 = Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity.")
    start_date = st.date_input("Observation start date")
    if st.button("Fetch FRED observations", type="primary"):
        if not api_key:
            st.warning("Add your free FRED API key to Streamlit secrets as FRED_API_KEY, then retry.")
        else:
            try:
                with st.spinner("Fetching and validating observations…"):
                    rows = fetch_fred_series(series_id.strip(), api_key, start_date.isoformat())
                    accepted=[]
                    rejected=0
                    for row in rows:
                        verdict=validate_observation(row)
                        if verdict["valid"]:
                            row["quality_status"]=verdict["status"]
                            accepted.append(row)
                        else:
                            rejected += 1
                    saved=save_observations(accepted)
                st.success(f"Fetched {len(rows)} observations; saved {saved}; rejected {rejected}.")
                if accepted:
                    st.dataframe([{"Date":r["observed_at"][:10],"Value":r["value"],"Unit":r["unit"],"Source":r["source_id"]} for r in accepted[-20:]], use_container_width=True)
            except Exception as exc:
                st.error(f"FRED ingestion failed: {exc}")
    st.divider()
    st.markdown("### Public stablecoin overview")
    if st.button("Fetch DefiLlama stablecoin dataset"):
        try:
            with st.spinner("Fetching public stablecoin data…"):
                payload=fetch_defillama_stablecoins()
            st.success(f"Retrieved public dataset at {payload['retrieved_at']}.")
            st.json(payload["data"] if isinstance(payload["data"], (dict,list)) else {"response":str(payload["data"])})
        except Exception as exc:
            st.error(f"DefiLlama feed unavailable: {exc}")
    st.divider()
    st.markdown("### Local observation store")
    stored=latest_observations(limit=100)
    st.metric("Stored observations (latest 100 view)", len(stored))
    if stored:
        st.dataframe(stored, use_container_width=True)
else:
    st.markdown("### Module status")
    st.info("This module is registered in the platform roadmap. Its full data pipeline and calculations are not yet implemented; no synthetic market values are shown.")

with st.expander("Registered data sources"):
    for key, source in sources["sources"].items():
        st.write(f"**{source['name']}** — {source['status']} · {source['access']}")
with st.expander("Initial asset universe"):
    st.json(assets["assets"])

st.divider()
st.caption("GMF OS · Research tooling, not investment advice. Source schedules, timestamps and methodology must be checked before acting.")
