import csv
import os
import datetime

def process_directory(root_dir):
    try:
        posts_viewed = 0
        daily_posts_viewed = 0
        weekly_posts_viewed = 0
        daily_count = 0
        weekly_count = 0

        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith('.json'):
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as f:
                        data = eval(f.read())

                        if 'ads_and_topics' in data and 'ads_viewed.json' in data['ads_and_topics']:
                            for item in data['ads_and_topics']['ads_viewed.json']['structure']['impressions_history_ads_seen']:
                                if 'string_map_data' in item and 'Time' in item['string_map_data']:
                                    timestamp = item['string_map_data']['Time']['timestamp']
                                    if timestamp % 7 == 0:
                                        weekly_posts_viewed += 1
                                        weekly_count += 1
                                    else:
                                        daily_posts_viewed += 1
                                        daily_count += 1

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
            for i in range(daily_count):
                writer.writerow([datetime.date.today().strftime('%Y-%m-%d'), daily_posts_viewed, 'Daily'])
                daily_posts_viewed = 0
            for i in range(weekly_count):
                writer.writerow([f'Week {datetime.date.today().isocalendar()[0]}-{datetime.date.today().isocalendar()[1]}', weekly_posts_viewed, 'Weekly'])
                weekly_posts_viewed = 0

    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise ValueError("ValueError: " + str(e))

root_dir = "root_dir"
process_directory(root_dir)