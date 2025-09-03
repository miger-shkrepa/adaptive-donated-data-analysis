import os
import csv

# Define the root directory
root_dir = "root_dir"

# Function to read JSON files and extract authors
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = eval(file.read())
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: Error reading the file {file_path}: {str(e)}")

# Function to extract authors from posts_viewed.json
def extract_viewed_authors(data):
    authors = set()
    if 'impressions_history_posts_seen' in data:
        for entry in data['impressions_history_posts_seen']:
            if 'string_map_data' in entry and 'Author' in entry['string_map_data']:
                authors.add(entry['string_map_data']['Author']['value'])
    return authors

# Function to extract authors from liked_posts.json
def extract_liked_authors(data):
    authors = set()
    if 'likes_media_likes' in data:
        for entry in data['likes_media_likes']:
            if 'string_list_data' in entry:
                for item in entry['string_list_data']:
                    if 'value' in item:
                        authors.add(item['value'])
    return authors

# Main function to find accounts viewed but not liked
def find_viewed_but_not_liked_accounts(root_dir):
    try:
        # Define file paths
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

        # Read JSON files
        posts_viewed_data = read_json_file(posts_viewed_path) if os.path.exists(posts_viewed_path) else {}
        liked_posts_data = read_json_file(liked_posts_path) if os.path.exists(liked_posts_path) else {}

        # Extract authors
        viewed_authors = extract_viewed_authors(posts_viewed_data)
        liked_authors = extract_liked_authors(liked_posts_data)

        # Find the difference
        viewed_but_not_liked_authors = viewed_authors - liked_authors

        # Write to CSV
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for author in viewed_but_not_liked_authors:
                writer.writerow([author])

    except Exception as e:
        # If any error occurs, write only the column headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])

# Ensure the output directory exists
os.makedirs('query_responses', exist_ok=True)

# Execute the main function
find_viewed_but_not_liked_accounts(root_dir)