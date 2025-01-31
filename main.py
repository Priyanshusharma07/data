import schedule  # type: ignore
import time
import requests  # type: ignore
import datetime
from redis_utils import write_to_redis  # Importing the Redis utility

def is_market_open():
    """Check if the market is open by hitting the API."""
    try:
        response = requests.get("http://13.203.2.232/market/symbol?symbol=tatasteel&apiKey=07BQKTn3fgUcM3Z8MiY3aRjytlXAQ8c1")
        response.raise_for_status()
        data = response.json()
        market_open = data.get("is_market_open", False)
        print(f"Market open status: {market_open}")
        return market_open
    except requests.RequestException as e:
        print(f"Error checking market status: {e}")
        return False

def is_valid_data(data):
    """Check if the data is valid (not empty or default values)."""
    invalid_values = [
        {'fifty_two_week_high': '', 'fifty_two_week_low': ''},
        {'advance': '', 'decline': '', 'unchanged': ''},
        {'Stock_trade': ''},
        {'Lower_circuit': '', 'Upper_circuit': ''}
    ]
    return data not in invalid_values  # Return True only if data is not in invalid values

def hit_several_apis():
    """Hit several APIs and store their responses in Redis."""
    api_endpoints = [
        "http://127.0.0.1:5000/advance",
        "http://127.0.0.1:5000/fifty",
        "http://127.0.0.1:5000/stocktrade",
        "http://127.0.0.1:5000/circuit"
    ]

    for url in api_endpoints:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if is_valid_data(data):  # Check if data is valid
                print(f"Success: {url}, Response: {data}")
                key = f"{url.split('/')[-1]}"  # Using the last part of the URL as key
                write_to_redis(key, str(data))  # Store response in Redis
            else:
                print(f"Skipping invalid response from {url}: {data}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed for {url}: {e}")

def run_market_tasks():
    """Continuously check market status and hit APIs when the market is open."""
    market_start = datetime.time(9, 20)
    market_end = datetime.time(15, 30)

    while True:
        now = datetime.datetime.now().time()

        if market_start <= now <= market_end:  # Market time range
            if is_market_open():
                print(f"Market is open at {datetime.datetime.now()}, hitting APIs...")
                hit_several_apis()
                time.sleep(5 * 60)  # Wait for 5 minutes before next API call
            else:
                print("Market is closed, rechecking in 15 minutes...")
                time.sleep(15 * 60)  # Check again after 15 minutes
        else:
            print("Outside market hours. Checking again in 30 minutes...")
            time.sleep(30 * 60)  # Wait for 30 minutes before rechecking market status

if __name__ == "__main__":
    print("Market Monitoring System Started...")
    run_market_tasks()
