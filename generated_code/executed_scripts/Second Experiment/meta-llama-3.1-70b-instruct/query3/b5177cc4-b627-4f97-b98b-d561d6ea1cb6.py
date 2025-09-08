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
            return posts_viewed
        
        with open(posts_viewed_file, 'r') as file:
            data = json.load(file)
            for post in data["impressions_history_posts_seen"]:
                timestamp = post["string_map_data"]["Time"]["timestamp"]
                date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                if date not in posts_viewed:
                    posts_viewed[date] = 1
                else:
                    posts_viewed[date] += 1
    except Exception as e:
        raise ValueError("Error: " + str(e))
    
    return posts_viewed

def get_weekly_posts_viewed(posts_viewed):
    weekly_posts_viewed = {}
    for date, count in posts_viewed.items():
        year, month, day = date.split('-')
        week_number = datetime(int(year), int(month), int(day)).isocalendar()[1]
        week = f"Week {year}-{week_number:02d}"
        if week not in weekly_posts_viewed:
            weekly_posts_viewed[week] = count
        else:
            weekly_posts_viewed[week] += count
    return weekly_posts_viewed

def write_to_csv(posts_viewed, weekly_posts_viewed):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
            for date, count in posts_viewed.items():
                writer.writerow([date, count, "Daily"])
            for week, count in weekly_posts_viewed.items():
                writer.writerow([week, count, "Weekly"])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        
        posts_viewed = get_posts_viewed(root_dir)
        weekly_posts_viewed = get_weekly_posts_viewed(posts_viewed)
        write_to_csv(posts_viewed, weekly_posts_viewed)
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()