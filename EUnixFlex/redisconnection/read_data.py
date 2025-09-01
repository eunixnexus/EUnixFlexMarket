import redis
import json

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def read_from_redis():
    # Retrieve all the data from the "time_series_data" list (or set a range)
    data_list = redis_client.lrange("time_series_data", 0, -1)  # 0 to -1 to get all elements

    if not data_list:
        print("No data found in the Redis list.")
        return

    # Process each entry in the list
    for index, data in enumerate(data_list):
        # Convert each JSON string back to a Python dictionary
        data_dict = json.loads(data.decode('utf-8'))
        print(f"Data {index + 1}: {data_dict}")

if __name__ == "__main__":
    # Read data from Redis
    read_from_redis()