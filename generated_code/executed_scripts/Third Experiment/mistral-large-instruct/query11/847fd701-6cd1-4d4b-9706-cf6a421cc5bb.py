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
        viewed_posts = {entry['string_map_data']['Author']['value'] for entry in viewed_posts_data['impressions_history_posts_seen']}
        return viewed_posts
    except FileNotFoundError:
        return set()

# Function to get liked posts
def get_liked_posts(root_dir):
    liked_posts_file = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')
    try:
        liked_posts_data = read_json_file(liked_posts_file)
        liked_posts = {entry['string_list_data'][0]['value'] for entry in liked_posts_data['likes_media_likes']}
        return liked_posts
    except FileNotFoundError:
        return set()

# Main function to get accounts viewed but not liked
def get_accounts_viewed_but_not_liked(root_dir):
    viewed_posts = get_viewed_posts(root_dir)
    liked_posts = get_liked_posts(root_dir)

    accounts_viewed_but_not_liked = viewed_posts - liked_posts

    return accounts_viewed_but_not_liked

# Function to save results to CSV
def save_to_csv(accounts, file_path):
    try:
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

# Main execution
if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    accounts_viewed_but_not_liked = get_accounts_viewed_but_not_liked(root_dir)

    output_file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    save_to_csv(accounts_viewed_but_not_liked, output_file_path)