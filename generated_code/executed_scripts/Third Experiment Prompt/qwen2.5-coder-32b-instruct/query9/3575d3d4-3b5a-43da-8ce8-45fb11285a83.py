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
def extract_usernames(data):
    usernames = set()
    if isinstance(data, dict):
        if 'relationships_following' in data:
            for entry in data['relationships_following']:
                for item in entry['string_list_data']:
                    if 'value' in item:
                        usernames.add(item['value'])
    return usernames

# Function to find profiles that the user follows but do not follow back
def find_non_mutual_follows(following, followers):
    return following - followers

# Main function to execute the query
def main():
    following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
    
    try:
        following_data = read_json_file(following_file)
        followers_data = read_json_file(followers_file)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        # If there's an error, write only the column headers to the CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Profile'])
        return
    
    following_usernames = extract_usernames(following_data)
    followers_usernames = extract_usernames(followers_data)
    
    non_mutual_follows = find_non_mutual_follows(following_usernames, followers_usernames)
    
    # Write the results to a CSV file
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in non_mutual_follows:
            writer.writerow([profile])

# Execute the main function
if __name__ == "__main__":
    main()