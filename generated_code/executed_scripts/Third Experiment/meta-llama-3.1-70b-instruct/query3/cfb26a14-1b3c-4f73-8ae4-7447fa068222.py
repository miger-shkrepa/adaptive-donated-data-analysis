import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    posts_viewed = []
    try:
        ads_information_dir = os.path.join(root_dir, "ads_information")
        if not os.path.exists(ads_information_dir):
            raise FileNotFoundError("Error: The 'ads_information' directory does not exist.")
        
        ads_and_topics_dir = os.path.join(ads_information_dir, "ads_and_topics")
        if not os.path.exists(ads_and_topics_dir):
            raise FileNotFoundError("Error: The 'ads_and_topics' directory does not exist.")
        
        posts_viewed_file = os.path.join(ads_and_topics_dir, "posts_viewed.json")
        if not os.path.exists(posts_viewed_file):
            raise FileNotFoundError("Error: The 'posts_viewed.json' file does not exist.")
        
        with open(posts_viewed_file, 'r') as file:
            data = json.load(file)
            for post in data["impressions_history_posts_seen"]:
                timestamp = post["string_map_data"]["Time"]["timestamp"]
                date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
                posts_viewed.append((date, 1, "Daily"))
        
        # Calculate weekly posts viewed
        weekly_posts_viewed = {}
        for post in posts_viewed:
            date = post[0]
            year, week, _ = datetime.strptime(date, "%Y-%m-%d").isocalendar()
            week_key = f"Week {year}-{week}"
            if week_key in weekly_posts_viewed:
                weekly_posts_viewed[week_key] += 1
            else:
                weekly_posts_viewed[week_key] = 1
        
        for week, count in weekly_posts_viewed.items():
            posts_viewed.append((week, count, "Weekly"))
        
        return posts_viewed
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Failed to parse JSON - {e}")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred - {e}")

def save_to_csv(posts_viewed):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
            for post in posts_viewed:
                writer.writerow(post)
    
    except Exception as e:
        raise ValueError(f"ValueError: Failed to save to CSV - {e}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        
        posts_viewed = get_posts_viewed(root_dir)
        save_to_csv(posts_viewed)
    
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()