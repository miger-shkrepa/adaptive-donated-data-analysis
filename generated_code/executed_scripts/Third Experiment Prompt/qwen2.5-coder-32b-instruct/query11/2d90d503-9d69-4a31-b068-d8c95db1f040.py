import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file and return its content
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to extract authors from posts viewed
def extract_authors_from_viewed_posts(viewed_posts_file):
    try:
        data = read_json_file(viewed_posts_file)
        authors = set()
        for entry in data.get('impressions_history_posts_seen', []):
            author = entry.get('string_map_data', {}).get('Author', {}).get('value')
            if author:
                authors.add(author)
        return authors
    except Exception as e:
        print(f"Error extracting authors from viewed posts: {e}")
        return set()

# Function to extract authors from liked posts
def extract_authors_from_liked_posts(liked_posts_file):
    try:
        data = read_json_file(liked_posts_file)
        authors = set()
        for entry in data.get('likes_media_likes', []):
            for item in entry.get('string_list_data', []):
                author = item.get('value')
                if author:
                    authors.add(author)
        return authors
    except Exception as e:
        print(f"Error extracting authors from liked posts: {e}")
        return set()

# Main function to find accounts viewed but not liked
def find_accounts_viewed_but_not_liked(root_dir):
    viewed_posts_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    liked_posts_file = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')

    viewed_authors = extract_authors_from_viewed_posts(viewed_posts_file)
    liked_authors = extract_authors_from_liked_posts(liked_posts_file)

    accounts_viewed_but_not_liked = viewed_authors - liked_authors

    # Write the result to a CSV file
    output_file = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Account'])
        for account in accounts_viewed_but_not_liked:
            writer.writerow([account])

# Execute the main function
try:
    find_accounts_viewed_but_not_liked(root_dir)
except Exception as e:
    print(f"Error: {e}")
    # Create an empty CSV file with only the column headers if there's an error
    output_file = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Account'])