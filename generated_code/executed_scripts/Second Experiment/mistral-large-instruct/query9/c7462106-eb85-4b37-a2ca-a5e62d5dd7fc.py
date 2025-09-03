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
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to get the list of profiles the user follows
def get_following_profiles(root_dir):
    following_file = os.path.join(root_dir, 'personal_information', 'following.json')
    try:
        following_data = read_json_file(following_file)
        return [item['string_list_data'][0]['value'] for item in following_data['relationships_following']]
    except (FileNotFoundError, ValueError):
        return []

# Function to get the list of profiles that follow the user
def get_followers_profiles(root_dir):
    followers_file = os.path.join(root_dir, 'personal_information', 'follow_requests_you\'ve_received.json')
    try:
        followers_data = read_json_file(followers_file)
        return [item['string_list_data'][0]['value'] for item in followers_data['relationships_follow_requests_received']]
    except (FileNotFoundError, ValueError):
        return []

# Function to get the list of profiles that do not follow the user back
def get_non_followers(following_profiles, followers_profiles):
    return [profile for profile in following_profiles if profile not in followers_profiles]

# Main function to generate the CSV file
def generate_csv(root_dir, output_csv):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    following_profiles = get_following_profiles(root_dir)
    followers_profiles = get_followers_profiles(root_dir)

    non_followers = get_non_followers(following_profiles, followers_profiles)

    # Write the results to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in non_followers:
            writer.writerow([profile])

# Execute the main function
generate_csv(root_dir, output_csv)