from confluent_kafka import Consumer
import json
from app.services.neo4j_service import insert_transaction
from app.services.risk_service import score_transaction

def start_consumer():
    print("🚀 Kafka consumer started...")

    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'aml-group',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe(['transactions'])

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print("Error:", msg.error())
            continue

        data = json.loads(msg.value().decode('utf-8'))

        # Apply risk scoring
        scored = score_transaction(data)

        # Insert into Neo4j
        insert_transaction(scored)

        print(f"✅ Inserted into Neo4j: {data['tx_id']}")
