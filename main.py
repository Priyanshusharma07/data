# import schedule
# import time
# import requests
# import datetime
# from redis_utils import write_to_redis  # Importing the Redis utility
# from threading import Timer

# def is_market_open():
#     """Check if the market is open by hitting the API."""
#     try:
#         response = requests.get("http://localhost:3001/market/symbol?symbol=tatasteel&apiKey=07BQKTn3fgUcM3Z8MiY3aRjytlXAQ8c1")
#         response.raise_for_status()
#         data = response.json()
#         market_open = data.get("is_market_open", False)
#         print(f"Market open status: {market_open}")
#         return market_open
#     except requests.RequestException as e:
#         print(f"Error checking market status: {e}")
#         return False

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
#             print(f"Success: {url}, Response: {data}")
#             # Store response in Redis
#             key = f"api_response:{url}"
#             write_to_redis(key, str(data))
#         except requests.RequestException as e:
#             print(f"Failed to hit {url}: {e}")

# def schedule_market_tasks():
#     """Schedule tasks to hit APIs every 30 minutes between 9:20 AM and 3:30 PM if the market is open."""
#     start_time = datetime.time(9, 20)
#     end_time = datetime.time(23, 59)

#     while True:
#         current_time = datetime.datetime.now().time()

#         if start_time <= current_time <= end_time:
#             print(f"Hitting APIs at {datetime.datetime.now()}...")
#             hit_several_apis()
#             time.sleep(5 * 60)  # Wait for 30 minutes
#         else:
#             print(f"Market closed or outside scheduled hours. Waiting until next schedule...")
#             break

# def task():
#     """Run the daily task to check market status and proceed accordingly."""
#     print(f"Task started at {datetime.datetime.now()}")
#     if is_market_open():
#         print("Market is open. Scheduling API hits...")
#         schedule_market_tasks()
#     else:
#         print("Market is closed. Waiting for the next day.")

# # Schedule the task to run daily at 9:20 AM
# schedule.every().day.at("22:52").do(task)

# print("Scheduler is running. Waiting for the next scheduled task...")

# while True:
#     schedule.run_pending()
#     time.sleep(1)

# ------------------------------------------------

# import schedule
# import time
# import requests
# from datetime import datetime, time as dtime

# # List to track APIs that fail to return valid data
# failed_apis = []

# def is_market_open():
#     """Check if the market is open by hitting the API."""
#     try:
#         response = requests.get("http://13.203.2.232/market/symbol?symbol=tatasteel&apiKey=07BQKTn3fgUcM3Z8MiY3aRjytlXAQ8c1")
#         response.raise_for_status()
#         data = response.json()
#         market_open = data.get("is_market_open", False)
#         print(f"Market open status: {market_open}")
#         return market_open
#     except requests.RequestException as e:
#         print(f"Error checking market status: {e}")
#         return False

# def fetch_api_with_retries(url, retries=3, delay=5):
#     """Fetch data from an API with retries."""
#     for attempt in range(retries):
#         try:
#             print(f"Fetching {url} (Attempt {attempt + 1}/{retries})...")
#             response = requests.get(url)
#             response.raise_for_status()
#             data = response.json()
#             if not data:
#                 raise ValueError("Empty response")
#             return data
#         except (requests.RequestException, ValueError) as e:
#             print(f"Error fetching {url}: {e}")
#             if attempt < retries - 1:
#                 time.sleep(delay)
#     print(f"Failed to fetch data from {url} after {retries} attempts.")
#     return None

# def hit_several_apis():
#     """Hit several APIs and process their responses."""
#     global failed_apis
#     api_endpoints = [
#         "http://127.0.0.1:5000/advance",
#         "http://127.0.0.1:5000/fifty",
#         "http://127.0.0.1:5000/stocktrade",
#         "http://127.0.0.1:5000/circuit",
#     ]

