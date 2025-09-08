import os
import csv
import datetime

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    posts_viewed = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "posts_viewed.json":
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r') as file:
                        data = eval(file.read())
                        for post in data['impressions_history_posts_seen']:
                            timestamp = post['string_map_data']['Time']['timestamp']
                            date = datetime.datetime.fromtimestamp(timestamp)
                            date_str = date.strftime('%Y-%m-%d')
                            week_str = date.strftime('Week %Y-%W')
                            if date_str not in posts_viewed:
                                posts_viewed[date_str] = 0
                            if week_str not in posts_viewed:
                                posts_viewed[week_str] = 0
                            posts_viewed[date_str] += 1
                            posts_viewed[week_str] += 1
                except FileNotFoundError:
                    raise FileNotFoundError("FileNotFoundError: The file 'posts_viewed.json' does not exist.")
                except Exception as e:
                    raise ValueError("Error: " + str(e))
    return posts_viewed

def write_to_csv(posts_viewed):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for date, count in posts_viewed.items():
            if date.startswith('Week'):
                writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Weekly'})
            else:
                writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        posts_viewed = get_posts_viewed(root_dir)
        write_to_csv(posts_viewed)
    except Exception as e:
        raise Exception("Error: " + str(e))

if __name__ == "__main__":
    main()