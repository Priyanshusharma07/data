
import schedule # type: ignore
import time
import requests # type: ignore
import datetime
from redis_utils import write_to_redis  # Importing the Redis utility
from threading import Timer

def is_market_open():
    """Check if the market is open by hitting the API."""
    try:
        response = requests.get("http://localhost:3001/market/symbol?symbol=tatasteel&apiKey=07BQKTn3fgUcM3Z8MiY3aRjytlXAQ8c1")
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

                # Extract the last part of the URL or use another method to create a single-word key
                key = f"{url.split('/')[-1]}"  # Using the last part of the URL as key

                write_to_redis(key, str(data))  # Store response in Redis
            else:
                print(f"Skipping invalid response from {url}: {data}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed for {url}: {e}")


# def hit_several_apis():
#     """Hit several APIs and store their responses in Redis."""
#     api_endpoints = [
#         "http://127.0.0.1:5000/advance",
#         "http://127.0.0.1:5000/fifty",
#         "http://127.0.0.1:5000/stocktrade",
#         "http://127.0.0.1:5000/circuit"
#     ]

#     for url in api_endpoints:
#         try:
#             response = requests.get(url)
#             response.raise_for_status()
#             data = response.json()
#             print(data)
#             if(data!="{'fifty_two_week_high': '', 'fifty_two_week_low': ''}" or data!="{'advance': '', 'decline': '', 'unchanged': ''}" or data!="{'Stock_trade': ''}" or data!="{'Lower_circuit': '', 'Upper_circuit': ''}"):
#                 print(f"Success: {url}, Response: {data}")

#                 # Extract the last part of the URL or use another method to create a single-word key
#                 key = f"api_response:{url.split('/')[-1]}"  # Using the last part of the URL as key
#                 # print(f"Writing data to Redis with key {key}")

#                 write_to_redis(key, str(data))  # Store response in Redis

#         except requests.exceptions.RequestException as e:
#             print(f"Request failed for {url}: {e}")

def schedule_market_tasks():
    """Schedule tasks to hit APIs every 30 minutes between 9:20 AM and 3:30 PM if the market is open."""
    start_time = datetime.time(0, 5)
    end_time = datetime.time(23, 59)

    while True:
        current_time = datetime.datetime.now().time()

        if start_time <= current_time <= end_time:
            print(f"Hitting APIs at {datetime.datetime.now()}...")
            hit_several_apis()
            time.sleep(5 * 60)  # Wait for 30 minutes
        else:
            print(f"Market closed or outside scheduled hours. Waiting until next schedule...")
            break

def task():
    """Run the daily task to check market status and proceed accordingly."""
    print(f"Task started at {datetime.datetime.now()}")
    if is_market_open():
        print("Market is open. Scheduling API hits...")
        schedule_market_tasks()
    else:
        print("Market is closed. Waiting for the next day.")

# Schedule the task to run daily at 9:20 AM
schedule.every().day.at("12:20").do(task)

print("Scheduler is running. Waiting for the next scheduled task...")

while True:
    schedule.run_pending()
    time.sleep(1)
