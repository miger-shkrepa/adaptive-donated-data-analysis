import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to load JSON data from a file
def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON file.")

# Function to get the list of profiles the user follows
def get_following(following_file):
    following_data = load_json(following_file)
    following_list = []
    for item in following_data.get("relationships_following", []):
        for string_data in item.get("string_list_data", []):
            following_list.append(string_data.get("value"))
    return following_list

# Function to get the list of profiles that follow the user
def get_followers(followers_file):
    followers_data = load_json(followers_file)
    followers_list = []
    for item in followers_data:
        for string_data in item.get("string_list_data", []):
            followers_list.append(string_data.get("value"))
    return followers_list

# Main function to find profiles that the user follows but do not follow back
def find_non_mutual_follows(root_dir):
    following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")

    try:
        following_list = get_following(following_file)
        followers_list = get_followers(followers_file)
    except Exception as e:
        # If any error occurs, write an empty CSV with the column header
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Profile"])
        raise e

    non_mutual_follows = [profile for profile in following_list if profile not in followers_list]

    # Write the results to the CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
        for profile in non_mutual_follows:
            writer.writerow([profile])

# Run the main function
find_non_mutual_follows(root_dir)