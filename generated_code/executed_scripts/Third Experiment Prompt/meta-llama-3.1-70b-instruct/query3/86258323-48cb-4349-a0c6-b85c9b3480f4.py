import os
import csv
import datetime
import json

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    posts_viewed = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "posts_viewed.json":
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for post in data["impressions_history_posts_seen"]:
                            timestamp = post["string_map_data"]["Time"]["timestamp"]
                            date = datetime.datetime.fromtimestamp(timestamp)
                            date_str = date.strftime('%Y-%m-%d')
                            if date_str not in posts_viewed:
                                posts_viewed[date_str] = 1
                            else:
                                posts_viewed[date_str] += 1
                except FileNotFoundError:
                    raise FileNotFoundError("Error: The file 'posts_viewed.json' does not exist.")
                except json.JSONDecodeError:
                    raise ValueError("Error: The file 'posts_viewed.json' is not a valid JSON file.")
    return posts_viewed

def get_weekly_posts_viewed(posts_viewed):
    weekly_posts_viewed = {}
    for date, count in posts_viewed.items():
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        week_str = date_obj.strftime('%Y-%W')
        if week_str not in weekly_posts_viewed:
            weekly_posts_viewed[week_str] = count
        else:
            weekly_posts_viewed[week_str] += count
    return weekly_posts_viewed

def write_to_csv(posts_viewed, weekly_posts_viewed):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for date, count in posts_viewed.items():
            writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})
        for week, count in weekly_posts_viewed.items():
            writer.writerow({'Date/Week': f'Week {week}', 'Posts Viewed': count, 'Type': 'Weekly'})

def main():
    try:
        posts_viewed = get_posts_viewed(root_dir)
        if not posts_viewed:
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
        else:
            weekly_posts_viewed = get_weekly_posts_viewed(posts_viewed)
            write_to_csv(posts_viewed, weekly_posts_viewed)
    except FileNotFoundError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()