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

# Function to get viewed posts
def get_viewed_posts(root_dir):
    viewed_posts_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    try:
        viewed_posts_data = read_json_file(viewed_posts_file)
        viewed_authors = {entry['string_map_data']['Author']['value'] for entry in viewed_posts_data['impressions_history_posts_seen']}
        return viewed_authors
    except FileNotFoundError:
        return set()

# Function to get liked posts
def get_liked_posts(root_dir):
    liked_posts_file = os.path.join(root_dir, 'likes', 'liked_posts.json')
    try:
        liked_posts_data = read_json_file(liked_posts_file)
        liked_authors = {entry['title'] for entry in liked_posts_data['likes_media_likes']}
        return liked_authors
    except FileNotFoundError:
        return set()

# Main function to find accounts viewed but not liked
def find_viewed_but_not_liked_accounts(root_dir):
    viewed_authors = get_viewed_posts(root_dir)
    liked_authors = get_liked_posts(root_dir)

    viewed_but_not_liked = viewed_authors - liked_authors

    return viewed_but_not_liked

# Function to save results to CSV
def save_to_csv(results, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in results:
                writer.writerow([account])
    except Exception as e:
        raise ValueError(f"Error: Unable to write to CSV file. {str(e)}")

# Main execution
if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    viewed_but_not_liked_accounts = find_viewed_but_not_liked_accounts(root_dir)

    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    save_to_csv(viewed_but_not_liked_accounts, output_path)