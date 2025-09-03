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

# Function to process interactions
def process_interactions(directory):
    interactions = {}

    # Placeholder for processing different types of interactions
    # This example assumes the structure and files are as described
    # You need to adjust the paths and processing logic based on actual data

    # Example paths (adjust as necessary)
    post_likes_path = os.path.join(directory, 'likes', 'post_likes.json')
    story_likes_path = os.path.join(directory, 'likes', 'story_likes.json')
    comments_path = os.path.join(directory, 'comments', 'comments.json')

    # Process post likes
    if os.path.exists(post_likes_path):
        post_likes = read_json_file(post_likes_path)
        for like in post_likes:
            user = like.get('user')
            if user:
                if user not in interactions:
                    interactions[user] = {'Post Likes': 0, 'Story Likes': 0, 'Comments': 0}
                interactions[user]['Post Likes'] += 1

    # Process story likes
    if os.path.exists(story_likes_path):
        story_likes = read_json_file(story_likes_path)
        for like in story_likes:
            user = like.get('user')
            if user:
                if user not in interactions:
                    interactions[user] = {'Post Likes': 0, 'Story Likes': 0, 'Comments': 0}
                interactions[user]['Story Likes'] += 1

    # Process comments
    if os.path.exists(comments_path):
        comments = read_json_file(comments_path)
        for comment in comments:
            user = comment.get('user')
            if user:
                if user not in interactions:
                    interactions[user] = {'Post Likes': 0, 'Story Likes': 0, 'Comments': 0}
                interactions[user]['Comments'] += 1

    return interactions

# Function to write results to CSV
def write_to_csv(interactions):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user, data in interactions.items():
            writer.writerow({'User': user, **data})

# Main function
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    interactions = process_interactions(root_dir)

    # Sort interactions by total interactions
    sorted_interactions = sorted(interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)

    # Get top 20 interactions
    top_20_interactions = dict(sorted_interactions[:20])

    write_to_csv(top_20_interactions)

if __name__ == "__main__":
    main()