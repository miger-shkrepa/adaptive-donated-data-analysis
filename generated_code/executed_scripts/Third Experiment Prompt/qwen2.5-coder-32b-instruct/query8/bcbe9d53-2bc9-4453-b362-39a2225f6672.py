import os
import csv
import json
from collections import defaultdict

# Variable referring to the file input
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

# Function to aggregate interactions from a JSON structure
def aggregate_interactions(data, interactions_dict, interaction_type):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "string_list_data":
                for item in value:
                    if "value" in item:
                        interactions_dict[item["value"]][interaction_type] += 1
            elif key == "string_map_data":
                for item in value.values():
                    if "value" in item:
                        interactions_dict[item["value"]][interaction_type] += 1
            else:
                aggregate_interactions(value, interactions_dict, interaction_type)
    elif isinstance(data, list):
        for item in data:
            aggregate_interactions(item, interactions_dict, interaction_type)

# Initialize a dictionary to store interactions
interactions = defaultdict(lambda: {"Post Likes": 0, "Story Likes": 0, "Comments": 0})

# Path to the liked posts JSON file
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
# Path to the liked comments JSON file
liked_comments_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_comments.json")
# Path to the post comments JSON file
post_comments_path = os.path.join(root_dir, "your_instagram_activity", "comments", "post_comments_1.json")

# Aggregate interactions from liked posts
if os.path.exists(liked_posts_path):
    liked_posts_data = read_json_file(liked_posts_path)
    aggregate_interactions(liked_posts_data, interactions, "Post Likes")

# Aggregate interactions from liked comments
if os.path.exists(liked_comments_path):
    liked_comments_data = read_json_file(liked_comments_path)
    aggregate_interactions(liked_comments_data, interactions, "Story Likes")

# Aggregate interactions from post comments
if os.path.exists(post_comments_path):
    post_comments_data = read_json_file(post_comments_path)
    aggregate_interactions(post_comments_data, interactions, "Comments")

# Sort interactions by total count in descending order and get the top 20
top_interactions = sorted(interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)[:20]

# Prepare the CSV data
csv_data = [["User", "Post Likes", "Story Likes", "Comments"]]
for user, counts in top_interactions:
    csv_data.append([user, counts["Post Likes"], counts["Story Likes"], counts["Comments"]])

# Write the CSV file
output_path = "query_responses/results.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(csv_data)