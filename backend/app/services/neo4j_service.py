from neo4j import GraphDatabase
from app.utils.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 'neo4j-ok' AS msg")
        return result.single()["msg"]

def init_graph():
    queries = [
        "CREATE CONSTRAINT transaction_id IF NOT EXISTS FOR (t:Transaction) REQUIRE t.tx_id IS UNIQUE",
        "CREATE CONSTRAINT wallet_id IF NOT EXISTS FOR (w:Wallet) REQUIRE w.wallet_id IS UNIQUE"
    ]
    with driver.session() as session:
        for query in queries:
            session.run(query)

def insert_transaction(tx: dict):
    query = """
    MERGE (s:Wallet {wallet_id: $source})
    MERGE (d:Wallet {wallet_id: $target})
    MERGE (t:Transaction {tx_id: $tx_id})
    SET t.amount = $amount,
        t.timestamp = $timestamp,
        t.source = $source,
        t.target = $target,
        t.risk_score = $risk_score,
        t.is_suspect = $is_suspect,
        t.reasons = $reasons,
        t.hop_count = $hop_count,
        t.velocity_score = $velocity_score,
        t.amount_zscore = $amount_zscore
    MERGE (s)-[:SENT {is_suspect: $is_suspect}]->(t)
    MERGE (t)-[:TO {is_suspect: $is_suspect}]->(d)
    """
    with driver.session() as session:
        session.run(query, **tx)

def fetch_summary():
    query = """
    MATCH (t:Transaction)
    RETURN
      count(t) AS total_transactions,
      sum(CASE WHEN t.is_suspect THEN 1 ELSE 0 END) AS suspect_transactions,
      round(avg(t.risk_score), 2) AS avg_risk_score,
      round(sum(t.amount), 2) AS total_amount
    """
    with driver.session() as session:
        record = session.run(query).single()
        return dict(record) if record else {}

def fetch_recent_alerts(limit=20):
    query = """
    MATCH (t:Transaction)
    WHERE t.is_suspect = true
    RETURN t.tx_id AS tx_id,
           t.amount AS amount,
           t.timestamp AS timestamp,
           t.risk_score AS risk_score,
           t.reasons AS reasons,
           t.source AS source,
           t.target AS target
    ORDER BY t.timestamp DESC
    LIMIT $limit
    """
    with driver.session() as session:
        rows = session.run(query, limit=limit)
        return [dict(r) for r in rows]
