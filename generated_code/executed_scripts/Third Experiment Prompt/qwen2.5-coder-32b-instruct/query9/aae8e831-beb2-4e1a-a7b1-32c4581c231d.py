import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Function to read JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to extract following and followers from JSON data
def extract_following_and_followers(root_dir):
    following_file_path = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    followers_file_path = os.path.join(root_dir, "connections", "followers_and_following", "close_friends.json")

    following = set()
    followers = set()

    # Extract following
    if os.path.exists(following_file_path):
        following_data = read_json_file(following_file_path)
        for item in following_data.get("relationships_following", []):
            for data in item.get("string_list_data", []):
                following.add(data.get("value", ""))
    else:
        print(f"Warning: The file {following_file_path} does not exist. Treating following as empty.")

    # Extract followers
    if os.path.exists(followers_file_path):
        followers_data = read_json_file(followers_file_path)
        for item in followers_data.get("relationships_close_friends", []):
            for data in item.get("string_list_data", []):
                followers.add(data.get("value", ""))
    else:
        print(f"Warning: The file {followers_file_path} does not exist. Treating followers as empty.")

    return following, followers

# Main function to find profiles that the user follows but do not follow back
def find_non_mutual_follows(root_dir):
    following, followers = extract_following_and_followers(root_dir)
    non_mutual_follows = following - followers
    return non_mutual_follows

# Main execution
try:
    non_mutual_follows = find_non_mutual_follows(root_dir)

    # Write the result to a CSV file
    output_file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in non_mutual_follows:
            writer.writerow([profile])

except Exception as e:
    print(f"Error: {e}")
    # Create an empty CSV file with only the column headers if there's an error
    output_file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])