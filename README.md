# 🛒 E-Commerce Customer RFM Segmentation API

An end-to-end data science pipeline and REST API that processes **100,000+ real-world e-commerce transactions** to classify customers into actionable business segments using **RFM (Recency, Frequency, Monetary)** analysis — enabling marketing teams to run precise, data-driven campaigns at scale.

---

## 🚀 Project Overview

In e-commerce, not all customers are equal. This project transforms raw, relational database exports into a high-speed, production-ready API that instantly classifies users based on their purchasing behavior.

Instead of treating every user the same, the system evaluates three key dimensions — **when** a customer last bought, **how often** they buy, and **how much** they spend — to assign them a segment like **Champions**, **At Risk**, or **Hibernating**, along with automated, tailored marketing recommendations for each.

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Data Processing | Python, Pandas |
| API Framework | FastAPI, Uvicorn |
| Exploratory Analysis | Jupyter Notebooks, Matplotlib, Seaborn |
| Data Source | [Brazilian E-Commerce Dataset — Olist (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) |

---

## 📁 Project Structure

```text
ecommerce-rfm-api/
│
├── data/                                        # Raw datasets & pre-calculated lookups (git-ignored)
├── notebooks/
│   └── 01_rfm_exploratory_analysis.ipynb       # EDA, Pandas logic, and visualizations
│
├── compute_rfm.py                               # Backend script — merges CSVs and computes RFM scores
├── main.py                                      # FastAPI application serving customer insights
├── requirements.txt                             # Python dependencies
└── README.md
```

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Yash49-Xe/ecommerce-rfm-api.git
cd ecommerce-rfm-api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add the dataset

Download the [Olist Dataset from Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and place the following three files into the `/data` directory:

data/
├── olist_customers_dataset.csv
├── olist_orders_dataset.csv
└── olist_order_payments_dataset.csv


### 4. Run the data pipeline

Execute the data engineering script to merge the source tables, calculate RFM scores, and generate the lightweight `rfm_output.csv` lookup table.

```bash
python compute_rfm.py
```

### 5. Start the API server

```bash
uvicorn main:app --reload
```

The API will be live at **http://127.0.0.1:8000**

> 📖 Interactive Swagger UI docs available at **http://127.0.0.1:8000/docs**

---

## 📡 API Reference

### `GET /api/v1/customer-segment/{customer_unique_id}`

Returns the calculated RFM scores, segment classification, and a tailored marketing recommendation for the given customer.

**Example Response**

```json
{
  "customer_id": "8d50f5eadf50201ccdcedfb4e2ac8455",
  "rfm_scores": {
    "recency_score": 4,
    "frequency_score": 1,
    "monetary_score": 3
  },
  "segment_code": "413",
  "segment_name": "Recent Customers",
  "recommended_action": "Send a welcome onboarding sequence or a customer satisfaction feedback survey."
}
```

---

## 📈 Business Insights

> See the [Jupyter Notebook](notebooks/rfm_exploratory_analysis.ipynb) for full visualizations and methodology.

By mapping the mathematical quantiles to business logic and visualizing the revenue distribution, we uncovered several crucial, non-traditional insights about the Olist marketplace:

1. **The Acquisition-Heavy Marketplace:** Contrary to standard retail models where "Champions" drive the majority of sales, our visualization reveals that the vast majority of historical revenue (> $14 Million) comes from the **"Lost"**, **"Recent Customers"**, **"Hibernating"**, and **"Promising"** segments. This indicates a business model heavily reliant on continuous new customer acquisition rather than long-term retention.
2. **The Frequency Skew:** Out of ~100,000 unique customers, over 95% made only a single purchase. This extreme right-skew in the Frequency metric required custom scoring functions to properly isolate the few returning buyers from the massive pool of one-off shoppers.
3. **Actionable Marketing:** Because retention is currently low but initial spend is incredibly high, the business must shift its strategy. Marketing teams should focus heavily on onboarding "Recent Customers" and "Promising" users to build buying habits, while deploying aggressive re-engagement campaigns (like massive clearance discounts) to tap into the enormous uncaptured value sitting in the "Hibernating" and "Lost" segments..