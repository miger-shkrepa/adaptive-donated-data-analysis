import csv
import os

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the profiles
profiles = []

# Iterate over the JSON files in the 'following.json' file
for following_file in os.listdir(root_dir):
    if following_file.endswith('following.json'):
        with open(os.path.join(root_dir, following_file), 'r') as f:
            following_data = eval(f.read())
            for relationship in following_data['following.json']['structure']['relationships_following']:
                # Check if the 'string_list_data' key exists in the relationship dictionary
                if 'string_list_data' in relationship:
                    # Iterate over the 'string_list_data' list
                    for data in relationship['string_list_data']:
                        # Check if the 'href' key exists in the data dictionary
                        if 'href' in data:
                            # Check if the 'timestamp' key exists in the data dictionary
                            if 'timestamp' in data:
                                # Check if the 'value' key exists in the data dictionary
                                if 'value' in data:
                                    # Append the 'value' to the profiles list
                                    profiles.append(data['value'])

# Check if the 'follow_requests_you've_received.json' file exists
if os.path.exists(os.path.join(root_dir, 'follow_requests_youve_received.json')):
    with open(os.path.join(root_dir, 'follow_requests_youve_received.json'), 'r') as f:
        follow_requests_data = eval(f.read())
        for relationship in follow_requests_data['follow_requests_youve_received.json']['structure']['relationships_follow_requests_received']:
            # Check if the 'string_list_data' key exists in the relationship dictionary
            if 'string_list_data' in relationship:
                # Iterate over the 'string_list_data' list
                for data in relationship['string_list_data']:
                    # Check if the 'href' key exists in the data dictionary
                    if 'href' in data:
                        # Check if the 'timestamp' key exists in the data dictionary
                        if 'timestamp' in data:
                            # Check if the 'value' key exists in the data dictionary
                            if 'value' in data:
                                # Append the 'value' to the profiles list
                                profiles.append(data['value'])

# Write the profiles list to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Profile'])  # Write the column headers
    for profile in profiles:
        writer.writerow([profile])  # Write each profile to a new row