import requests
import time
import pandas as pd

# API details
API_KEY = "589a6d6cedmsh4c0cf365627c871p1156aajsnbebfb7fbb3e5"
BASE_URL = "https://alpha-vantage.p.rapidapi.com/query"
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
}

#fetch data for a company
def fetch_stock_data(symbol):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "datatype": "json"
    }
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json()
        if "Time Series (Daily)" in data:
            daily_data = data["Time Series (Daily)"]
            df = pd.DataFrame.from_dict(daily_data, orient="index")
            df.columns = ["Open", "High", "Low", "Close", "Volume"]
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            return df
        else:
            print(f"No data found for {symbol}")
            return None
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Fetch data for all companies
companies = ["MSFT", "AAPL", "NFLX", "META", "AMZN"]  
all_data = {}

for company in companies:
    print(f"Fetching data for {company}...")
    all_data[company] = fetch_stock_data(company)
    time.sleep(12)  

# Save data to CSV files
for company, data in all_data.items():
    if data is not None:
        data.to_csv(f"{company}_data.csv")
        print(f"Data for {company} saved to {company}_data.csv")
