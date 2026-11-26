import streamlit as st
import yaml
from pathlib import Path
from engines.providers import get_binance_ticker

ROOT = Path(__file__).parent
st.set_page_config(page_title="GMF OS | Global Money Flow Intelligence", page_icon="🌐", layout="wide")
st.title("🌐 Global Money Flow Intelligence")
st.caption("Institutional-style macro, liquidity and cross-asset research workspace")

@st.cache_data(ttl=300, show_spinner=False)
def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

sources = load_yaml(ROOT / "config" / "sources.yaml")
assets = load_yaml(ROOT / "config" / "assets.yaml")
sections = ["Global Money Map", "Macro Intelligence", "Institutional Flows", "Crypto Intelligence", "Asset Rotation", "Risk Intelligence", "AI Research Analyst", "Alerts & Reports"]
with st.sidebar:
    st.header("Navigation")
    section = st.radio("Research module", sections)
    st.divider()
    st.caption("Data integrity: reported ≠ estimated ≠ inferred")

st.subheader(section)
st.info("Foundation build: only connected feeds are displayed. Missing or unverified feeds are never replaced with synthetic values.")

if section == "Crypto Intelligence":
    st.markdown("### Public crypto market snapshot")
    symbol = st.selectbox("Asset", ["BTCUSDT", "ETHUSDT"])
    if st.button("Fetch latest public ticker", type="primary"):
        try:
            with st.spinner("Requesting public market data…"):
                data = get_binance_ticker(symbol)
            c1, c2, c3 = st.columns(3)
            c1.metric("Last Price (USDT)", f"{data['last_price']:,.2f}")
            c2.metric("24h Change", f"{data['price_change_pct_24h']:.2f}%")
            c3.metric("24h Base Volume", f"{data['volume_base_24h']:,.2f}")
            st.caption(f"Source: {data['source']} · Retrieved: {data['retrieved_at']} · Classification: {data['classification']}")
            st.link_button("Open source endpoint", data["source_url"])
        except Exception as exc:
            st.error(f"Feed unavailable: {exc}")
else:
    st.markdown("### Module status")
    st.write("This module is registered in the platform roadmap. Its data pipeline is not yet connected, so no live values are shown.")

with st.expander("Registered data sources"):
    for key, source in sources["sources"].items():
        st.write(f"**{source['name']}** — {source['status']} · {source['access']}")
with st.expander("Initial asset universe"):
    st.json(assets["assets"])

st.divider()
st.caption("GMF OS · Research tooling, not investment advice. Verify source timestamps and methodology before acting.")
