import os
import json
import csv

root_dir = "root_dir"

def extract_interests_from_json(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            interests = set()
            for media_like in data.get('likes_media_likes', []):
                title = media_like.get('title')
                if title:
                    interests.add(title)
            return interests
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def write_interests_to_csv(interests, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])
            for interest in interests:
                writer.writerow([interest])
    except Exception as e:
        raise IOError(f"Error: Failed to write to CSV file. Reason: {str(e)}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if not os.path.exists(liked_posts_path):
            write_interests_to_csv([], 'query_responses/results.csv')
            return
        
        interests = extract_interests_from_json(liked_posts_path)
        write_interests_to_csv(interests, 'query_responses/results.csv')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()