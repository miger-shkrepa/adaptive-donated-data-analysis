import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as f:
            # Load the JSON data
            data = json.load(f)

            # Check if the JSON data has the required structure
            if "media" in data and "other" in data["media"] and "202501" in data["media"]["other"]:
                # Iterate over the files in the "202501" directory
                for file in data["media"]["other"]["202501"]:
                    # Check if the file is an image file
                    if file.endswith(".jpg"):
                        # Extract the device ID and login time from the file name
                        device_id = file.split("_")[0]
                        login_time = file.split("_")[1].split(".")[0]

                        # Add the result to the list
                        results.append([device_id, login_time])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Device ID", "Login Time"])
    writer.writerows(results)