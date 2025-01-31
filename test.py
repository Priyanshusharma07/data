from redis_utils import write_to_redis, read_from_redis  # Importing the Redis utility

# Test writing data
test_key = "api_response:http://127.0.0.1:5000/circuit"
test_value = {"message": "Hello from Redis!"}

# write_to_redis(test_key, test_value)

# Test reading data
print("🔹 Fetching data from Redis...")
result = read_from_redis(test_key)
print("✅ Read from Redis:", result)
