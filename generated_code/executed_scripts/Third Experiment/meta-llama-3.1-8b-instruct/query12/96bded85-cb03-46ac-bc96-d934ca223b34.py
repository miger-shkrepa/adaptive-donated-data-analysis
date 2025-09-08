import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

# Iterate over each file in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a directory
    if os.path.isdir(os.path.join(root_dir, filename)):
        # Check if the directory is a JSON file
        if filename.endswith(".json"):
            # Open the JSON file
            with open(os.path.join(root_dir, filename), 'r') as file:
                # Load the JSON data
                data = json.load(file)
                
                # Check if the JSON data contains the required structure
                if 'relationships_permanent_follow_requests' in data:
                    # Iterate over each relationship in the JSON data
                    for relationship in data['relationships_permanent_follow_requests']:
                        # Check if the relationship contains the required data
                        if 'string_list_data' in relationship:
                            # Iterate over each string in the relationship
                            for string in relationship['string_list_data']:
                                # Check if the string contains the required data
                                if 'timestamp' in string and 'value' in string:
                                    # Extract the timestamp and value from the string
                                    timestamp = string['timestamp']
                                    value = string['value']
                                    
                                    # Calculate the week from the timestamp
                                    week = timestamp // 10080 + 1  # 10080 is the number of seconds in a week
                                    
                                    # Append the result to the list
                                    results.append([f"Week {week-1:04d}-{(week-1)%52+1:02d}", 1])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Week", "Messages Sent"])
    writer.writerows(results)