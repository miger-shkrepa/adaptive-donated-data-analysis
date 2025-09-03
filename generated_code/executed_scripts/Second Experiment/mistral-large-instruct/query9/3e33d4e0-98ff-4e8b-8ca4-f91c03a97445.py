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
        following_profiles = [entry['string_list_data'][0]['value'] for entry in following_data['relationships_following']]
        return following_profiles
    except FileNotFoundError:
        return []

# Function to get the list of profiles that follow the user
def get_followers_profiles(root_dir):
    followers_file = os.path.join(root_dir, 'personal_information', 'follow_requests_you\'ve_received.json')
    try:
        followers_data = read_json_file(followers_file)
        followers_profiles = [entry['string_list_data'][0]['value'] for entry in followers_data['relationships_follow_requests_received']]
        return followers_profiles
    except FileNotFoundError:
        return []

# Function to find profiles that the user follows but do not follow back
def find_non_reciprocal_follows(root_dir):
    following_profiles = get_following_profiles(root_dir)
    followers_profiles = get_followers_profiles(root_dir)

    non_reciprocal_follows = [profile for profile in following_profiles if profile not in followers_profiles]
    return non_reciprocal_follows

# Function to write the results to a CSV file
def write_to_csv(data, output_csv):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Profile'])
            for profile in data:
                writer.writerow([profile])
    except Exception as e:
        raise ValueError(f"ValueError: Failed to write to CSV file. {str(e)}")

# Main function to execute the query
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    non_reciprocal_follows = find_non_reciprocal_follows(root_dir)
    write_to_csv(non_reciprocal_follows, output_csv)

if __name__ == "__main__":
    main()