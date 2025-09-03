import os
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Function to parse the directory structure and extract relevant data
def parse_directory_structure(root_dir):
    data = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    try:
                        content = f.read()
                        # Assuming the JSON structure is known and can be parsed
                        # Extract relevant data from the JSON content
                        # For example, extracting timestamps and post views
                        # This is a placeholder for actual parsing logic
                        # data.append((timestamp, post_views, 'Daily' or 'Weekly'))
                    except Exception as e:
                        print(f"Error parsing {file_path}: {e}")
    return data

# Function to aggregate data into daily and weekly views
def aggregate_data(data):
    daily_views = {}
    weekly_views = {}

    for timestamp, post_views, view_type in data:
        date = datetime.fromtimestamp(timestamp)
        date_str = date.strftime('%Y-%m-%d')
        week_str = f"Week {date.strftime('%Y-%W')}"

        if view_type == 'Daily':
            if date_str in daily_views:
                daily_views[date_str] += post_views
            else:
                daily_views[date_str] = post_views
        elif view_type == 'Weekly':
            if week_str in weekly_views:
                weekly_views[week_str] += post_views
            else:
                weekly_views[week_str] = post_views

    return daily_views, weekly_views

# Function to write the aggregated data to a CSV file
def write_to_csv(daily_views, weekly_views, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for date, views in daily_views.items():
            writer.writerow({'Date/Week': date, 'Posts Viewed': views, 'Type': 'Daily'})

        for week, views in weekly_views.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': views, 'Type': 'Weekly'})

# Main function to execute the script
def main():
    try:
        data = parse_directory_structure(root_dir)
        daily_views, weekly_views = aggregate_data(data)
        output_path = 'query_responses/results.csv'
        write_to_csv(daily_views, weekly_views, output_path)
        print(f"CSV file generated successfully at {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()