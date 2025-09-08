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

# Function to extract usernames from the JSON data
def extract_usernames(data, key):
    usernames = set()
    if key in data:
        for item in data[key]:
            for entry in item['string_list_data']:
                if 'value' in entry:
                    usernames.add(entry['value'])
    return usernames

# Main function to find profiles that the user follows but do not follow back
def find_unfollowed_back_profiles(root_dir):
    following_file_path = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    followers_file_path = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
    
    try:
        following_data = read_json_file(following_file_path)
    except FileNotFoundError:
        following_data = {}
    
    try:
        followers_data = read_json_file(followers_file_path)
    except FileNotFoundError:
        followers_data = {}
    
    following_usernames = extract_usernames(following_data, "relationships_following")
    followers_usernames = extract_usernames(followers_data, "relationships_followers")
    
    unfollowed_back_profiles = following_usernames - followers_usernames
    
    return unfollowed_back_profiles

# Generate the CSV file with the results
def generate_csv(profiles):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in profiles:
            writer.writerow([profile])

# Main execution
try:
    unfollowed_back_profiles = find_unfollowed_back_profiles(root_dir)
    generate_csv(unfollowed_back_profiles)
except Exception as e:
    generate_csv([])  # Create an empty CSV file with only the column headers if an error occurs