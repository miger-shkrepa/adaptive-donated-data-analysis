import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Check if 'your_instagram_activity' directory exists
        your_instagram_activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if not os.path.exists(your_instagram_activity_dir):
            return companies
        
        # Check if 'comments' directory exists
        comments_dir = os.path.join(your_instagram_activity_dir, 'comments')
        if os.path.exists(comments_dir):
            # Check if 'reels_comments.json' file exists
            reels_comments_file = os.path.join(comments_dir, 'reels_comments.json')
            if os.path.exists(reels_comments_file):
                with open(reels_comments_file, 'r') as file:
                    data = json.load(file)
                    for comment in data['comments_reels_comments']:
                        # Assuming 'Media Owner' is the company name
                        companies.add(comment['string_map_data']['Media Owner']['value'])
        
        # Check if 'content' directory exists
        content_dir = os.path.join(your_instagram_activity_dir, 'content')
        if os.path.exists(content_dir):
            # Check if 'profile_photos.json' file exists
            profile_photos_file = os.path.join(content_dir, 'profile_photos.json')
            if os.path.exists(profile_photos_file):
                with open(profile_photos_file, 'r') as file:
                    data = json.load(file)
                    for photo in data['ig_profile_picture']:
                        # Assuming 'cross_post_source' is the company name
                        if 'cross_post_source' in photo and 'source_app' in photo['cross_post_source']:
                            companies.add(photo['cross_post_source']['source_app'])
        
        # Check if 'likes' directory exists
        likes_dir = os.path.join(your_instagram_activity_dir, 'likes')
        if os.path.exists(likes_dir):
            # Check if 'liked_posts.json' file exists
            liked_posts_file = os.path.join(likes_dir, 'liked_posts.json')
            if os.path.exists(liked_posts_file):
                with open(liked_posts_file, 'r') as file:
                    data = json.load(file)
                    for like in data['likes_media_likes']:
                        # Assuming 'title' is the company name
                        companies.add(like['title'])
        
        # Check if 'messages' directory exists
        messages_dir = os.path.join(your_instagram_activity_dir, 'messages')
        if os.path.exists(messages_dir):
            # Check if 'inbox' directory exists
            inbox_dir = os.path.join(messages_dir, 'inbox')
            if os.path.exists(inbox_dir):
                for filename in os.listdir(inbox_dir):
                    if filename.endswith('.json'):
                        file_path = os.path.join(inbox_dir, filename)
                        with open(file_path, 'r') as file:
                            data = json.load(file)
                            for message in data['messages']:
                                # Assuming 'sender_name' is the company name
                                companies.add(message['sender_name'])
        
        return companies
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(companies):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Company Name'])
            for company in companies:
                writer.writerow([company])
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    companies = get_companies_with_access(root_dir)
    save_to_csv(companies)

if __name__ == "__main__":
    main()