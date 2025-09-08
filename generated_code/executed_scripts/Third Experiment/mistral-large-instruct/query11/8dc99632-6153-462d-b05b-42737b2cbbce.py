import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the paths to the relevant JSON files
posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
story_likes_path = os.path.join(root_dir, "connections", "followers_and_following", "recently_unfollowed_accounts.json")

# Function to read JSON file
def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON.")

# Function to extract account names from JSON data
def extract_accounts(data, key):
    accounts = set()
    for item in data.get(key, []):
        for string_data in item.get("string_list_data", []):
            accounts.add(string_data.get("value"))
    return accounts

# Read the JSON files
try:
    posts_viewed_data = read_json(posts_viewed_path)
    story_likes_data = read_json(story_likes_path)
except Exception as e:
    print(e)
    # Create an empty CSV file with only the column headers
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
    exit()

# Extract account names
viewed_accounts = extract_accounts(posts_viewed_data, "impressions_history_posts_seen")
liked_accounts = extract_accounts(story_likes_data, "story_activities_story_likes")

# Find accounts viewed but not liked
accounts_viewed_not_liked = viewed_accounts - liked_accounts

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])
    for account in accounts_viewed_not_liked:
        writer.writerow([account])