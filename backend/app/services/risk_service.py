HIGH_RISK_WALLETS = {
    "wallet_dark_001",
    "wallet_mixer_009",
    "wallet_scam_777",
    "wallet_risky_404"
}

def score_transaction(tx: dict) -> dict:
    score = 0
    reasons = []

    amount = float(tx["amount"])
    velocity_score = int(tx.get("velocity_score", 0))
    hop_count = int(tx.get("hop_count", 1))
    amount_zscore = float(tx.get("amount_zscore", 0))

    if tx["source"] in HIGH_RISK_WALLETS or tx["target"] in HIGH_RISK_WALLETS:
        score += 35
        reasons.append("linked_to_high_risk_wallet")

    if amount >= 150000:
        score += 20
        reasons.append("very_large_amount")

    if amount_zscore >= 2.5:
        score += 15
        reasons.append("amount_anomaly")

    if velocity_score >= 8:
        score += 15
        reasons.append("high_velocity_pattern")

    if hop_count >= 4:
        score += 10
        reasons.append("multi_hop_layering_pattern")

    if tx["source"].startswith("wallet_new_"):
        score += 8
        reasons.append("newly_seen_source_wallet")

    tx["risk_score"] = min(score, 100)
    tx["is_suspect"] = tx["risk_score"] >= 45
    tx["reasons"] = reasons
    return tx
