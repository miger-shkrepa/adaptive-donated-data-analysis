import os
import csv
import json

# Variable referring to the file input
root_dir = "root_dir"

# Function to read JSON file and return its content
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to extract profiles from the JSON content
def extract_profiles(json_content, key):
    profiles = set()
    if key in json_content:
        for item in json_content[key]:
            for data in item.get('string_list_data', []):
                profiles.add(data.get('value', ''))
    return profiles

# Main function to find profiles that the user follows but do not follow back
def find_unfollowed_profiles(root_dir):
    following_file_path = os.path.join(root_dir, 'connections', 'followers_and_following', 'following.json')
    followers_file_path = os.path.join(root_dir, 'connections', 'followers_and_following', 'followers_1.json')
    
    try:
        following_content = read_json_file(following_file_path)
        followers_content = read_json_file(followers_file_path)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        return []

    following_profiles = extract_profiles(following_content, 'relationships_following')
    followers_profiles = extract_profiles(followers_content, 'relationships_followers')

    unfollowed_profiles = following_profiles - followers_profiles
    return unfollowed_profiles

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
    unfollowed_profiles = find_unfollowed_profiles(root_dir)
    generate_csv(unfollowed_profiles)
except Exception as e:
    print(e)
    generate_csv([])  # Generate an empty CSV file with only the column headers