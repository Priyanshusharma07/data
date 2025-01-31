import json
from redis_utils import read_from_redis  # Import the correct read function

def fetch_all_data():
    """Fetch all stored API responses from Redis."""
    keys = ["api_response:http://127.0.0.1:5000/advance", "api_response:http://127.0.0.1:5000/fifty", "api_response:http://127.0.0.1:5000/stocktrade", "api_response:http://127.0.0.1:5000/circuit"]
    
    for key in keys:
        data = read_from_redis(key)
        if data:
            print(f"📌 Stored Data [{key}]:", json.dumps(data, indent=4))
        else:
            print(f"⚠️ No stored data for {key}")

def fetch_specific_data():
    """Allow user to fetch specific API response from Redis."""
    key_map = {
        "1": "api_response:http://127.0.0.1:5000/advance",
        "2": "api_response:http://127.0.0.1:5000/fifty",
        "3": "api_response:http://127.0.0.1:5000/stocktrade",
        "4": "api_response:http://127.0.0.1:5000/circuit"
    }

    print("\n📌 Choose API Data to Retrieve:")
    print("1️⃣ Advance")
    print("2️⃣ Fifty")
    print("3️⃣ Stock Trade")
    print("4️⃣ Circuit")
    choice = input("Enter your choice (1-4): ")

    key = key_map.get(choice)
    if key:
        data = read_from_redis(key)
        if data:
            print(f"✅ Retrieved Data [{key}]:\n{json.dumps(data, indent=4)}")
        else:
            print("⚠️ No data found for the selected API.")
    else:
        print("❌ Invalid choice!")

def menu():
    """Menu-driven interface to access stored data."""
    while True:
        print("\n🔹 **DATA ACCESS MENU** 🔹")
        print("1️⃣ Fetch All API Data")
        print("2️⃣ Fetch Specific API Data")
        print("3️⃣ Exit")

        option = input("Choose an option (1-3): ")

        if option == "1":
            fetch_all_data()
        elif option == "2":
            fetch_specific_data()
        elif option == "3":
            print("👋 Exiting... Have a great day!")
            break
        else:
            print("❌ Invalid option! Please choose again.")

if __name__ == "__main__":
    menu()