#     for url in api_endpoints:
#         data = fetch_api_with_retries(url)
#         if data:
#             # Check if all values in the response are non-empty
#             if all(value != '' for value in data.values()):
#                 print(f"Success: {url}, Response: {data}")
#             else:
#                 print(f"Response contains empty values. Adding {url} to failed APIs.")
#                 failed_apis.append(url)
#         else:
#             print(f"Adding {url} to failed APIs due to failed fetch.")
#             failed_apis.append(url)

# def retry_failed_apis():
#     """Retry fetching data for previously failed APIs."""
#     global failed_apis
#     if not failed_apis:
#         print("No failed APIs to retry.")
#         return

#     print("Retrying failed APIs...")
#     remaining_failed_apis = []

#     for url in failed_apis:
#         data = fetch_api_with_retries(url)
#         if data:
#             print(f"Success on retry: {url}, Response: {data}")
#         else:
#             print(f"Still failing: {url}. Adding back to retry list.")
#             remaining_failed_apis.append(url)

#     failed_apis = remaining_failed_apis

# def schedule_market_tasks():
#     """Schedule API hits between 9:20 AM and 3:30 PM if the market is open."""
#     start_time = dtime(15, 40)
#     end_time = dtime(15, 30)

#     while True:
#         current_time = datetime.now().time()
#         if start_time <= current_time <= end_time:
#             print(f"Hitting APIs at {datetime.now()}...")
#             hit_several_apis()
#             retry_failed_apis()
#             time.sleep(5 * 60)
#         else:
#             print("Market closed or outside scheduled hours.")
#             break

# def task():
#     """Daily task to check market status and hit APIs."""
#     print(f"Task started at {datetime.now()}")
#     if is_market_open():
#         print("Market is open. Scheduling API hits...")
#         schedule_market_tasks()
#     else:
#         print("Market is closed. Waiting for the next day.")

# # Schedule the task
# schedule.every().day.at("15:36").do(task)

# print("Scheduler is running. Waiting for the next scheduled task...")

# while True:
#     schedule.run_pending()
#     time.sleep(1)



# import schedule # type: ignore
# import time
# import requests # type: ignore
# import datetime
# from redis_utils import write_to_redis  # Importing the Redis utility
# from threading import Timer

# def is_market_open():
#     """Check if the market is open by hitting the API."""
#     try:
#         response = requests.get("http://localhost:3001/market/symbol?symbol=tatasteel&apiKey=07BQKTn3fgUcM3Z8MiY3aRjytlXAQ8c1")
#         response.raise_for_status()
#         data = response.json()
#         market_open = data.get("is_market_open", False)
#         print(f"Market open status: {market_open}")
#         return market_open
#     except requests.RequestException as e:
#         print(f"Error checking market status: {e}")
#         return False


# def is_valid_data(data):
#     """Check if the data is valid (not empty or default values)."""
#     invalid_values = [
#         {'fifty_two_week_high': '', 'fifty_two_week_low': ''},
#         {'advance': '', 'decline': '', 'unchanged': ''},
#         {'Stock_trade': ''},
#         {'Lower_circuit': '', 'Upper_circuit': ''}
#     ]

#     return data not in invalid_values  # Return True only if data is not in invalid values

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

#             if is_valid_data(data):  # Check if data is valid
#                 print(f"Success: {url}, Response: {data}")

#                 # Extract the last part of the URL or use another method to create a single-word key
#                 key = f"{url.split('/')[-1]}"  # Using the last part of the URL as key

#                 write_to_redis(key, str(data))  # Store response in Redis
#             else:
#                 print(f"Skipping invalid response from {url}: {data}")

#         except requests.exceptions.RequestException as e:
#             print(f"Request failed for {url}: {e}")


