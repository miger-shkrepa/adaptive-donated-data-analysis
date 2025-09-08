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

# Function to get viewed posts
def get_viewed_posts(root_dir):
    viewed_posts_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    if not os.path.exists(viewed_posts_file):
        return []
    viewed_posts_data = read_json_file(viewed_posts_file)
    viewed_posts = [entry['string_map_data']['Author']['value'] for entry in viewed_posts_data['impressions_history_posts_seen']]
    return viewed_posts

# Function to get liked posts
def get_liked_posts(root_dir):
    liked_posts_file = os.path.join(root_dir, 'connections', 'followers_and_following', 'following.json')
    if not os.path.exists(liked_posts_file):
        return []
    liked_posts_data = read_json_file(liked_posts_file)
    liked_posts = [entry['string_list_data'][0]['value'] for entry in liked_posts_data['relationships_following']]
    return liked_posts

# Main function to get accounts viewed but not liked
def get_viewed_but_not_liked_accounts(root_dir):
    viewed_posts = get_viewed_posts(root_dir)
    liked_posts = get_liked_posts(root_dir)

    viewed_but_not_liked = [account for account in viewed_posts if account not in liked_posts]

    return viewed_but_not_liked

# Function to write results to CSV
def write_to_csv(data, output_csv):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in data:
                writer.writerow([account])
    except Exception as e:
        raise ValueError(f"Error: ValueError: Failed to write to CSV file. {str(e)}")

# Main execution
if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: FileNotFoundError: The root directory does not exist.")

    viewed_but_not_liked_accounts = get_viewed_but_not_liked_accounts(root_dir)

    if not os.path.exists('query_responses'):
        os.makedirs('query_responses')

    write_to_csv(viewed_but_not_liked_accounts, output_csv)