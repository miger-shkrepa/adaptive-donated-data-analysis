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

# Function to extract usernames from the JSON data
def extract_usernames(data, key):
    usernames = set()
    if key in data:
        for item in data[key]:
            for entry in item['string_list_data']:
                usernames.add(entry['value'])
    return usernames

# Main function to find profiles the user follows that do not follow back
def find_non_mutual_follows(root_dir):
    following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")

    following_usernames = set()
    followers_usernames = set()

    try:
        following_data = read_json_file(following_file)
        following_usernames = extract_usernames(following_data, "relationships_following")
    except (FileNotFoundError, ValueError) as e:
        print(e)

    try:
        followers_data = read_json_file(followers_file)
        followers_usernames = extract_usernames(followers_data, "relationships_followers")
    except (FileNotFoundError, ValueError) as e:
        print(e)

    non_mutual_follows = following_usernames - followers_usernames

    return non_mutual_follows

# Generate the result
non_mutual_follows = find_non_mutual_follows(root_dir)

# Write the result to a CSV file
output_file = 'query_responses/results.csv'
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Profile'])
    for profile in non_mutual_follows:
        writer.writerow([profile])