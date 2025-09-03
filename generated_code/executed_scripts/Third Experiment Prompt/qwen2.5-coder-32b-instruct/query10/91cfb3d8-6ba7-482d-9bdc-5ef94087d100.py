import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Initialize dictionaries to store the counts
account_likes = {}
account_saves = {}

# Function to process JSON files and update the account counts
def process_json_file(file_path, account_dict):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'likes_media_likes' in data:
                for item in data['likes_media_likes']:
                    for entry in item['string_list_data']:
                        account = entry['value']
                        if account not in account_dict:
                            account_dict[account] = 0
                        account_dict[account] += 1
            elif 'saved_saved_media' in data:
                for item in data['saved_saved_media']:
                    account = item['title']
                    if account not in account_dict:
                        account_dict[account] = 0
                    account_dict[account] += 1
    except FileNotFoundError:
        print(f"FileNotFoundError: The file {file_path} does not exist. Skipping.")
    except json.JSONDecodeError:
        print(f"ValueError: The file {file_path} is not a valid JSON file. Skipping.")
    except Exception as e:
        print(f"Error: An unexpected error occurred while processing {file_path}: {e}")

# Process the liked_posts.json file
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
process_json_file(liked_posts_path, account_likes)

# Process the saved_posts.json file
saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
process_json_file(saved_posts_path, account_saves)

# Combine the likes and saves into a single dictionary
combined_counts = {}
for account, count in account_likes.items():
    combined_counts[account] = {'Post Views': count, 'Video Views': 0}

for account, count in account_saves.items():
    if account in combined_counts:
        combined_counts[account]['Post Views'] += count
    else:
        combined_counts[account] = {'Post Views': count, 'Video Views': 0}

# Ensure the output directory exists
output_dir = os.path.dirname('query_responses/results.csv')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Account', 'Post Views', 'Video Views']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for account, counts in combined_counts.items():
        writer.writerow({'Account': account, 'Post Views': counts['Post Views'], 'Video Views': counts['Video Views']})

print("CSV file has been generated at 'query_responses/results.csv'.")