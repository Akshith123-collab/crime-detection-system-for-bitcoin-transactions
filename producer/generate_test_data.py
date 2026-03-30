import json
import random
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_FILE = Path("data/sample_stream/transactions.jsonl")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

NORMAL_WALLETS = [f"wallet_user_{i:03d}" for i in range(1, 81)]
NEW_WALLETS = [f"wallet_new_{i:03d}" for i in range(1, 21)]
HIGH_RISK_WALLETS = [
    "wallet_dark_001",
    "wallet_mixer_009",
    "wallet_scam_777",
    "wallet_risky_404"
]
EXCHANGES = ["wallet_exchange_binance", "wallet_exchange_coinbase", "wallet_exchange_kraken"]

ALL_WALLETS = NORMAL_WALLETS + NEW_WALLETS + HIGH_RISK_WALLETS + EXCHANGES

def normal_tx(i, ts):
    source = random.choice(NORMAL_WALLETS)
    target = random.choice([w for w in NORMAL_WALLETS + EXCHANGES if w != source])
    amount = round(random.uniform(150, 12000), 2)
    return {
        "tx_id": f"tx_normal_{i:05d}",
        "source": source,
        "target": target,
        "amount": amount,
        "timestamp": ts.isoformat(),
        "velocity_score": random.randint(1, 4),
        "hop_count": random.randint(1, 2),
        "amount_zscore": round(random.uniform(0.1, 1.8), 2),
        "pattern": "normal"
    }

def suspicious_large_amount(i, ts):
    source = random.choice(NORMAL_WALLETS + NEW_WALLETS)
    target = random.choice(HIGH_RISK_WALLETS + EXCHANGES)
    amount = round(random.uniform(160000, 450000), 2)
    return {
        "tx_id": f"tx_large_{i:05d}",
        "source": source,
        "target": target,
        "amount": amount,
        "timestamp": ts.isoformat(),
        "velocity_score": random.randint(5, 8),
        "hop_count": random.randint(2, 4),
        "amount_zscore": round(random.uniform(2.6, 4.5), 2),
        "pattern": "large_amount_to_risky"
    }

def suspicious_layering(i, ts):
    source = random.choice(NEW_WALLETS)
    target = random.choice(HIGH_RISK_WALLETS + NORMAL_WALLETS)
    amount = round(random.uniform(40000, 120000), 2)
    return {
        "tx_id": f"tx_layer_{i:05d}",
        "source": source,
        "target": target,
        "amount": amount,
        "timestamp": ts.isoformat(),
        "velocity_score": random.randint(8, 10),
        "hop_count": random.randint(4, 6),
        "amount_zscore": round(random.uniform(2.0, 3.8), 2),
        "pattern": "layering_velocity"
    }

def suspicious_mixer(i, ts):
    source = random.choice(NORMAL_WALLETS + NEW_WALLETS)
    target = "wallet_mixer_009"
    amount = round(random.uniform(25000, 180000), 2)
    return {
        "tx_id": f"tx_mixer_{i:05d}",
        "source": source,
        "target": target,
        "amount": amount,
        "timestamp": ts.isoformat(),
        "velocity_score": random.randint(7, 10),
        "hop_count": random.randint(3, 5),
        "amount_zscore": round(random.uniform(2.3, 4.2), 2),
        "pattern": "mixer_interaction"
    }

def build_dataset(total=300):
    rows = []
    base_time = datetime.utcnow() - timedelta(hours=6)

    for i in range(total):
        ts = base_time + timedelta(seconds=i * 45)
        r = random.random()

        if r < 0.68:
            rows.append(normal_tx(i, ts))
        elif r < 0.80:
            rows.append(suspicious_large_amount(i, ts))
        elif r < 0.92:
            rows.append(suspicious_layering(i, ts))
        else:
            rows.append(suspicious_mixer(i, ts))

    return rows

def main():
    random.seed(42)
    rows = build_dataset(300)
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")

    print(f"generated_file={OUTPUT_FILE}")
    print(f"total_rows={len(rows)}")

    counts = {}
    for row in rows:
        counts[row["pattern"]] = counts.get(row["pattern"], 0) + 1
    print("pattern_counts=", counts)

if __name__ == "__main__":
    main()
