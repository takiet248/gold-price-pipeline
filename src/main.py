import pandas as pd
from google.cloud import bigquery
from google.oauth2.service_account import Credentials
from datetime import datetime
from crawler import extract_from_doji, transform_data_doji

# Config BigQuery variable
PROJECT_ID = "gold-price-crawler"
DATASET_ID = "gold_store"
TABLE_ID = "gold_price"
SERVICE_ACCOUNT_FILE = "service-account-key.json"

# Initialize BigQuery client
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
client = bigquery.Client(credentials=creds, project=PROJECT_ID)

def delete_today_data():
    """Deletes today's data from BigQuery before inserting new data."""
    today_str = datetime.today().strftime("%Y-%m-%d")
    query = f"""
        DELETE FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        WHERE DATE(datetime) = '{today_str}'
    """
    print(f"🗑️ Deleting existing data for {today_str} from BigQuery...")
    query_job = client.query(query)
    query_job.result()
    print(f"✅ Data for {today_str} deleted successfully.")

def update_bigquery(df):
    """Clears today's data and loads transformed data into BigQuery."""
    if df.empty:
        print("❌ No new data to update BigQuery.")
        return
    
    delete_today_data()  # Always delete before inserting

    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"  # ✅ FIXED TYPO HERE
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    
    print("📊 Updating BigQuery...")
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()
    print("✅ BigQuery updated successfully.")

def run_etl():
    """Runs the ETL pipeline."""
    print("🚀 Starting ETL process...")

    extracted_df = extract_from_doji("https://baomoi.com/tien-ich/gia-vang-doji.epi")
    transformed_df = transform_data_doji(extracted_df)

    update_bigquery(transformed_df)

    print("✅ ETL process completed successfully.")

if __name__ == "__main__":
    run_etl()
