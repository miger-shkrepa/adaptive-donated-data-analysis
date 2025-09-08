import csv
import os
import datetime
import json

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    posts_viewed = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "ads_and_topics/posts_viewed.json":
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for item in data["structure"]["impressions_history_posts_seen"]:
                            date = item["string_map_data"]["Time"]["value"]
                            if date.startswith("2023-"):
                                date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
                            else:
                                date = datetime.datetime.strptime(date, "%Y-%W").strftime("%Y-%W")
                            posts_viewed.append((date, 1))
                except FileNotFoundError:
                    raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
                except json.JSONDecodeError:
                    raise ValueError("ValueError: The posts_viewed.json file is not a valid JSON.")
    return posts_viewed

def get_weekly_posts_viewed(posts_viewed):
    weekly_posts_viewed = {}
    for date, count in posts_viewed:
        if date.startswith("Week "):
            week = date[5:]
            if week not in weekly_posts_viewed:
                weekly_posts_viewed[week] = 0
            weekly_posts_viewed[week] += count
    return weekly_posts_viewed

def write_to_csv(posts_viewed, weekly_posts_viewed):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        for date, count in posts_viewed:
            writer.writerow([date, count, "Daily"])
        for week, count in weekly_posts_viewed.items():
            writer.writerow([week, count, "Weekly"])

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        posts_viewed = get_posts_viewed(root_dir)
        weekly_posts_viewed = get_weekly_posts_viewed(posts_viewed)
        write_to_csv(posts_viewed, weekly_posts_viewed)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()