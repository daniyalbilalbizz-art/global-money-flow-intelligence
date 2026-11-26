from datetime import datetime, timezone, timedelta
from engines.validation import validate_observation
from engines.storage import save_observations, latest_observations

def base_row():
    now = datetime.now(timezone.utc).isoformat()
    return {"observation_id":"abc","series_id":"TEST","source_id":"test","value":1.2,
            "unit":"index_points","observed_at":now,"retrieved_at":now,
            "frequency":"daily","evidence_class":"REPORTED","quality_status":"VALID"}

def test_valid_observation_passes():
    result = validate_observation(base_row())
    assert result["valid"] and result["status"] == "VALID"

def test_nan_is_rejected():
    row = base_row()
    row["value"] = float("nan")
    assert validate_observation(row)["status"] == "INVALID"

def test_unknown_evidence_class_is_rejected():
    row = base_row()
    row["evidence_class"] = "GUESS"
    assert validate_observation(row)["status"] == "INVALID"

def test_old_observation_is_delayed():
    row = base_row()
    row["observed_at"] = (datetime.now(timezone.utc)-timedelta(days=5)).isoformat()
    assert validate_observation(row, max_age_seconds=86400)["status"] == "DELAYED"

def test_sqlite_round_trip(tmp_path):
    row = base_row()
    assert save_observations([row], tmp_path/"test.sqlite3") == 1
    stored = latest_observations(tmp_path/"test.sqlite3")
    assert stored[0]["series_id"] == "TEST"
