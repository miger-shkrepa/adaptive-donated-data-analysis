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
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Load followers data
try:
    followers_data = load_data(os.path.join(root_dir, "connections/followers_and_following/followers_1.json"))
    if 'string_list_data' in followers_data and isinstance(followers_data['string_list_data'], list):
        followers = [item['value'] for item in followers_data['string_list_data']]
except (FileNotFoundError, ValueError) as e:
    print(e)

# Load following data
try:
    following_data = load_data(os.path.join(root_dir, "connections/followers_and_following/following.json"))
    if 'relationships_following' in following_data and isinstance(following_data['relationships_following'], list):
        following = [item['value'] for item in following_data['relationships_following'][0]['string_list_data']]
except (FileNotFoundError, ValueError) as e:
    print(e)

# Find profiles that the user follows but do not follow back
unfollowed_back = [profile for profile in following if profile not in followers]

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Profile'])
    for profile in unfollowed_back:
        writer.writerow([profile])