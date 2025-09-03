import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    posts_viewed = {}
    try:
        ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_and_topics_dir):
            raise FileNotFoundError("FileNotFoundError: The ads_and_topics directory does not exist.")
        
        posts_viewed_file = os.path.join(ads_and_topics_dir, "posts_viewed.json")
        if not os.path.exists(posts_viewed_file):
            raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
        
        with open(posts_viewed_file, 'r') as file:
            data = json.load(file)
            for post in data["impressions_history_posts_seen"]:
                time = post["string_map_data"]["Time"]["timestamp"]
                date = datetime.fromtimestamp(time).strftime('%Y-%m-%d')
                if date not in posts_viewed:
                    posts_viewed[date] = 1
                else:
                    posts_viewed[date] += 1
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")
    
    return posts_viewed

def get_weekly_posts_viewed(posts_viewed):
    weekly_posts_viewed = {}
    for date, count in posts_viewed.items():
        year, month, day = map(int, date.split('-'))
        week_number = datetime(year, month, day).isocalendar()[1]
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
        raise ValueError(f"Error: {e}")

def main():
    try:
        posts_viewed = get_posts_viewed(root_dir)
        weekly_posts_viewed = get_weekly_posts_viewed(posts_viewed)
        write_to_csv(posts_viewed, weekly_posts_viewed)
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()