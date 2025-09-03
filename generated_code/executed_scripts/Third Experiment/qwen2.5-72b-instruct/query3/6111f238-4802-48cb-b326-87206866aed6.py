import os
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Initialize the CSV file path
csv_file_path = 'query_responses/results.csv'

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: FileNotFoundError: The root directory does not exist.")

# Initialize the data structure to hold the results
results = []

# Function to get the week number from a date
def get_week_number(date):
    return date.strftime("Week %Y-%W")

# Function to process posts and count views
def process_posts(posts_dir):
    for year_month in os.listdir(posts_dir):
        year_month_path = os.path.join(posts_dir, year_month)
        if os.path.isdir(year_month_path):
            for file in os.listdir(year_month_path):
                file_path = os.path.join(year_month_path, file)
                if file.endswith('.srt') or file.endswith('.mp4') or file.endswith('.jpg'):
                    # Assuming each file represents a post viewed
                    file_date = datetime.strptime(year_month, "%Y%m")
                    daily_date = file_date.replace(day=1)
                    week_number = get_week_number(daily_date)
                    results.append([daily_date.strftime("%Y-%m-%d"), 1, 'Daily'])
                    results.append([week_number, 1, 'Weekly'])

# Check if the media/posts directory exists
posts_dir = os.path.join(root_dir, "media", "posts")
if not os.path.exists(posts_dir):
    # If the posts directory does not exist, create a CSV with only headers
    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Date/Week', 'Posts Viewed', 'Type'])
else:
    try:
        process_posts(posts_dir)
        
        # Aggregate the results
        aggregated_results = {}
        for row in results:
            key = (row[0], row[2])
            if key not in aggregated_results:
                aggregated_results[key] = 0
            aggregated_results[key] += row[1]
        
        # Write the aggregated results to the CSV file
        with open(csv_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Date/Week', 'Posts Viewed', 'Type'])
            for key, value in aggregated_results.items():
                csvwriter.writerow([key[0], value, key[1]])
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")