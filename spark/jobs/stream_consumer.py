import json
from confluent_kafka import Consumer
from app.services.neo4j_service import insert_transaction
from app.services.risk_service import score_transaction

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "aml-risk-consumer",
    "auto.offset.reset": "earliest"
})

TOPIC = "transactions"

def main():
    consumer.subscribe([TOPIC])
    print("consumer_started=true")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"consumer_error={msg.error()}")
                continue

            data = json.loads(msg.value().decode("utf-8"))
            scored = score_transaction(data)
            insert_transaction(scored)

            print(
                f"processed tx_id={scored['tx_id']} "
                f"risk_score={scored['risk_score']} "
                f"is_suspect={scored['is_suspect']} "
                f"reasons={','.join(scored['reasons']) if scored['reasons'] else 'none'}"
            )
    except KeyboardInterrupt:
        print("consumer_stopped=true")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
