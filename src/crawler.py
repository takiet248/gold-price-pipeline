import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def extract_from_doji(url):
    """
    Extracts gold price data from the Doji website and returns a pandas DataFrame.
    
    Args:
        url (str): The URL of the Doji gold price page.

    Returns:
        pd.DataFrame: A DataFrame containing extracted gold price data.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data from {url}: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")
    
    if not tables:
        print("❌ No tables found on the webpage.")
        return pd.DataFrame()

    # Extract headers
    headers = [th.text.strip() for th in tables[0].find_all("th") if th.text.strip()]
    
    # Extract data rows
    data = [
        [td.text.strip() for td in row.find_all("td")[1:]]
        for row in tables[0].find_all("tr")[1:]
    ]
    
    df = pd.DataFrame(data, columns=headers)
    print(f"✅ Successfully extracted data from Doji: {df.shape}")
    return df

def transform_data_doji(df):
    """
    Transforms extracted gold price data into a clean DataFrame.

    Args:
        df (pd.DataFrame): Raw extracted gold price data.

    Returns:
        pd.DataFrame: Cleaned and formatted gold price data.
    """
    if df.empty:
        print("❌ No data to transform.")
        return df

    df = df.rename(columns={'Loại vàng': 'type', 'Giá mua (VNĐ)': 'buy', 'Giá bán (VNĐ)': 'sell'})

    df['type'] = df['type'].str.replace('- Bán Lẻ', '').str.replace('(Hưng Thịnh Vượng)', '').str.strip()
    df['buy'] = df['buy'].str.replace(',', '').astype(int)
    df['sell'] = df['sell'].str.replace(',', '').astype(int)
    df['source'] = 'Doji'
    df['datetime'] = dt.datetime.today().strftime('%Y-%m-%d')
    df["datetime"] = pd.to_datetime(df["datetime"])
    print(f"✅ Data transformation completed: {df.shape}")
    return df
