import json
import time
from confluent_kafka import Producer
from pathlib import Path

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "transactions"
INPUT_FILE = Path("data/sample_stream/transactions.jsonl")

producer = Producer({"bootstrap.servers": BOOTSTRAP_SERVERS})

def delivery_report(err, msg):
    if err is not None:
        print(f"delivery_failed key={msg.key()} error={err}")
    else:
        print(f"delivered topic={msg.topic()} partition={msg.partition()} offset={msg.offset()}")

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Missing input file: {INPUT_FILE}")

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            payload = line.strip()
            if not payload:
                continue
            data = json.loads(payload)
            producer.produce(
                TOPIC,
                key=data["tx_id"],
                value=json.dumps(data),
                callback=delivery_report
            )
            producer.poll(0)
            print(f"sent tx_id={data['tx_id']} pattern={data['pattern']} amount={data['amount']}")
            time.sleep(0.05)

    producer.flush()
    print("stream_complete=true")

if __name__ == "__main__":
    main()
