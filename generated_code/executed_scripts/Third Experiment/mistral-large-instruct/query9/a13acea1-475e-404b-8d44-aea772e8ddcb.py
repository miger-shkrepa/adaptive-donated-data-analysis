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

# Function to get the list of profiles the user follows
def get_followed_profiles(root_dir):
    followed_profiles = []
    relationships_dir = os.path.join(root_dir, 'relationships_permanent_follow_requests')
    if not os.path.exists(relationships_dir):
        return followed_profiles

    for item in os.listdir(relationships_dir):
        item_path = os.path.join(relationships_dir, item)
        if os.path.isfile(item_path) and item.endswith('.json'):
            data = read_json_file(item_path)
            for entry in data.get('relationships_permanent_follow_requests', []):
                for string_data in entry.get('string_list_data', []):
                    followed_profiles.append(string_data.get('value'))
    return followed_profiles

# Function to get the list of profiles that follow the user
def get_followers(root_dir):
    followers = []
    relationships_dir = os.path.join(root_dir, 'relationships_permanent_follow_requests')
    if not os.path.exists(relationships_dir):
        return followers

    for item in os.listdir(relationships_dir):
        item_path = os.path.join(relationships_dir, item)
        if os.path.isfile(item_path) and item.endswith('.json'):
            data = read_json_file(item_path)
            for entry in data.get('relationships_permanent_follow_requests', []):
                for string_data in entry.get('string_list_data', []):
                    followers.append(string_data.get('value'))
    return followers

# Main function to find profiles that the user follows but do not follow back
def find_non_reciprocal_follows(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: FileNotFoundError: The root directory does not exist.")

    followed_profiles = get_followed_profiles(root_dir)
    followers = get_followers(root_dir)

    non_reciprocal_follows = [profile for profile in followed_profiles if profile not in followers]

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
        raise ValueError(f"Error: ValueError: Failed to write to CSV file. {str(e)}")

# Main execution
if __name__ == "__main__":
    try:
        non_reciprocal_follows = find_non_reciprocal_follows(root_dir)
        write_to_csv(non_reciprocal_follows, output_csv)
    except Exception as e:
        print(e)