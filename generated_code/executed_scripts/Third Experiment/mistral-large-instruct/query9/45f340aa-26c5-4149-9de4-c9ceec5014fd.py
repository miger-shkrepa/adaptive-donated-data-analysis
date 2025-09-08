import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to read JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON file.")

# Function to get usernames from JSON files
def get_usernames(json_data):
    usernames = set()
    for item in json_data:
        for string_data in item.get('string_list_data', []):
            usernames.add(string_data.get('value', ''))
    return usernames

# Main function to find profiles that the user follows but do not follow back
def find_non_reciprocal_follows(root_dir):
    following_file = os.path.join(root_dir, 'connections', 'followers_and_following', 'following.json')
    followers_file = os.path.join(root_dir, 'connections', 'followers_and_following', 'followers_1.json')

    try:
        following_data = read_json_file(following_file)
        followers_data = read_json_file(followers_file)
    except Exception as e:
        # If any file is missing, return a CSV with only the column headers
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Profile'])
        return

    following_usernames = get_usernames(following_data.get('relationships_following', []))
    followers_usernames = get_usernames(followers_data)

    non_reciprocal_follows = following_usernames - followers_usernames

    # Write the results to the CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in non_reciprocal_follows:
            writer.writerow([profile])

# Execute the main function
find_non_reciprocal_follows(root_dir)