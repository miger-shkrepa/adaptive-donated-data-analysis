import os
import json
import csv

root_dir = "root_dir"

def extract_advertisement_data(root_dir):
    ad_data = {}
    
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        likes_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        saved_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
        
        if os.path.exists(likes_path):
            with open(likes_path, 'r') as f:
                likes_data = json.load(f)
                for item in likes_data.get("likes_media_likes", []):
                    for data in item.get("string_list_data", []):
                        value = data.get("value")
                        if value and "advertisement" in value.lower():
                            company_name = value.split(" ")[0]  # Assuming company name is the first word
                            ad_data[company_name] = ad_data.get(company_name, 0) + 1
        
        if os.path.exists(saved_path):
            with open(saved_path, 'r') as f:
                saved_data = json.load(f)
                for item in saved_data.get("saved_saved_media", []):
                    for key, value in item.get("string_map_data", {}).items():
                        if "advertisement" in key.lower() or "advertisement" in str(value).lower():
                            company_name = key.split(" ")[0]  # Assuming company name is the first word
                            ad_data[company_name] = ad_data.get(company_name, 0) + 1
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")
    
    return ad_data

def save_to_csv(ad_data):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        if not ad_data:
            return
        
        for company, count in ad_data.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

try:
    ad_data = extract_advertisement_data(root_dir)
    save_to_csv(ad_data)
except Exception as e:
    print(e)