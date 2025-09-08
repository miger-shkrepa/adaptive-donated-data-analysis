import os
import json
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file and extract timestamps
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to extract timestamps from liked_posts.json
def extract_liked_timestamps(data):
    timestamps = []
    if 'likes_media_likes' in data:
        for item in data['likes_media_likes']:
            for entry in item['string_list_data']:
                if 'timestamp' in entry:
                    timestamps.append(entry['timestamp'])
    return timestamps

# Function to extract timestamps from saved_posts.json
def extract_saved_timestamps(data):
    timestamps = []
    if 'saved_saved_media' in data:
        for item in data['saved_saved_media']:
            if 'string_map_data' in item and 'Saved on' in item['string_map_data']:
                if 'timestamp' in item['string_map_data']['Saved on']:
                    timestamps.append(item['string_map_data']['Saved on']['timestamp'])
    return timestamps

# Function to aggregate timestamps into daily and weekly counts
def aggregate_timestamps(timestamps):
    daily_counts = {}
    weekly_counts = {}
    
    for timestamp in timestamps:
        dt = datetime.fromtimestamp(timestamp)
        date_str = dt.strftime('%Y-%m-%d')
        week_str = dt.strftime('Week %Y-%W')
        
        if date_str in daily_counts:
            daily_counts[date_str] += 1
        else:
            daily_counts[date_str] = 1
        
        if week_str in weekly_counts:
            weekly_counts[week_str] += 1
        else:
            weekly_counts[week_str] = 1
    
    return daily_counts, weekly_counts

# Main function to process the data and generate the CSV
def process_data(root_dir):
    liked_file_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    saved_file_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
    
    liked_data = {}
    saved_data = {}
    
    if os.path.exists(liked_file_path):
        liked_data = read_json_file(liked_file_path)
    
    if os.path.exists(saved_file_path):
        saved_data = read_json_file(saved_file_path)
    
    liked_timestamps = extract_liked_timestamps(liked_data)
    saved_timestamps = extract_saved_timestamps(saved_data)
    
    all_timestamps = liked_timestamps + saved_timestamps
    
    daily_counts, weekly_counts = aggregate_timestamps(all_timestamps)
    
    # Prepare the CSV content
    csv_content = "Date/Week,Posts Viewed,Type\n"
    
    for date, count in daily_counts.items():
        csv_content += f"{date},{count},Daily\n"
    
    for week, count in weekly_counts.items():
        csv_content += f"{week},{count},Weekly\n"
    
    # Write the CSV content to the output file
    output_path = "query_responses/results.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(csv_content)

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Process the data
process_data(root_dir)