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

# Helper function to update interaction counts
def update_interaction_counts(interaction_dict, user):
    if user in interaction_dict:
        interaction_dict[user] += 1
    else:
        interaction_dict[user] = 1

# Process the directory structure
try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Process liked_posts.json
    liked_posts_path = os.path.join(root_dir, 'likes', 'liked_posts.json')
    if os.path.exists(liked_posts_path):
        with open(liked_posts_path, 'r') as file:
            data = json.load(file)
            for item in data.get('likes_media_likes', []):
                for entry in item.get('string_list_data', []):
                    update_interaction_counts(post_likes, entry.get('value', ''))

    # Process story_likes.json (assuming a similar structure as liked_posts.json)
    story_likes_path = os.path.join(root_dir, 'likes', 'story_likes.json')
    if os.path.exists(story_likes_path):
        with open(story_likes_path, 'r') as file:
            data = json.load(file)
            for item in data.get('likes_media_likes', []):
                for entry in item.get('string_list_data', []):
                    update_interaction_counts(story_likes, entry.get('value', ''))

    # Process comments.json (assuming a similar structure as liked_posts.json)
    comments_path = os.path.join(root_dir, 'comments', 'comments.json')
    if os.path.exists(comments_path):
        with open(comments_path, 'r') as file:
            data = json.load(file)
            for item in data.get('comments_media_comments', []):
                for entry in item.get('string_list_data', []):
                    update_interaction_counts(comments, entry.get('value', ''))

    # Aggregate interaction counts
    total_interactions = {}
    for user in set(post_likes.keys()).union(story_likes.keys()).union(comments.keys()):
        total_interactions[user] = (
            post_likes.get(user, 0) +
            story_likes.get(user, 0) +
            comments.get(user, 0)
        )

    # Sort users by total interactions
    sorted_users = sorted(total_interactions.items(), key=lambda x: x[1], reverse=True)[:20]

    # Write the results to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, _ in sorted_users:
            writer.writerow({
                'User': user,
                'Post Likes': post_likes.get(user, 0),
                'Story Likes': story_likes.get(user, 0),
                'Comments': comments.get(user, 0)
            })

except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(f"ValueError: {e}")
except Exception as e:
    print(f"Error: {e}")