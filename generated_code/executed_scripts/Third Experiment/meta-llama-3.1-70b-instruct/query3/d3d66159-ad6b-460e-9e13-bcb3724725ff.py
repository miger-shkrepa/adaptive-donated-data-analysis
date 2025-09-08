import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    posts_viewed = {}
    try:
        ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_and_topics_dir):
            raise FileNotFoundError("Error: The 'ads_and_topics' directory does not exist.")
        
        posts_viewed_file = os.path.join(ads_and_topics_dir, "posts_viewed.json")
        if not os.path.exists(posts_viewed_file):
            raise FileNotFoundError("Error: The 'posts_viewed.json' file does not exist.")
        
        with open(posts_viewed_file, 'r') as file:
            data = json.load(file)
            for post in data["impressions_history_posts_seen"]:
                timestamp = post["string_map_data"]["Time"]["timestamp"]
                date = datetime.fromtimestamp(timestamp).date()
                week = date.strftime("Week %Y-%W")
                date_str = date.strftime("%Y-%m-%d")
                
                if date_str not in posts_viewed:
                    posts_viewed[date_str] = 0
                if week not in posts_viewed:
                    posts_viewed[week] = 0
                
                posts_viewed[date_str] += 1
                posts_viewed[week] += 1
        
        return posts_viewed
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

def write_to_csv(posts_viewed):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
            for date, count in posts_viewed.items():
                if date.startswith("Week"):
                    writer.writerow([date, count, "Weekly"])
                else:
                    writer.writerow([date, count, "Daily"])
    
    except Exception as e:
        raise ValueError(f"Error: {e}")

def main():
    try:
        posts_viewed = get_posts_viewed(root_dir)
        if not posts_viewed:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        else:
            write_to_csv(posts_viewed)
    
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()