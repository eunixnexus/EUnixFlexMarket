import redis
import time
import os
import pandas as pd
import uuid
import json
import csv
#print()


class ProcessSlots:

    def __init__(self, data, startSlot = None, steps = 96):
        """TODO: to be defined."""
        self.data = data
        self.startSlot  = startSlot
        self.Nstep = steps
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.red_cl = redis.StrictRedis(host='localhost', port=6379, db=0)
        action = "Registration open"
        unique_id = str(uuid.uuid4())
        message = f"{action}:{unique_id}"
        self.r.publish('registration_channel', message) 
        r_data = {
            "action": "Registration open",
            "platID": unique_id,
              }  
        self.send_to_redis("registraion", r_data)
        
        print("Regiistration channel opened")
 
       


    def get_timeSlot(self):
    
        # Convert the Datetime column and startSlot to datetime objects
        self.data["Datetime"] = pd.to_datetime(self.data["Datetime"], format="%Y-%m-%dT%H:%M")
        startSlot_datetime = pd.to_datetime(self.startSlot, format="%Y-%m-%dT%H:%M")
    
        # Find rows matching the startSlot
        matches = self.data[self.data["Datetime"] == startSlot_datetime]
    
        if matches.empty:
            raise ValueError(f"Datetime {self.startSlot} not found in the data.")
    
        # Find the starting index
        start_index = matches.index[0]
    
        # Select rows starting from the index up to n_slots
        selected_rows = self.data.iloc[start_index : start_index + self.Nstep]
    
        return selected_rows


    def send_to_redis(self, inst, data):
        # Push to Redis
        self.red_cl.rpush(inst, json.dumps(data))

        # Set expiration (e.g., 1 hour = 3600 seconds)
        self.red_cl.expire(inst, 300) 





    def publish_slot(self, slot_time, step, msg="end"):
        time.sleep(0.5)
        if step == self.Nstep:
            self.r.publish('slot_channel', "end")
            print("Main Script: Sending termination signal")
        else:
            self.r.publish('slot_channel', msg+" Slot "+ slot_time)  # Publish step
            print(f"Market slot {slot_time} {msg}")
            #time.sleep(1)  # Simulate delay or processing time
            
  
  
    def read_from_redis(self, key):
        # Retrieve all the data from the "time_series_data" list (or set a range)
        data_list = self.red_cl.lrange(key, 0, -1)  # 0 to -1 to get all elements
        if not data_list:
            print("No data found in the Redis list.")
            return
        # Process each entry in the list
        data_dict = [json.loads(item.decode('utf-8')) for item in data_list]
        #df = pd.DataFrame(parsed_data)
        for item in data_list:
            self.red_cl.lrem(key, 1, item) #Delete read data
            
        return data_dict        
                


    def delete_from_redis(self, key):
        """
        Deletes data associated with a given key from Redis.

        """
        # Connect to Redis
        
        # Check if the key exists
        if self.r.exists(key):
            self.r.delete(key)
            print(f"Key '{key}' deleted from Redis.")
            return True
        else:
            print(f"Key '{key}' does not exist in Redis.")
            return False


    def json_to_csv(self, json_data, output_file):
        try:
            # Parse the input JSON string
            parsed_data = []
            
            for item in json_data:
                # Convert the string item to a list of dictionaries
                parsed_item = json.loads(item)
                # Append the parsed item to the main list
                parsed_data.extend(parsed_item)
            
            # Create a DataFrame from the parsed data
            df_r = pd.DataFrame(parsed_data)
            
            # Save the DataFrame to a CSV file
            df_r.to_csv(output_file, index=False)
            print(f"Result data successfully saved to {output_file}")
        
        except Exception as e:
            print(f"Error while converting JSON to CSV: {e}")





# Example Usage
#delete_from_redis("example_key")

