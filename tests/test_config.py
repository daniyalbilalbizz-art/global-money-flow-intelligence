from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def test_source_registry_requires_provenance():
    cfg = yaml.safe_load((ROOT / 'config/sources.yaml').read_text())
    assert cfg['policy']['require_provenance'] is True
    assert 'binance_public' in cfg['sources']

def test_watchlist_contains_core_assets():
    cfg = yaml.safe_load((ROOT / 'config/assets.yaml').read_text())
    symbols = {x['symbol'] for group in cfg['assets'].values() for x in group}
    assert {'BTCUSDT', 'ETHUSDT', 'US10Y', 'DXY', 'GOLD'}.issubset(symbols)
