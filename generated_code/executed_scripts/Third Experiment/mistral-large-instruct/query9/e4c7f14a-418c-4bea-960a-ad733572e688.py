import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the paths to the relevant JSON files
following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")

# Function to read JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to extract usernames from JSON data
def extract_usernames(data):
    usernames = set()
    for item in data:
        for string_data in item.get("string_list_data", []):
            usernames.add(string_data.get("value", ""))
    return usernames

# Read the following and followers JSON files
try:
    following_data = read_json_file(following_file)
    followers_data = read_json_file(followers_file)
except Exception as e:
    print(e)
    # Create an empty CSV file with the column header
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
    exit()

# Extract usernames from the following and followers data
following_usernames = extract_usernames(following_data.get("relationships_following", []))
followers_usernames = extract_usernames(followers_data)

# Find profiles that the user follows but do not follow him back
non_reciprocal_follows = following_usernames - followers_usernames

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    for profile in non_reciprocal_follows:
        writer.writerow([profile])