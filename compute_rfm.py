import pandas as pd
import os

# Define file paths based on the project structure
DATA_DIR = 'data'
CUSTOMERS_FILE = os.path.join(DATA_DIR, 'olist_customers_dataset.csv')
ORDERS_FILE = os.path.join(DATA_DIR, 'olist_orders_dataset.csv')
PAYMENTS_FILE = os.path.join(DATA_DIR, 'olist_order_payments_dataset.csv')
OUTPUT_FILE = os.path.join(DATA_DIR, 'rfm_output.csv')

def score_frequency(x):
    """Custom scoring for Olist's heavily skewed frequency data."""
    if x == 1: return 1
    elif x == 2: return 2
    elif x == 3: return 3
    else: return 4

def assign_business_segment(row):
    """Maps numerical RFM scores to human-readable business categories."""
    r = int(row['R_score'])
    f = int(row['F_score'])
    
    if r >= 3 and f >= 3:
        return 'Champions'
    elif r >= 2 and f >= 3:
        return 'Loyal Customers'
    elif r >= 3 and f == 2:
        return 'Potential Loyalist'
    elif r == 4 and f == 1:
        return 'Recent Customers'
    elif r == 3 and f == 1:
        return 'Promising'
    elif r == 2 and f == 2:
        return 'Needs Attention'
    elif r == 1 and f >= 3:
        return 'At Risk'
    elif r == 2 and f == 1:
        return 'Hibernating'
    else:
        return 'Lost'

def main():
    print("Starting RFM calculation pipeline...")
    
    try:
        # Load only the 3 datasets required for RFM to optimize memory
        print("Loading CSV files from /data...")
        customers = pd.read_csv(CUSTOMERS_FILE)
        orders = pd.read_csv(ORDERS_FILE)
        payments = pd.read_csv(PAYMENTS_FILE)
    except FileNotFoundError as e:
        print(f"ERROR: Could not find data files. Ensure CSVs are in the '{DATA_DIR}' folder.")
        print(e)
        return

    print("Merging datasets...")
    df = orders.merge(customers, on="customer_id")
    df = df.merge(payments, on="order_id")

    print("Formatting dates and calculating snapshot...")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    snapshot_date = df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

    print("Aggregating customer metrics...")
    rfm = df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (snapshot_date - x.max()).days,
        'order_id': 'nunique',
        'payment_value': 'sum'
    }).reset_index()

    rfm.rename(columns={
        'order_purchase_timestamp': 'recency',
        'order_id': 'frequency',
        'payment_value': 'monetary'
    }, inplace=True)

    print("Assigning RFM scores...")
    rfm['R_score'] = pd.qcut(rfm['recency'], q=4, labels=[4, 3, 2, 1])
    rfm['M_score'] = pd.qcut(rfm['monetary'], q=4, labels=[1, 2, 3, 4])
    rfm['F_score'] = rfm['frequency'].apply(score_frequency)

    # Combined score
    rfm['RFM_segment'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)

    print("Mapping business segments...")
    rfm['Customer_Segment'] = rfm.apply(assign_business_segment, axis=1)

    print("Exporting data for FastAPI...")
    # Keep only the essential columns mapped exactly to your notebook variables
    lookup_df = rfm[['customer_unique_id', 'R_score', 'F_score', 'M_score', 'RFM_segment', 'Customer_Segment']]
    lookup_df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"Pipeline complete! Output saved to {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()