import os
import json
import csv

root_dir = "root_dir"

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")

def extract_topics_from_likes(data):
    topics = set()
    if 'likes_media_likes' in data:
        for item in data['likes_media_likes']:
            if 'title' in item:
                topics.add(item['title'])
            for string_list_data in item.get('string_list_data', []):
                if 'value' in string_list_data:
                    topics.add(string_list_data['value'])
    return topics

def extract_topics_from_saved(data):
    topics = set()
    if 'saved_saved_media' in data:
        for item in data['saved_saved_media']:
            if 'title' in item:
                topics.add(item['title'])
            for key, value in item.get('string_map_data', {}).items():
                if 'value' in value:
                    topics.add(value['value'])
    return topics

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        topics_of_interest = set()
        
        likes_file_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if os.path.exists(likes_file_path):
            likes_data = read_json_file(likes_file_path)
            topics_of_interest.update(extract_topics_from_likes(likes_data['structure']))
        
        saved_file_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
        if os.path.exists(saved_file_path):
            saved_data = read_json_file(saved_file_path)
            topics_of_interest.update(extract_topics_from_saved(saved_data['structure']))
        
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])
            for topic in topics_of_interest:
                writer.writerow([topic])
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()