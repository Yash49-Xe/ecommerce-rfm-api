# 🛒 E-Commerce Customer RFM Segmentation API

An end-to-end data science pipeline and REST API that processes over 100,000 real-world e-commerce transactions to categorize customers into actionable business segments using **RFM (Recency, Frequency, Monetary)** analysis.

## 🚀 Project Overview

In e-commerce, not all customers are equal. This project takes raw, relational database exports and transforms them into a high-speed, scalable API that marketing teams can use to drive targeted campaigns. 

Instead of treating all users the same, this system evaluates purchasing behavior to instantly classify users into segments like **"Champions"**, **"At Risk"**, or **"Hibernating"**, providing automated, data-driven marketing recommendations for each.

## 🛠️ Tech Stack

* **Data Processing:** Python, Pandas
* **Backend / API:** FastAPI, Uvicorn
* **Exploratory Data Analysis:** Jupyter Notebooks, Matplotlib, Seaborn
* **Data Source:** [Brazilian E-Commerce Public Dataset by Olist (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

## 📁 Project Structure

```text
ecommerce-rfm-api/
│
├── data/                            # Raw datasets and pre-calculated lookups (ignored by Git)
├── notebooks/
│   └── 01_rfm_exploratory_analysis.ipynb  # Initial EDA, Pandas logic, and Visualizations
│
├── compute_rfm.py                   # Scheduled backend script to process CSVs into RFM scores
├── main.py                          # FastAPI application serving the insights
├── requirements.txt                 # Python dependencies
└── README.md

⚙️ How to Run Locally
1. Clone the repository
Bash

git clone [https://github.com/Yash49-Xe/ecommerce-rfm-api.git]
cd ecommerce-rfm-api

2. Install dependencies
Bash

pip install -r requirements.txt

3. Add the Data

Download the Olist Dataset from Kaggle and place the following three files into the /data directory:

    olist_customers_dataset.csv

    olist_orders_dataset.csv

    olist_order_payments_dataset.csv

4. Run the Data Pipeline

Execute the data engineering script to merge the tables, calculate the RFM scores, and generate the lightweight rfm_output.csv lookup table.
Bash

python compute_rfm.py

5. Start the API Server
Bash

uvicorn main:app --reload

The API will be live at http://127.0.0.1:8000.
You can view the interactive API documentation (Swagger UI) at http://127.0.0.1:8000/docs.



📡 API Endpoints
GET /api/v1/customer-segment/{customer_unique_id}

Returns the calculated RFM scores, the business segment classification, and a tailored marketing strategy for the requested customer.

Example Response:
JSON

{
  "customer_id": "8d50f5eadf50201ccdcedfb4e2ac8455",
  "rfm_scores": {
    "recency_score": 4,
    "frequency_score": 1,
    "monetary_score": 3
  },
  "segment_code": "413",
  "segment_name": "Recent Customers",
  "recommended_action": "Send a welcome onboarding sequence or a simple customer satisfaction feedback survey."
}


📈 Business Insights

(See the Jupyter Notebook for full visualizations)

By mapping the mathematical quantiles to business logic, we uncovered that out of ~100k unique customers, over 95% made only a single purchase. This extreme right-skew in the Frequency metric required custom scoring functions to properly isolate the highly valuable Champions (top spenders who return often) from the massive pool of one-off Recent Customers.