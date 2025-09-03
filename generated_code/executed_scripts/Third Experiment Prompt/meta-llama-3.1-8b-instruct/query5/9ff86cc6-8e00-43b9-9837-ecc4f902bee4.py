import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the output CSV file
output_csv = "query_responses/results.csv"

# Initialize the CSV writer
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Device ID", "Login Time"])

    # Iterate over the 'your_instagram_activity' directory
    for device in os.listdir(root_dir + "/your_instagram_activity"):
        device_path = root_dir + "/your_instagram_activity/" + device
        if os.path.isdir(device_path):
            # Iterate over the 'likes' and 'saved' directories
            for activity in os.listdir(device_path):
                activity_path = device_path + "/" + activity
                if os.path.isdir(activity_path):
                    # Iterate over the JSON files
                    for file in os.listdir(activity_path):
                        file_path = activity_path + "/" + file
                        if file.endswith(".json"):
                            try:
                                # Load the JSON file
                                with open(file_path, 'r') as json_file:
                                    data = json.load(json_file)

                                # Extract the login time and device ID
                                login_time = None
                                device_id = None
                                for item in data['structure'][file[:-5]]:
                                    if 'timestamp' in item:
                                        login_time = item['timestamp']
                                    if 'href' in item:
                                        device_id = item['href']

                                # Write the data to the output CSV file
                                if login_time is not None and device_id is not None:
                                    writer.writerow([device_id, login_time])
                            except json.JSONDecodeError as e:
                                print(f"Error: Failed to parse JSON file {file_path}: {e}")
                            except KeyError as e:
                                print(f"Error: Missing key in JSON file {file_path}: {e}")