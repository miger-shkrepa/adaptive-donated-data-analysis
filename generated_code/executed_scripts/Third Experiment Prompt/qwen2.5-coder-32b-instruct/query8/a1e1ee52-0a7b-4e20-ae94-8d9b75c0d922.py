import os
import csv
import json
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Initialize a dictionary to store the count of interactions per account
account_interactions = defaultdict(int)

# Function to load and parse JSON files
def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to process liked posts
def process_liked_posts(file_path):
    try:
        data = load_json_file(file_path)
        if 'likes_media_likes' in data:
            for item in data['likes_media_likes']:
                for entry in item['string_list_data']:
                    account_interactions[entry['value']] += 1
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Define the path to the liked posts JSON file
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

# Process the liked posts file if it exists
if os.path.exists(liked_posts_path):
    process_liked_posts(liked_posts_path)

# Sort the accounts by the number of interactions in descending order
sorted_accounts = sorted(account_interactions.items(), key=lambda x: x[1], reverse=True)

# Prepare the top 20 accounts
top_20_accounts = sorted_accounts[:20]

# Define the output CSV file path
output_csv_path = 'query_responses/results.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Write the results to the CSV file
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['User', 'Post Likes', 'Story Likes and Comments'])
    for account, likes in top_20_accounts:
        csvwriter.writerow([account, likes, 0])

print(f"Results have been saved to {output_csv_path}")