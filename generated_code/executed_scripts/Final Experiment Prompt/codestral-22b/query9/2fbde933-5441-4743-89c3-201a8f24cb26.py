import json
import csv
import os

# Declare the root directory
root_dir = "root_dir"

# Initialize empty lists to store followers and following
followers = []
following = []

# Function to load data from a JSON file
def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Load followers data
followers_data = load_data(os.path.join(root_dir, "connections/followers_and_following/followers_1.json"))
if followers_data:
    followers = [item['value'] for item in followers_data['string_list_data']]

# Load following data
following_data = load_data(os.path.join(root_dir, "connections/followers_and_following/following.json"))
if following_data:
    following = [item['value'] for item in following_data['relationships_following'][0]['string_list_data']]

# Find profiles that the user follows but do not follow back
unfollowed_back = [profile for profile in following if profile not in followers]

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Profile'])
    for profile in unfollowed_back:
        writer.writerow([profile])