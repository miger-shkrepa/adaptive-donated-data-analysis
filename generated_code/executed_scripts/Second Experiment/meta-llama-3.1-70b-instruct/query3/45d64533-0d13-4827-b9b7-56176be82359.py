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
            raise FileNotFoundError("FileNotFoundError: The ads_and_topics directory does not exist.")
        
        posts_viewed_file = os.path.join(ads_and_topics_dir, "posts_viewed.json")
        if not os.path.exists(posts_viewed_file):
            return posts_viewed
        
        with open(posts_viewed_file, 'r') as file:
            data = json.load(file)
            for post in data["impressions_history_posts_seen"]:
                timestamp = post["string_map_data"]["Time"]["timestamp"]
                date = datetime.fromtimestamp(timestamp).date()
                week = date.isocalendar()[1]
                year = date.year
                
                # Daily
                date_str = date.strftime("%Y-%m-%d")
                if date_str not in posts_viewed:
                    posts_viewed[date_str] = {"Daily": 1, "Weekly": 0}
                else:
                    posts_viewed[date_str]["Daily"] += 1
                
                # Weekly
                week_str = f"Week {year}-{week:02d}"
                if week_str not in posts_viewed:
                    posts_viewed[week_str] = {"Daily": 0, "Weekly": 1}
                else:
                    posts_viewed[week_str]["Weekly"] += 1
        
        return posts_viewed
    
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def save_to_csv(posts_viewed):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
            for date, values in posts_viewed.items():
                for type, count in values.items():
                    writer.writerow([date, count, type])
    
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def main():
    try:
        posts_viewed = get_posts_viewed(root_dir)
        if not posts_viewed:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        else:
            save_to_csv(posts_viewed)
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

if __name__ == "__main__":
    main()