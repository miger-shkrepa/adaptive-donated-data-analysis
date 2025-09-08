import os
import csv
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

# Function to parse the creation timestamp from a post
def parse_creation_timestamp(post):
    return post.get('creation_timestamp', 0)

# Function to count posts per day and per week
def count_posts_by_date_and_week(posts):
    daily_count = {}
    weekly_count = {}

    for post in posts:
        timestamp = parse_creation_timestamp(post)
        if timestamp == 0:
            continue
        date = datetime.fromtimestamp(timestamp)
        date_str = date.strftime('%Y-%m-%d')
        week_str = date.strftime('Week %Y-%W')

        if date_str in daily_count:
            daily_count[date_str] += 1
        else:
            daily_count[date_str] = 1

        if week_str in weekly_count:
            weekly_count[week_str] += 1
        else:
            weekly_count[week_str] = 1

    return daily_count, weekly_count

# Main function to process the directory and generate the CSV
def generate_posts_viewed_csv(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize counters
        daily_count = {}
        weekly_count = {}

        # Path to the posts directory
        posts_dir = os.path.join(root_dir, 'your_instagram_activity', 'media', 'posts')

        # Check if the posts directory exists
        if not os.path.exists(posts_dir):
            # If the directory does not exist, return an empty CSV with headers
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
            return

        # Iterate through each file in the posts directory
        for filename in os.listdir(posts_dir):
            file_path = os.path.join(posts_dir, filename)
            if os.path.isfile(file_path) and filename.endswith('.json'):
                try:
                    with open(file_path, 'r') as file:
                        import json
                        data = json.load(file)
                        if 'posts' in data:
                            posts = data['posts']
                            daily, weekly = count_posts_by_date_and_week(posts)
                            daily_count.update(daily)
                            weekly_count.update(weekly)
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Error decoding JSON file {file_path}: {e}")

        # Prepare the data for CSV
        csv_data = []
        for date, count in daily_count.items():
            csv_data.append([date, count, 'Daily'])
        for week, count in weekly_count.items():
            csv_data.append([week, count, 'Weekly'])

        # Sort the data by date/week
        csv_data.sort(key=lambda x: datetime.strptime(x[0].replace('Week ', ''), '%Y-%m-%d' if 'Week' not in x[0] else '%Y-%W'))

        # Write the CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
            writer.writerows(csv_data)

    except Exception as e:
        print(f"Error: {e}")

# Call the main function
generate_posts_viewed_csv(root_dir)