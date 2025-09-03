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

# Function to extract the list of usernames from the JSON data
def extract_usernames(data, key):
    usernames = set()
    if key in data:
        for item in data[key]:
            for entry in item['string_list_data']:
                if 'value' in entry:
                    usernames.add(entry['value'])
    return usernames

# Main function to find profiles that the user follows but do not follow back
def find_non_mutual_follows(root_dir):
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
    
    following_usernames = extract_usernames(following_data, "relationships_following")
    followers_usernames = extract_usernames(followers_data, "relationships_followers")
    
    non_mutual_follows = following_usernames - followers_usernames
    
    return non_mutual_follows

# Generate the result and save it to a CSV file
def save_to_csv(data, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
        for profile in data:
            writer.writerow([profile])

# Main execution
try:
    non_mutual_follows = find_non_mutual_follows(root_dir)
    save_to_csv(non_mutual_follows, 'query_responses/results.csv')
except Exception as e:
    save_to_csv([], 'query_responses/results.csv')
    print(f"Error: {e}")