# # def hit_several_apis():
# #     """Hit several APIs and store their responses in Redis."""
# #     api_endpoints = [
# #         "http://127.0.0.1:5000/advance",
# #         "http://127.0.0.1:5000/fifty",
# #         "http://127.0.0.1:5000/stocktrade",
# #         "http://127.0.0.1:5000/circuit"
# #     ]

# #     for url in api_endpoints:
# #         try:
# #             response = requests.get(url)
# #             response.raise_for_status()
# #             data = response.json()
# #             print(data)
# #             if(data!="{'fifty_two_week_high': '', 'fifty_two_week_low': ''}" or data!="{'advance': '', 'decline': '', 'unchanged': ''}" or data!="{'Stock_trade': ''}" or data!="{'Lower_circuit': '', 'Upper_circuit': ''}"):
# #                 print(f"Success: {url}, Response: {data}")

# #                 # Extract the last part of the URL or use another method to create a single-word key
# #                 key = f"api_response:{url.split('/')[-1]}"  # Using the last part of the URL as key
# #                 # print(f"Writing data to Redis with key {key}")

# #                 write_to_redis(key, str(data))  # Store response in Redis

# #         except requests.exceptions.RequestException as e:
# #             print(f"Request failed for {url}: {e}")

# def schedule_market_tasks():
#     """Schedule tasks to hit APIs every 30 minutes between 9:20 AM and 3:30 PM if the market is open."""
#     start_time = datetime.time(0, 5)
#     end_time = datetime.time(23, 59)

#     while True:
#         current_time = datetime.datetime.now().time()

#         if start_time <= current_time <= end_time:
#             print(f"Hitting APIs at {datetime.datetime.now()}...")
#             hit_several_apis()
#             time.sleep(5 * 60)  # Wait for 30 minutes
#         else:
#             print(f"Market closed or outside scheduled hours. Waiting until next schedule...")
#             break

# def task():
#     """Run the daily task to check market status and proceed accordingly."""
#     print(f"Task started at {datetime.datetime.now()}")
#     if is_market_open():
#         print("Market is open. Scheduling API hits...")
#         schedule_market_tasks()
#     else:
#         print("Market is closed. Waiting for the next day.")

# # Schedule the task to run daily at 9:20 AM
# schedule.every().day.at("16:22").do(task)

# print("Scheduler is running. Waiting for the next scheduled task...")

# while True:
#     schedule.run_pending()
#     time.sleep(1)


import schedule
import time
import requests
import datetime
from redis_utils import write_to_redis  # Importing the Redis utility
from threading import Thread

def is_market_open():
    """Check if the market is open by hitting the API."""
    try:
        response = requests.get("http://13.203.2.232/market/symbol?symbol=tatasteel&apiKey=07BQKTn3fgUcM3Z8MiY3aRjytlXAQ8c1")
        response.raise_for_status()
        data = response.json()
        market_open = data.get("is_market_open", False)
        print(f"Market open status: {market_open}")
        market_open='true'
        return market_open
    except requests.RequestException as e:
        print(f"Error checking market status: {e}")
        return False

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
            print(f"Success: {url}, Response: {data}")
            key = f"api_response:{url.split('/')[-1]}"  # Use last part of URL as key
            write_to_redis(key, str(data))
        except requests.RequestException as e:
            print(f"Failed to hit {url}: {e}")

def run_market_tasks():
    """Continuously check market status and hit APIs if open."""
    while True:
        if is_market_open():
            print(f"Market is open. Hitting APIs at {datetime.datetime.now()}...")
            hit_several_apis()
            time.sleep(1000)  # Wait 5 minutes before the next run
        else:
            print("Market is closed. Retrying in 5 minutes...")
            time.sleep(2000)  # Check again after 5 minutes

def start_task():
    """Start the market monitoring task in a separate thread."""
    task_thread = Thread(target=run_market_tasks)
    task_thread.daemon = True
    task_thread.start()

# Start task immediately upon running the script
start_task()

# Keep script running to maintain the scheduled task
while True:
    time.sleep(1)
