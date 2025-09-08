import os
import json
import csv

root_dir = "root_dir"

def get_story_engagement(root_dir):
    story_engagement = {}
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Iterate through 'your_instagram_activity' directory
        activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if not os.path.exists(activity_dir):
            return story_engagement

        # Iterate through 'content' directory
        content_dir = os.path.join(activity_dir, 'content')
        if not os.path.exists(content_dir):
            return story_engagement

        # Iterate through 'stories.json' file
        stories_file = os.path.join(content_dir, 'stories.json')
        if not os.path.exists(stories_file):
            return story_engagement

        # Open 'stories.json' file and load data
        with open(stories_file, 'r') as f:
            stories_data = json.load(f)

        # Iterate through stories and extract engagement data
        for story in stories_data['ig_stories']:
            media_owner = story.get('media_owner', '')
            if media_owner not in story_engagement:
                story_engagement[media_owner] = 0
            story_engagement[media_owner] += 1

        # Iterate through 'likes' directory
        likes_dir = os.path.join(activity_dir, 'likes')
        if not os.path.exists(likes_dir):
            return story_engagement

        # Iterate through 'liked_posts.json' file
        liked_posts_file = os.path.join(likes_dir, 'liked_posts.json')
        if not os.path.exists(liked_posts_file):
            return story_engagement

        # Open 'liked_posts.json' file and load data
        with open(liked_posts_file, 'r') as f:
            liked_posts_data = json.load(f)

        # Iterate through liked posts and extract engagement data
        for post in liked_posts_data['likes_media_likes']:
            media_owner = post.get('media_owner', '')
            if media_owner not in story_engagement:
                story_engagement[media_owner] = 0
            story_engagement[media_owner] += 1

        # Sort engagement data by value in descending order
        story_engagement = dict(sorted(story_engagement.items(), key=lambda item: item[1], reverse=True))

        return story_engagement

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def save_to_csv(story_engagement):
    try:
        # Create 'query_responses' directory if it does not exist
        query_responses_dir = 'query_responses'
        if not os.path.exists(query_responses_dir):
            os.makedirs(query_responses_dir)

        # Save engagement data to 'results.csv' file
        with open(os.path.join(query_responses_dir, 'results.csv'), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['User', 'Times Engaged'])
            for user, times_engaged in story_engagement.items():
                writer.writerow([user, times_engaged])

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    story_engagement = get_story_engagement(root_dir)
    if story_engagement:
        save_to_csv(story_engagement)
    else:
        # Save empty CSV file with column headers
        with open(os.path.join('query_responses', 'results.csv'), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['User', 'Times Engaged'])

if __name__ == "__main__":
    main()