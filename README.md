# 🚨 Bitcoin Transaction Crime Detection System (AML)

## 📌 Overview

This project focuses on detecting **illicit (criminal) Bitcoin transactions** using Machine Learning and graph-based analysis.

With the rise of cryptocurrencies, financial crimes such as money laundering and fraud have increased. This system aims to identify suspicious transactions using features derived from the **Elliptic Bitcoin Dataset**.

---

## 🎯 Objectives

* Detect whether a Bitcoin transaction is **licit or illicit**
* Use ML models for prediction and validation
* Visualize transaction relationships using graph techniques
* Provide insights into suspicious transaction patterns

---

## 🛠️ Tech Stack

### 👨‍💻 Programming & Frameworks

* Python
* Streamlit (Dashboard)
* Pandas, NumPy (Data Processing)

### 🤖 Machine Learning

* Scikit-learn
* Models used:

  * Logistic Regression
  * Random Forest

### 📊 Visualization & Graph

* Neo4j (Graph Database)
* Matplotlib / Plotly

### 🗄️ Dataset

* Elliptic Bitcoin Dataset

---

## 📂 Project Structure

```
bitcoin-aml-system/
│
├── app/                # Streamlit dashboard
├── src/                # Core ML & processing code
├── models/             # Saved ML models
├── notebooks/          # Experiments & analysis
├── data/               # Dataset (not included)
├── requirements.txt
└── README.md
```

---

## ⚠️ Dataset Note

Due to size limitations, the dataset is not included in this repository.

👉 Download from:
https://www.kaggle.com/datasets/ellipticco/elliptic-data-set

After downloading, place it inside:

```
data/elliptic/
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Akshith123-collab/crime-detection-system-for-bitcoin-transactions.git
cd crime-detection-system-for-bitcoin-transactions
```

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Project

### ▶️ Run ML Pipeline

```bash
python src/main.py
```

### 🌐 Run Dashboard

```bash
streamlit run app/app.py
```

---

## 🔍 How the System Works

### 1. Data Processing

* Load transaction features
* Clean and preprocess data
* Label transactions (licit / illicit)

### 2. Feature Engineering

* Time-based features
* Transaction graph features
* Aggregated statistics

### 3. Model Training

* Train ML models on labeled data
* Evaluate using accuracy, precision, recall

### 4. Prediction

* Classify new transactions
* Output: **Licit / Illicit**

### 5. Visualization

* Graph-based transaction analysis (Neo4j)
* Dashboard insights using Streamlit

---

## 🧠 How Illicit Transactions are Detected

The model detects suspicious transactions based on:

* Abnormal transaction patterns
* Connections to known illicit nodes
* Frequency and volume anomalies
* Graph relationships (neighbors, clusters)

👉 If a transaction shows patterns similar to known illegal behavior, it is classified as **illicit**

---

## 📊 Model Performance (Example)

* Accuracy: ~95% (depends on dataset split)
* Precision & Recall optimized for fraud detection

---

## 📸 Features

* ✅ Real-time transaction prediction
* ✅ ML vs Rule-based comparison
* ✅ Neo4j graph visualization
* ✅ Dashboard with insights
* ✅ Classification of transactions

---

## 🔮 Future Improvements

* Use Deep Learning (GNNs for graph data)
* Real-time blockchain monitoring
* Advanced anomaly detection
* API deployment

---

## 👨‍🎓 Use Case

* Academic project (AML / FinTech)
* Fraud detection systems
* Blockchain analytics

---

## 📌 Conclusion

This project demonstrates how **Machine Learning + Graph Analysis** can be combined to detect financial crimes in blockchain systems.

---

## 🙌 Author

**Akshith Viswanathan**
M.Tech CSE

---

## ⭐ If you like this project

Give it a star on GitHub!
