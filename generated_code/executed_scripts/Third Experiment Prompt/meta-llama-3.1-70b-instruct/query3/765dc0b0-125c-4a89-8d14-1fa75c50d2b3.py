import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    posts_viewed = {}
    try:
        ads_info_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_info_dir):
            raise FileNotFoundError("Error: The 'ads_information/ads_and_topics' directory does not exist.")
        
        posts_viewed_file = os.path.join(ads_info_dir, "posts_viewed.json")
        if not os.path.exists(posts_viewed_file):
            raise FileNotFoundError("Error: The 'posts_viewed.json' file does not exist.")
        
        with open(posts_viewed_file, "r") as f:
            data = json.load(f)
            for post in data["impressions_history_posts_seen"]:
                timestamp = post["string_map_data"]["Time"]["timestamp"]
                date = datetime.fromtimestamp(timestamp)
                date_str = date.strftime("%Y-%m-%d")
                week_str = date.strftime("Week %Y-%W")
                if date_str not in posts_viewed:
                    posts_viewed[date_str] = 0
                if week_str not in posts_viewed:
                    posts_viewed[week_str] = 0
                posts_viewed[date_str] += 1
                posts_viewed[week_str] += 1
    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise ValueError("Error: An error occurred while processing the data. " + str(e))
    
    return posts_viewed

def write_to_csv(posts_viewed):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        fieldnames = ["Date/Week", "Posts Viewed", "Type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for date, count in posts_viewed.items():
            if date.startswith("Week"):
                writer.writerow({"Date/Week": date, "Posts Viewed": count, "Type": "Weekly"})
            else:
                writer.writerow({"Date/Week": date, "Posts Viewed": count, "Type": "Daily"})

def main():
    try:
        posts_viewed = get_posts_viewed(root_dir)
        write_to_csv(posts_viewed)
    except FileNotFoundError as e:
        print(e)
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            fieldnames = ["Date/Week", "Posts Viewed", "Type"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()