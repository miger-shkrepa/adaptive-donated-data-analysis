import os
import csv

# Define the root directory
root_dir = "root_dir"

# Function to read JSON files and extract authors
def read_json_file(file_path):
    authors = set()
    try:
        with open(file_path, 'r') as file:
            data = eval(file.read())
            if 'impressions_history_posts_seen' in data:
                for entry in data['impressions_history_posts_seen']:
                    if 'string_map_data' in entry and 'Author' in entry['string_map_data']:
                        authors.add(entry['string_map_data']['Author']['value'])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: Error reading the file {file_path}: {str(e)}")
    return authors

# Function to read liked posts and extract authors
def read_liked_posts(file_path):
    liked_authors = set()
    try:
        with open(file_path, 'r') as file:
            data = eval(file.read())
            if 'likes_media_likes' in data:
                for entry in data['likes_media_likes']:
                    if 'string_list_data' in entry:
                        for item in entry['string_list_data']:
                            if 'href' in item:
                                liked_authors.add(item['href'].split('/')[-1])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: Error reading the file {file_path}: {str(e)}")
    return liked_authors

# Define the paths to the JSON files
posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

# Initialize sets to store authors
viewed_authors = set()
liked_authors = set()

# Read the viewed posts file
if os.path.exists(posts_viewed_path):
    viewed_authors = read_json_file(posts_viewed_path)
else:
    print(f"Warning: {posts_viewed_path} does not exist. Continuing with empty data.")

# Read the liked posts file
if os.path.exists(liked_posts_path):
    liked_authors = read_liked_posts(liked_posts_path)
else:
    print(f"Warning: {liked_posts_path} does not exist. Continuing with empty data.")

# Find the difference to get accounts viewed but not liked
result_authors = viewed_authors - liked_authors

# Write the result to a CSV file
output_path = 'query_responses/results.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Account'])
    for author in result_authors:
        csvwriter.writerow([author])

print(f"Results saved to {output_path}")