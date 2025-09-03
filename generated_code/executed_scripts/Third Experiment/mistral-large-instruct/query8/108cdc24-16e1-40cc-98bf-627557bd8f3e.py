import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Initialize dictionaries to store interaction counts
post_likes = {}
story_likes = {}
comments = {}

# Helper function to process JSON files
def process_json_file(file_path, interaction_type):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data.get(interaction_type, []):
                user = item.get('string_map_data', {}).get('value', '')
                if user:
                    if interaction_type == 'post_likes':
                        post_likes[user] = post_likes.get(user, 0) + 1
                    elif interaction_type == 'story_likes':
                        story_likes[user] = story_likes.get(user, 0) + 1
                    elif interaction_type == 'comments':
                        comments[user] = comments.get(user, 0) + 1
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Process the directory structure
try:
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                if 'post_likes' in file:
                    process_json_file(file_path, 'post_likes')
                elif 'story_likes' in file:
                    process_json_file(file_path, 'story_likes')
                elif 'comments' in file:
                    process_json_file(file_path, 'comments')
except FileNotFoundError:
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Aggregate interaction counts
interaction_counts = {}
for user in set(post_likes.keys()).union(story_likes.keys()).union(comments.keys()):
    interaction_counts[user] = {
        'Post Likes': post_likes.get(user, 0),
        'Story Likes': story_likes.get(user, 0),
        'Comments': comments.get(user, 0)
    }

# Sort users by total interactions
sorted_users = sorted(interaction_counts.items(), key=lambda x: sum(x[1].values()), reverse=True)

# Write the results to a CSV file
try:
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, counts in sorted_users[:20]:
            writer.writerow({
                'User': user,
                'Post Likes': counts['Post Likes'],
                'Story Likes': counts['Story Likes'],
                'Comments': counts['Comments']
            })
except Exception as e:
    raise ValueError(f"ValueError: Failed to write to CSV file. {str(e)}")