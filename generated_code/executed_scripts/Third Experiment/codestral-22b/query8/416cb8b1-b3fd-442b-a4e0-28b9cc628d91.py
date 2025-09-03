import os
import json
import csv

def get_interactions(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    interactions = {}

    # Process post likes
    post_likes_path = os.path.join(root_dir, 'likes', 'posts_liked.json')
    if os.path.exists(post_likes_path):
        with open(post_likes_path, 'r') as f:
            post_likes = json.load(f)
            for post in post_likes['likes_media_likes']:
                user = post['title']
                if user not in interactions:
                    interactions[user] = {'Post Likes': 1, 'Story Likes': 0, 'Comments': 0}
                else:
                    interactions[user]['Post Likes'] += 1

    # Process story likes
    story_likes_path = os.path.join(root_dir, 'story_interactions', 'story_likes.json')
    if os.path.exists(story_likes_path):
        with open(story_likes_path, 'r') as f:
            story_likes = json.load(f)
            for story in story_likes['story_activities_story_likes']:
                user = story['title']
                if user not in interactions:
                    interactions[user] = {'Post Likes': 0, 'Story Likes': 1, 'Comments': 0}
                else:
                    interactions[user]['Story Likes'] += 1

    # Process comments
    comments_path = os.path.join(root_dir, 'comments', 'comments.json')
    if os.path.exists(comments_path):
        with open(comments_path, 'r') as f:
            comments = json.load(f)
            for comment in comments['comments_media_comments']:
                user = comment['title']
                if user not in interactions:
                    interactions[user] = {'Post Likes': 0, 'Story Likes': 0, 'Comments': 1}
                else:
                    interactions[user]['Comments'] += 1

    # Sort interactions by total count
    sorted_interactions = sorted(interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)

    # Write results to CSV file
    with open('query_responses/results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
        for user, counts in sorted_interactions[:20]:
            writer.writerow([user, counts['Post Likes'], counts['Story Likes'], counts['Comments']])

root_dir = "root_dir"
get_interactions(root_dir)