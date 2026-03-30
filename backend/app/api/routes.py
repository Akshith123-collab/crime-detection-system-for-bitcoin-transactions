from collections import Counter
from fastapi import APIRouter
from app.services.neo4j_service import test_connection, fetch_summary, fetch_recent_alerts

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "neo4j": test_connection()}

@router.get("/summary")
def summary():
    return fetch_summary()

@router.get("/alerts")
def alerts():
    return fetch_recent_alerts()

@router.get("/risk-distribution")
def risk_distribution():
    alerts = fetch_recent_alerts(200)
    buckets = {
        "45-54": 0,
        "55-64": 0,
        "65-74": 0,
        "75-84": 0,
        "85-100": 0,
    }

    for row in alerts:
        score = row["risk_score"]
        if 45 <= score <= 54:
            buckets["45-54"] += 1
        elif 55 <= score <= 64:
            buckets["55-64"] += 1
        elif 65 <= score <= 74:
            buckets["65-74"] += 1
        elif 75 <= score <= 84:
            buckets["75-84"] += 1
        elif score >= 85:
            buckets["85-100"] += 1

    return [{"bucket": k, "count": v} for k, v in buckets.items()]

@router.get("/reason-breakdown")
def reason_breakdown():
    alerts = fetch_recent_alerts(200)
    counter = Counter()

    for row in alerts:
        for reason in row["reasons"]:
            counter[reason] += 1

    return [{"reason": k, "count": v} for k, v in counter.items()]
