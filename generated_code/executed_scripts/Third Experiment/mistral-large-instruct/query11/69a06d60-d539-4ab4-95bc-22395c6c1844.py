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
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Function to get viewed posts
def get_viewed_posts(root_dir):
    viewed_posts_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    if not os.path.exists(viewed_posts_file):
        return []
    data = read_json_file(viewed_posts_file)
    viewed_posts = [entry['string_map_data']['Author']['value'] for entry in data['impressions_history_posts_seen']]
    return viewed_posts

# Function to get liked posts
def get_liked_posts(root_dir):
    # Assuming there is a file for liked posts, but it's not provided in the context
    liked_posts_file = os.path.join(root_dir, 'liked_posts.json')
    if not os.path.exists(liked_posts_file):
        return []
    data = read_json_file(liked_posts_file)
    liked_posts = [entry['string_map_data']['Author']['value'] for entry in data['liked_posts']]
    return liked_posts

# Main function to get accounts viewed but not liked
def get_viewed_but_not_liked_accounts(root_dir):
    viewed_posts = get_viewed_posts(root_dir)
    liked_posts = get_liked_posts(root_dir)

    viewed_but_not_liked = set(viewed_posts) - set(liked_posts)
    return list(viewed_but_not_liked)

# Function to write results to CSV
def write_to_csv(data, output_csv):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in data:
                writer.writerow([account])
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

# Main execution
if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    viewed_but_not_liked_accounts = get_viewed_but_not_liked_accounts(root_dir)
    write_to_csv(viewed_but_not_liked_accounts, output_csv)