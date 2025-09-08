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

# Function to get the list of followed users
def get_followed_users(root_dir):
    followed_users_path = os.path.join(root_dir, "relationships_follow_requests_received.json")
    if not os.path.exists(followed_users_path):
        return []
    followed_users_data = read_json_file(followed_users_path)
    followed_users = [entry['title'] for entry in followed_users_data['relationships_follow_requests_received']]
    return followed_users

# Function to get the list of users who follow the user
def get_followers(root_dir):
    followers_path = os.path.join(root_dir, "relationships_hide_stories_from.json")
    if not os.path.exists(followers_path):
        return []
    followers_data = read_json_file(followers_path)
    followers = [entry['title'] for entry in followers_data['relationships_hide_stories_from']]
    return followers

# Function to find profiles that the user follows but do not follow back
def find_non_reciprocal_follows(root_dir):
    followed_users = get_followed_users(root_dir)
    followers = get_followers(root_dir)

    non_reciprocal_follows = [user for user in followed_users if user not in followers]
    return non_reciprocal_follows

# Function to save the results to a CSV file
def save_to_csv(data, file_path):
    try:
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Profile"])
            for item in data:
                writer.writerow([item])
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

# Main function
def main():
    try:
        non_reciprocal_follows = find_non_reciprocal_follows(root_dir)
        save_to_csv(non_reciprocal_follows, 'query_responses/results.csv')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()