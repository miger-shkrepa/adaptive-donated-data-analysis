import os
import json
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the path to the JSON file
json_file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
output_csv_path = "query_responses/results.csv"

# Function to convert timestamp to date and week
def convert_timestamp(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    date_str = dt.strftime('%Y-%m-%d')
    week_str = f"Week {dt.strftime('%Y-%W')}"
    return date_str, week_str

# Function to write CSV file
def write_csv(data, output_path):
    with open(output_path, 'w') as f:
        f.write("Date/Week,Posts Viewed,Type\n")
        for entry in data:
            f.write(f"{entry['date_week']},{entry['count']},{entry['type']}\n")

# Main function to process the data
def process_data():
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Check if the JSON file exists
        if not os.path.exists(json_file_path):
            # If the file does not exist, write only the column headers to the CSV
            write_csv([], output_csv_path)
            return
        
        # Load the JSON data
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        # Check if the required key exists in the JSON data
        if 'impressions_history_posts_seen' not in data:
            raise ValueError("ValueError: The required key 'impressions_history_posts_seen' is missing in the JSON data.")
        
        # Initialize dictionaries to store daily and weekly counts
        daily_counts = {}
        weekly_counts = {}
        
        # Process each entry in the impressions_history_posts_seen
        for entry in data['impressions_history_posts_seen']:
            if 'string_map_data' in entry and 'Time' in entry['string_map_data'] and 'timestamp' in entry['string_map_data']['Time']:
                timestamp = entry['string_map_data']['Time']['timestamp']
                date_str, week_str = convert_timestamp(timestamp)
                
                # Update daily counts
                if date_str in daily_counts:
                    daily_counts[date_str] += 1
                else:
                    daily_counts[date_str] = 1
                
                # Update weekly counts
                if week_str in weekly_counts:
                    weekly_counts[week_str] += 1
                else:
                    weekly_counts[week_str] = 1
        
        # Prepare the data for CSV
        csv_data = []
        for date, count in daily_counts.items():
            csv_data.append({'date_week': date, 'count': count, 'type': 'Daily'})
        for week, count in weekly_counts.items():
            csv_data.append({'date_week': week, 'count': count, 'type': 'Weekly'})
        
        # Sort the data by date/week
        csv_data.sort(key=lambda x: x['date_week'])
        
        # Write the CSV file
        write_csv(csv_data, output_csv_path)
    
    except FileNotFoundError as e:
        print(e)
        write_csv([], output_csv_path)
    except ValueError as e:
        print(e)
        write_csv([], output_csv_path)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        write_csv([], output_csv_path)

# Execute the main function
process_data()