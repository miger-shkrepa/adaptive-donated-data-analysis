import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: The root directory does not exist.")

# Function to parse the JSON files and extract the required data
def parse_json_files(directory):
    posts_viewed = []

    # Walk through the directory structure
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == "posts_viewed.json":
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    for entry in data.get("impressions_history_posts_seen", []):
                        timestamp = entry["string_map_data"]["Time"]["timestamp"]
                        date = datetime.fromtimestamp(timestamp)
                        posts_viewed.append(date)

    return posts_viewed

# Function to generate the CSV file
def generate_csv(posts_viewed):
    # Create a dictionary to store the counts
    daily_counts = {}
    weekly_counts = {}

    for date in posts_viewed:
        date_str = date.strftime('%Y-%m-%d')
        week_str = f"Week {date.strftime('%Y-%U')}"

        if date_str in daily_counts:
            daily_counts[date_str] += 1
        else:
            daily_counts[date_str] = 1

        if week_str in weekly_counts:
            weekly_counts[week_str] += 1
        else:
            weekly_counts[week_str] = 1

    # Write the results to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for date, count in daily_counts.items():
            writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})

        for week, count in weekly_counts.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

# Main function to execute the script
def main():
    try:
        posts_viewed = parse_json_files(root_dir)
        generate_csv(posts_viewed)
        print("CSV file generated successfully.")
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

if __name__ == "__main__":
    main()