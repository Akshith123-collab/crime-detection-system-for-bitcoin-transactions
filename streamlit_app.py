import streamlit as st
import pandas as pd
import json
from neo4j import GraphDatabase
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# CONFIG
# -----------------------------
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "amlproject123"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

st.set_page_config(page_title="AML Dashboard", layout="wide")

st.title("🚀 AML Live Monitoring Dashboard")

# -----------------------------
# MODEL METRICS
# -----------------------------
st.header("📊 Model Performance")

try:
    with open("backend/app/model_metrics.json") as f:
        metrics = json.load(f)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Accuracy", f"{metrics['accuracy']:.2f}")
    col2.metric("Precision", f"{metrics['precision_illicit']:.2f}")
    col3.metric("Recall", f"{metrics['recall_illicit']:.2f}")
    col4.metric("F1 Score", f"{metrics['f1_illicit']:.2f}")

except:
    st.warning("Run evaluation first")

# -----------------------------
# LOAD NEO4J DATA
# -----------------------------
def run_query(query):
    with driver.session() as session:
        result = session.run(query)
        return [dict(record) for record in result]

# -----------------------------
# TRANSACTION SUMMARY
# -----------------------------
st.header("📈 Transaction Overview")

query = """
MATCH (t:Transaction)
RETURN 
count(t) AS total,
sum(CASE WHEN t.is_suspect THEN 1 ELSE 0 END) AS suspicious,
avg(t.risk_score) AS avg_risk
"""

data = run_query(query)

if data:
    d = data[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", d["total"])
    col2.metric("Suspicious", d["suspicious"])
    col3.metric("Avg Risk Score", round(d["avg_risk"], 2))

# -----------------------------
# SUSPICIOUS TRANSACTIONS
# -----------------------------
st.header("🚨 Suspicious Transactions")

query = """
MATCH (s:Wallet)-[:SENT]->(t:Transaction)-[:TO]->(d:Wallet)
WHERE t.is_suspect = true
RETURN s.wallet_id AS source, d.wallet_id AS target,
t.tx_id AS tx_id, t.amount AS amount, t.risk_score AS risk
LIMIT 50
"""

df = pd.DataFrame(run_query(query))

if not df.empty:
    st.dataframe(df)

# -----------------------------
# HIGH RISK GRAPH DATA
# -----------------------------
st.header("🔥 High Risk Transactions")

query = """
MATCH (t:Transaction)
WHERE t.risk_score >= 75
RETURN t.tx_id AS tx_id, t.risk_score AS risk
LIMIT 50
"""

df_high = pd.DataFrame(run_query(query))

if not df_high.empty:
    fig, ax = plt.subplots()
    sns.histplot(df_high["risk"], bins=10, ax=ax)
    st.pyplot(fig)

# -----------------------------
# CORRECT vs WRONG
# -----------------------------
st.header("✅ ML Prediction Accuracy")

try:
    df_pred = pd.read_csv("backend/app/predictions.csv")

    df_pred["correct"] = df_pred["actual"] == df_pred["predicted"]

    correct = df_pred["correct"].sum()
    wrong = len(df_pred) - correct

    fig2, ax2 = plt.subplots()
    ax2.pie(
        [correct, wrong],
        labels=["Correct", "Wrong"],
        autopct="%1.1f%%",
        colors=["green", "red"]
    )
    st.pyplot(fig2)

except:
    st.warning("Run evaluation to generate predictions.csv")

# -----------------------------
# CONFUSION MATRIX
# -----------------------------
st.header("📉 Confusion Matrix")

try:
    cm = pd.crosstab(df_pred["actual"], df_pred["predicted"])

    fig3, ax3 = plt.subplots()
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax3)

    st.pyplot(fig3)

except:
    pass

# -----------------------------
# WALLET ANALYSIS
# -----------------------------
st.header("💰 Wallet Risk Analysis")

query = """
MATCH (w:Wallet)-[:SENT]->(t:Transaction)
RETURN w.wallet_id AS wallet, avg(t.risk_score) AS avg_risk
ORDER BY avg_risk DESC
LIMIT 20
"""

df_wallet = pd.DataFrame(run_query(query))

if not df_wallet.empty:
    st.dataframe(df_wallet)
