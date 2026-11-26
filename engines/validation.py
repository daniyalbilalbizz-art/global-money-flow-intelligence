"""Canonical observation validation and freshness policy."""
from datetime import datetime, timezone
from math import isfinite

REQUIRED = {"series_id", "source_id", "value", "unit", "observed_at", "retrieved_at", "evidence_class"}

def validate_observation(row, max_age_seconds=None, now=None):
    errors = []
    missing = REQUIRED - set(row)
    if missing:
        errors.append("missing_fields:" + ",".join(sorted(missing)))
    if errors:
        return {"valid": False, "status": "INVALID", "errors": errors}
    try:
        value = float(row["value"])
        if not isfinite(value):
            errors.append("value_not_finite")
    except (TypeError, ValueError):
        errors.append("value_not_numeric")
    if row["evidence_class"] not in {"REPORTED", "ESTIMATED", "INFERRED"}:
        errors.append("invalid_evidence_class")
    parsed = None
    try:
        parsed = datetime.fromisoformat(str(row["observed_at"]).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            errors.append("observed_at_missing_timezone")
    except ValueError:
        errors.append("observed_at_invalid")
    try:
        retrieved = datetime.fromisoformat(str(row["retrieved_at"]).replace("Z", "+00:00"))
        if retrieved.tzinfo is None:
            errors.append("retrieved_at_missing_timezone")
    except ValueError:
        errors.append("retrieved_at_invalid")
    if errors:
        return {"valid": False, "status": "INVALID", "errors": errors}
    status = "VALID"
    if max_age_seconds is not None and parsed is not None:
        now = now or datetime.now(timezone.utc)
        age = (now - parsed.astimezone(timezone.utc)).total_seconds()
        if age > max_age_seconds:
            status = "DELAYED"
    return {"valid": True, "status": status, "errors": []}
