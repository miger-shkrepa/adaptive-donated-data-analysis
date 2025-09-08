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

# Function to extract authors from posts_viewed.json
def extract_viewed_authors(root_dir):
    viewed_authors = set()
    file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    if os.path.exists(file_path):
        data = read_json_file(file_path)
        for entry in data.get("impressions_history_posts_seen", []):
            string_map_data = entry.get("string_map_data", {})
            author = string_map_data.get("Author", {}).get("value")
            if author:
                viewed_authors.add(author)
    return viewed_authors

# Function to extract authors from liked_posts.json
def extract_liked_authors(root_dir):
    liked_authors = set()
    file_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    if os.path.exists(file_path):
        data = read_json_file(file_path)
        for entry in data.get("likes_media_likes", []):
            for item in entry.get("string_list_data", []):
                href = item.get("href")
                if href:
                    liked_authors.add(href.split('/')[-1])
    return liked_authors

# Main function to find accounts viewed but not liked
def find_viewed_but_not_liked_accounts(root_dir):
    try:
        viewed_authors = extract_viewed_authors(root_dir)
        liked_authors = extract_liked_authors(root_dir)
        result_authors = viewed_authors - liked_authors
        return result_authors
    except Exception as e:
        print(f"Error: {e}")
        return set()

# Write the result to a CSV file
def write_to_csv(result_authors):
    try:
        os.makedirs('query_responses', exist_ok=True)
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for author in result_authors:
                writer.writerow([author])
    except Exception as e:
        print(f"Error: {e}")

# Execute the main function and write the result to CSV
result_authors = find_viewed_but_not_liked_accounts(root_dir)
write_to_csv(result_authors)