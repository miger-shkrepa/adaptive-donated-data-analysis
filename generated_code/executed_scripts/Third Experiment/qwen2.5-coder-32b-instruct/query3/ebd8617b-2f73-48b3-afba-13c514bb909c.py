import os
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to parse the timestamp and convert it to a date or week
def parse_timestamp(timestamp):
    date = datetime.fromtimestamp(timestamp)
    return date.strftime('%Y-%m-%d'), date.strftime('Week %Y-%W')

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize lists to store the data
data = []

# Path to the posts_viewed.json file
posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Check if the posts_viewed.json file exists
if os.path.exists(posts_viewed_path):
    with open(posts_viewed_path, 'r') as file:
        import json
        posts_viewed_data = json.load(file)
        
        # Extract the impressions history
        impressions_history = posts_viewed_data.get('structure', {}).get('impressions_history_posts_seen', [])
        
        # Process each impression
        for impression in impressions_history:
            string_map_data = impression.get('string_map_data', {})
            time_data = string_map_data.get('Time', {})
            timestamp = time_data.get('timestamp')
            
            if timestamp:
                date_str, week_str = parse_timestamp(timestamp)
                data.append((date_str, 1, 'Daily'))
                data.append((week_str, 1, 'Weekly'))
else:
    # If the file does not exist, treat its contribution as 0
    pass

# Aggregate the data
from collections import defaultdict

daily_counts = defaultdict(int)
weekly_counts = defaultdict(int)

for date_str, count, period in data:
    if period == 'Daily':
        daily_counts[date_str] += count
    elif period == 'Weekly':
        weekly_counts[date_str] += count

# Prepare the final data for CSV
final_data = []

for date_str, count in daily_counts.items():
    final_data.append((date_str, count, 'Daily'))

for week_str, count in weekly_counts.items():
    final_data.append((week_str, count, 'Weekly'))

# Sort the final data by date/week
final_data.sort(key=lambda x: x[0])

# Define the output CSV path
output_csv_path = 'query_responses/results.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Write the data to the CSV file
with open(output_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
    writer.writerows(final_data)