import os
import json
import csv

root_dir = "root_dir"

def extract_company_names_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")
    
    company_names = set()
    
    if 'likes_media_likes' in data:
        for item in data['likes_media_likes']:
            for string_data in item.get('string_list_data', []):
                value = string_data.get('value')
                if value:
                    company_names.add(value)
    
    if 'saved_saved_media' in data:
        for item in data['saved_saved_media']:
            for key, value in item.get('string_map_data', {}).items():
                if key == 'Saved on':
                    company_name = value.get('value')
                    if company_name:
                        company_names.add(company_name)
    
    return company_names

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
        
        company_names = set()
        
        if os.path.exists(liked_posts_path):
            company_names.update(extract_company_names_from_json(liked_posts_path))
        
        if os.path.exists(saved_posts_path):
            company_names.update(extract_company_names_from_json(saved_posts_path))
        
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
            for company in company_names:
                writer.writerow([company])
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()