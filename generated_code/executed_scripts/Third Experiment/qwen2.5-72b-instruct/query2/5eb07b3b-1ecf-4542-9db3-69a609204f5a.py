import os
import json
import csv

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    ads_data = {}
    ads_viewed = 0

    # Check if the necessary files exist
    liked_posts_path = os.path.join(root_dir, "likes", "liked_posts.json")
    saved_posts_path = os.path.join(root_dir, "saved", "saved_posts.json")

    if os.path.exists(liked_posts_path):
        with open(liked_posts_path, 'r') as file:
            liked_posts = json.load(file)
            for media_like in liked_posts.get("likes_media_likes", []):
                for string_data in media_like.get("string_list_data", []):
                    if "value" in string_data and "href" in string_data:
                        company_name = string_data["value"]
                        ads_data[company_name] = ads_data.get(company_name, 0) + 1
                        ads_viewed += 1

    if os.path.exists(saved_posts_path):
        with open(saved_posts_path, 'r') as file:
            saved_posts = json.load(file)
            for saved_media in saved_posts.get("saved_saved_media", []):
                string_map_data = saved_media.get("string_map_data", {}).get("Saved on", {})
                if "value" in string_map_data and "href" in string_map_data:
                    company_name = string_map_data["value"]
                    ads_data[company_name] = ads_data.get(company_name, 0) + 1
                    ads_viewed += 1

    # Write the results to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for company, count in ads_data.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

    if not ads_data:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

except Exception as e:
    raise ValueError(f"Error: {str(e)}")