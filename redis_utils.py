import redis # type: ignore
import json

# Initialize Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# def write_to_redis(key, value):
#     try:
#         # Convert dictionary to JSON string before storing
#         redis_client.set(key, json.dumps(value), ex=600)  # Expiration: 10 min
#         print(f"Data written: {key} -> {value}")
#     except Exception as e:
#         print(f"Error writing to Redis: {e}")

# def write_to_redis(key, value):
#     try:
#         client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
#         client.set(key, json.dumps(value))  # Convert dict to string before storing
#         print(f"Data written to Redis: {key}")
#     except Exception as e:
#         print(f" Error writing to Redis: {e}")


# Initialize Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379)

def write_to_redis(key, data):
    try:
        # Connect to Redis
        client = redis.StrictRedis(host='localhost', port=6379)
        
        # Convert data to JSON string
        json_data = json.dumps(data)
        
        # Write data to Redis
        client.set(key, json_data)
        
        print(f"Data written to Redis with key: {key}")
    except Exception as e:
        print(f"Error writing to Redis: {e}")
def read_from_redis(key):
    """Retrieve data from Redis."""
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)  # Convert JSON string back to dictionary
        else:
            print(f" No data found for key: {key}")
            return None
    except Exception as e:
        print(f"Error reading from Redis: {e}")
        return None



# print(read_from_redis("api_response:stocktrade"))
