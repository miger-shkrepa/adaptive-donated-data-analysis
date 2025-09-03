import csv
import os
import json
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])

    # Iterate over the daily and weekly posts
    for date in os.listdir(os.path.join(root_dir, 'media', 'posts')):
        date_path = os.path.join(root_dir, 'media', 'posts', date)
        if os.path.isdir(date_path):
            # Get the daily posts
            daily_posts = 0
            for file in os.listdir(date_path):
                if file.endswith('.json'):
                    try:
                        with open(os.path.join(date_path, file), 'r') as f:
                            data = json.load(f)
                            if 'structure' in data and 'impressions_history_posts_seen' in data['structure']:
                                daily_posts += len(data['structure']['impressions_history_posts_seen'])
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON file {file}: {e}")
                    except KeyError as e:
                        print(f"Error accessing key {e} in JSON file {file}")

            # Get the weekly posts
            weekly_posts = 0
            for file in os.listdir(date_path):
                if file.endswith('.json'):
                    try:
                        with open(os.path.join(date_path, file), 'r') as f:
                            data = json.load(f)
                            if 'structure' in data and 'impressions_history_posts_seen' in data['structure']:
                                weekly_posts += len(data['structure']['impressions_history_posts_seen'])
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON file {file}: {e}")
                    except KeyError as e:
                        print(f"Error accessing key {e} in JSON file {file}")

            # Write the daily and weekly posts to the CSV file
            writer.writerow([date, daily_posts, 'Daily'])
            if date.startswith('2022') or date.startswith('2023'):
                writer.writerow([f'Week {datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%W")}', weekly_posts, 'Weekly'])
            else:
                writer.writerow([f'Week {date[:4]}-{date[5:7]}', weekly_posts, 'Weekly'])

    # If the 'ads_information' directory exists, get the daily and weekly ads
    if os.path.exists(os.path.join(root_dir, 'ads_information')):
        ads_path = os.path.join(root_dir, 'ads_information')
        for date in os.listdir(ads_path):
            date_path = os.path.join(ads_path, date)
            if os.path.isdir(date_path):
                # Get the daily ads
                daily_ads = 0
                for file in os.listdir(date_path):
                    if file.endswith('.json'):
                        try:
                            with open(os.path.join(date_path, file), 'r') as f:
                                data = json.load(f)
                                if 'structure' in data and 'impressions_history_ads_seen' in data['structure']:
                                    daily_ads += len(data['structure']['impressions_history_ads_seen'])
                        except json.JSONDecodeError as e:
                            print(f"Error parsing JSON file {file}: {e}")
                        except KeyError as e:
                            print(f"Error accessing key {e} in JSON file {file}")

                # Get the weekly ads
                weekly_ads = 0
                for file in os.listdir(date_path):
                    if file.endswith('.json'):
                        try:
                            with open(os.path.join(date_path, file), 'r') as f:
                                data = json.load(f)
                                if 'structure' in data and 'impressions_history_ads_seen' in data['structure']:
                                    weekly_ads += len(data['structure']['impressions_history_ads_seen'])
                        except json.JSONDecodeError as e:
                            print(f"Error parsing JSON file {file}: {e}")
                        except KeyError as e:
                            print(f"Error accessing key {e} in JSON file {file}")

                # Write the daily and weekly ads to the CSV file
                writer.writerow([date, daily_ads, 'Daily'])
                if date.startswith('2022') or date.startswith('2023'):
                    writer.writerow([f'Week {datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%W")}', weekly_ads, 'Weekly'])
                else:
                    writer.writerow([f'Week {date[:4]}-{date[5:7]}', weekly_ads, 'Weekly'])