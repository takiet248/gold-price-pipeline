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

def get_latest_date_from_bigquery():
    """Fetches the latest date (truncated) from BigQuery."""
    query = f"""
        SELECT DATE(MAX(datetime)) as latest_date FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    """
    query_job = client.query(query)
    results = query_job.result()
    for row in results:
        return row.latest_date  #return format YYYY-MM-DD
    return None


def should_run_pipeline():
    """Checks if the latest date in BigQuery is today. If yes, skip the ETL process."""
    latest_date_in_bq = get_latest_date_from_bigquery()
    today_date = datetime.today().date()
    
    if latest_date_in_bq and latest_date_in_bq == today_date:
        print(f"⏭️ Pipeline skipped: Data for {today_date} is already in BigQuery.")
        return False
    return True

def update_bigquery(df):
    """Loads transformed data directly into BigQuery."""
    if df.empty:
        print("❌ No new data to update BigQuery.")
        return
    
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    
    print("📊 Updating BigQuery...")
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()
    print("✅ BigQuery updated successfully.")

def run_etl():
    """Runs the ETL pipeline only if today's data is not in BigQuery."""
    print("🚀 Starting ETL process...")

    if not should_run_pipeline():
        return  # Skip if today's data is already in BigQuery
    
    extracted_df = extract_from_doji("https://baomoi.com/tien-ich/gia-vang-doji.epi")
    transformed_df = transform_data_doji(extracted_df)
    if not transformed_df.empty:
        update_bigquery(transformed_df)

    print("✅ ETL process completed successfully.")

if __name__ == "__main__":
    run_etl()