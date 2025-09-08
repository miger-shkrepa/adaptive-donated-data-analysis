import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

# Function to read JSON files and extract the required data
def read_json_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        import json
        data = json.load(file)
        return data

# Function to extract the list of profiles from the JSON data
def extract_profiles(data, key):
    profiles = set()
    if key in data:
        for item in data[key]:
            for entry in item['string_list_data']:
                if 'value' in entry:
                    profiles.add(entry['value'])
    return profiles

# Main function to find profiles that the user follows but do not follow back
def find_unfollowed_profiles(root_dir):
    following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
    
    try:
        following_data = read_json_file(following_file)
    except FileNotFoundError:
        following_data = {}
    
    try:
        followers_data = read_json_file(followers_file)
    except FileNotFoundError:
        followers_data = {}
    
    following_profiles = extract_profiles(following_data, "relationships_following")
    followers_profiles = extract_profiles(followers_data, "relationships_followers")
    
    unfollowed_profiles = following_profiles - followers_profiles
    
    return unfollowed_profiles

# Main execution
try:
    unfollowed_profiles = find_unfollowed_profiles(root_dir)
    
    # Write the results to a CSV file
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in unfollowed_profiles:
            writer.writerow([profile])
except Exception as e:
    # Write only the column headers if there is an error
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
    print(f"Error: {e}")