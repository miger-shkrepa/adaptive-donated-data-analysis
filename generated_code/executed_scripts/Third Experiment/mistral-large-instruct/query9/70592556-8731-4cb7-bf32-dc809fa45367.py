import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to read JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Function to get the list of profiles the user follows
def get_following_profiles(root_dir):
    following_file = os.path.join(root_dir, "following", "following.json")
    if not os.path.exists(following_file):
        return []
    following_data = read_json_file(following_file)
    return [entry['string_map_data']['Profile Name']['value'] for entry in following_data['relationships_following']]

# Function to get the list of profiles that follow the user
def get_followers_profiles(root_dir):
    followers_file = os.path.join(root_dir, "followers", "followers.json")
    if not os.path.exists(followers_file):
        return []
    followers_data = read_json_file(followers_file)
    return [entry['string_map_data']['Profile Name']['value'] for entry in followers_data['relationships_followers']]

# Main function to find profiles that the user follows but do not follow back
def find_non_reciprocal_follows(root_dir):
    following_profiles = get_following_profiles(root_dir)
    followers_profiles = get_followers_profiles(root_dir)

    non_reciprocal_follows = [profile for profile in following_profiles if profile not in followers_profiles]

    return non_reciprocal_follows

# Function to write the results to a CSV file
def write_to_csv(results, output_file):
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Profile"])
            for profile in results:
                writer.writerow([profile])
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

# Main execution
if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    non_reciprocal_follows = find_non_reciprocal_follows(root_dir)
    output_file = 'query_responses/results.csv'

    if not non_reciprocal_follows:
        write_to_csv([], output_file)
    else:
        write_to_csv(non_reciprocal_follows, output_file)