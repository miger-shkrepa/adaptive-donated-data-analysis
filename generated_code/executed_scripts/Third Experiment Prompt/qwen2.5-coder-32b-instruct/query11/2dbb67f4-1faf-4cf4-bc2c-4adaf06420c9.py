import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file and return its content
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to extract accounts from liked_posts.json
def extract_liked_accounts(liked_posts_path):
    try:
        liked_data = read_json_file(liked_posts_path)
        liked_accounts = set()
        for like in liked_data.get('likes_media_likes', []):
            for item in like.get('string_list_data', []):
                liked_accounts.add(item.get('value', ''))
        return liked_accounts
    except Exception as e:
        print(f"Error extracting liked accounts: {e}")
        return set()

# Function to extract accounts from saved_posts.json
def extract_saved_accounts(saved_posts_path):
    try:
        saved_data = read_json_file(saved_posts_path)
        saved_accounts = set()
        for saved in saved_data.get('saved_saved_media', []):
            for key, value in saved.get('string_map_data', {}).items():
                if key == "Saved on":
                    saved_accounts.add(value.get('value', ''))
        return saved_accounts
    except Exception as e:
        print(f"Error extracting saved accounts: {e}")
        return set()

# Main function to find accounts viewed but not liked
def find_viewed_but_not_liked_accounts(root_dir):
    liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

    liked_accounts = extract_liked_accounts(liked_posts_path)
    saved_accounts = extract_saved_accounts(saved_posts_path)

    # Find accounts that are in saved but not in liked
    viewed_but_not_liked_accounts = saved_accounts - liked_accounts

    # Write the result to a CSV file
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Account'])
        for account in viewed_but_not_liked_accounts:
            writer.writerow([account])

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Execute the main function
find_viewed_but_not_liked_accounts(root_dir)