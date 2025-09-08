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
        
        with open(posts_viewed_file, "r") as file:
            data = json.load(file)
            for post in data["impressions_history_posts_seen"]:
                timestamp = post["string_map_data"]["Time"]["timestamp"]
                date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
                week = datetime.fromtimestamp(timestamp).strftime("%Y-%W")
                if date not in posts_viewed:
                    posts_viewed[date] = 0
                if week not in posts_viewed:
                    posts_viewed[week] = 0
                posts_viewed[date] += 1
                posts_viewed[week] += 1
    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise ValueError("Error: An error occurred while processing the data. " + str(e))
    
    return posts_viewed

def write_to_csv(posts_viewed):
    try:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
            for date, count in posts_viewed.items():
                if date.startswith("Week"):
                    writer.writerow([date, count, "Weekly"])
                else:
                    writer.writerow([date, count, "Daily"])
    except Exception as e:
        raise ValueError("Error: An error occurred while writing to the CSV file. " + str(e))

def main():
    try:
        posts_viewed = get_posts_viewed(root_dir)
        write_to_csv(posts_viewed)
    except FileNotFoundError as e:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        raise e
    except Exception as e:
        raise e

if __name__ == "__main__":
    main()