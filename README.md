# 📌 Gold Price Pipeline

🚀 **Gold Price Pipeline** is an automated ETL pipeline that scrapes gold price data from the web, stores it in **BigQuery**, and visualizes it in **Looker Studio**.

---

## 📂 Project Structure
```
gold_price_pipeline/
│── src/                       # Source code directory
│   ├── main.py                # Main ETL script
│   ├── crawler.py             # Web scraping logic
│── requirements.txt           # Dependencies
│── Dockerfile                 # Docker configuration
│── README.md                  # Project documentation
│── service-account-key.json   # Google Cloud service account key (not included in the repository)
```

---

## Tech Stack
- **Python**: Core programming language for data processing.
- **Web Scraping**: Used to extract gold price data from web sources.
- **Google BigQuery**: Serverless data warehouse for storing extracted data.
- **Looker Studio**: Data visualization tool for creating dashboards and reports.
- **Docker**: Containerization platform for ensuring consistency across environments.
- **Google Cloud Run Jobs**: Serverless execution of containerized ETL tasks.

---

## 🚀 Running the Pipeline

### 1️⃣ Run Locally
#### 📌 Set up the environment
```sh
python3 -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
```
#### 📌 Execute the pipeline
```sh
python src/main.py
```

---

### 2️⃣ Run with Docker
#### 📌 Build Docker image
```sh
docker build -t gold_price_pipeline .
```
#### 📌 Run the container
```sh
docker run --rm gold_price_pipeline
```

---

### 3️⃣ Deploy to Google Cloud Run Jobs
#### 📌 Authenticate with Google Cloud
```sh
gcloud auth login
gcloud config set project gold-price-crawler
gcloud auth configure-docker us-central1-docker.pkg.dev
```

#### 📌 Build and push the Docker image
```sh
docker build -t us-central1-docker.pkg.dev/gold-price-crawler/gold-pipeline-repo/gold_price_pipeline .
docker push us-central1-docker.pkg.dev/gold-price-crawler/gold-pipeline-repo/gold_price_pipeline
```

#### 📌 Update and execute Cloud Run Job
```sh
gcloud run jobs update gold-price-pipeline-job \
    --image us-central1-docker.pkg.dev/gold-price-crawler/gold-pipeline-repo/gold_price_pipeline \
    --region us-central1

gcloud run jobs execute gold-price-pipeline-job --region=us-central1
```

---

## 🛠 BigQuery Configuration
- **Project ID:** `gold-price-crawler`
- **Dataset ID:** `gold_store`
- **Table ID:** `gold_price`

### 📊 Data Schema
| Column   | Type   | Description |
|----------|--------|-------------|
| `type` | `STRING` | Gold type |
| `buy` | `INT64` | Buying price |
| `sell` | `INT64` | Selling price |
| `source` | `STRING` | Data source |
| `datetime` | `DATETIME` | Timestamp |

---

## 📌 Handling `service-account-key.json`
Since `service-account-key.json` should **not** be included in your repository for security reasons, follow these steps:

### Locally
1. **Download your service account key** from the Google Cloud Console.
2. **Move the file** to your project directory:
   ```sh
   mv ~/Downloads/service-account-key.json gold_price_pipeline/
   ```
3. **Use it in your Python code**:
   ```python
   from google.oauth2.service_account import Credentials
   creds = Credentials.from_service_account_file("service-account-key.json")
   ```

### In Docker
Since Docker containers are stateless, you must **pass the key as a secret**:
1. **Run the container with the key mounted:**
   ```sh
   docker run --rm -v $(pwd)/service-account-key.json:/app/service-account-key.json gold_price_pipeline
   ```
2. **For Cloud Run, store the key in Secret Manager:**
   ```sh
   gcloud secrets create gold-price-key --data-file=service-account-key.json
   ```
   Then, mount the secret when running the job.

---

## 📌 Notes
- The pipeline **automatically checks** if today's data is already in **BigQuery** before inserting new records.
- If you get a **pyarrow** error, ensure it’s included in `requirements.txt`:
  ```
  pyarrow==15.0.0
  ```
  Then rebuild the Docker image.

---

📩 **Questions or issues? Feel free to reach out!** 🚀

