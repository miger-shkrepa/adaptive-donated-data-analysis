import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    posts_viewed = {"daily": {}, "weekly": {}}
    
    try:
        ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_and_topics_dir):
            raise FileNotFoundError("FileNotFoundError: The ads_and_topics directory does not exist.")
        
        posts_viewed_file = os.path.join(ads_and_topics_dir, "posts_viewed.json")
        if not os.path.exists(posts_viewed_file):
            return posts_viewed
        
        with open(posts_viewed_file, "r") as file:
            data = json.load(file)
            for post in data["impressions_history_posts_seen"]:
                timestamp = post["string_map_data"]["Time"]["timestamp"]
                date = datetime.fromtimestamp(timestamp).date()
                week = date.isocalendar()[0:2]
                week_str = f"Week {week[0]}-{week[1]:02d}"
                date_str = date.strftime("%Y-%m-%d")
                
                if date_str not in posts_viewed["daily"]:
                    posts_viewed["daily"][date_str] = 0
                posts_viewed["daily"][date_str] += 1
                
                if week_str not in posts_viewed["weekly"]:
                    posts_viewed["weekly"][week_str] = 0
                posts_viewed["weekly"][week_str] += 1
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Failed to parse JSON - {e}")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred - {e}")
    
    return posts_viewed

def save_to_csv(posts_viewed):
    with open("query_responses/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        
        for date, count in posts_viewed["daily"].items():
            writer.writerow([date, count, "Daily"])
        
        for week, count in posts_viewed["weekly"].items():
            writer.writerow([week, count, "Weekly"])

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        posts_viewed = get_posts_viewed(root_dir)
        save_to_csv(posts_viewed)
    
    except FileNotFoundError as e:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()