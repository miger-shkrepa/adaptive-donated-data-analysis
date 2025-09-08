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
    liked_posts_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_liked.json')
    try:
        liked_posts_data = read_json_file(liked_posts_file)
        liked_authors = {entry['string_map_data']['Author']['value'] for entry in liked_posts_data['impressions_history_posts_liked']}
        return liked_authors
    except FileNotFoundError:
        return set()

# Main function to get accounts viewed but not liked
def get_accounts_viewed_but_not_liked(root_dir):
    viewed_authors = get_viewed_posts(root_dir)
    liked_authors = get_liked_posts(root_dir)
    accounts_viewed_but_not_liked = viewed_authors - liked_authors
    return accounts_viewed_but_not_liked

# Function to write results to CSV
def write_results_to_csv(results, output_file):
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in results:
                writer.writerow([account])
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

# Main execution
if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    accounts_viewed_but_not_liked = get_accounts_viewed_but_not_liked(root_dir)
    output_file = 'query_responses/results.csv'
    write_results_to_csv(accounts_viewed_but_not_liked, output_file)