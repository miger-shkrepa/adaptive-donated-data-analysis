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
                if 'value' in entry:
                    usernames.add(entry['value'])
    return usernames

# Main function to find profiles the user follows that do not follow back
def find_unfollowed_profiles(root_dir):
    following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")

    try:
        following_data = read_json_file(following_file)
    except (FileNotFoundError, ValueError):
        following_data = {}

    try:
        followers_data = read_json_file(followers_file)
    except (FileNotFoundError, ValueError):
        followers_data = {}

    following_usernames = extract_usernames(following_data, 'relationships_following')
    followers_usernames = extract_usernames(followers_data, 'relationships_followers')

    unfollowed_profiles = following_usernames - followers_usernames

    return unfollowed_profiles

# Generate the CSV file
def generate_csv(unfollowed_profiles):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in unfollowed_profiles:
            writer.writerow([profile])

# Main execution
try:
    unfollowed_profiles = find_unfollowed_profiles(root_dir)
    generate_csv(unfollowed_profiles)
except Exception as e:
    generate_csv(set())  # Create an empty CSV file with only the column headers if an error occurs