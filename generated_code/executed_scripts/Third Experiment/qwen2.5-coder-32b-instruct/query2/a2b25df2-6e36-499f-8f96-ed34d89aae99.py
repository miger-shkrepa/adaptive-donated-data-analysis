import os
import json
import csv

# Variable referring to the file input
root_dir = "root_dir"

# Function to read JSON files and count impressions
def count_impressions(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'impressions_history_posts_seen' in data:
                return len(data['impressions_history_posts_seen'])
            elif 'impressions_history_videos_watched' in data:
                return len(data['impressions_history_videos_watched'])
            else:
                return 0
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {str(e)}")

# Main function to process the data and generate the CSV
def generate_ads_viewed_csv(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Define the path to the ads information directory
        ads_dir = os.path.join(root_dir, 'ads_information', 'ads_and_topics')
        
        # Check if the ads directory exists
        if not os.path.exists(ads_dir):
            raise FileNotFoundError("FileNotFoundError: The ads directory does not exist.")
        
        # Initialize the total number of ads viewed
        total_ads_viewed = 0
        
        # Process posts_viewed.json
        posts_viewed_path = os.path.join(ads_dir, 'posts_viewed.json')
        if os.path.exists(posts_viewed_path):
            total_ads_viewed += count_impressions(posts_viewed_path)
        
        # Process videos_watched.json
        videos_watched_path = os.path.join(ads_dir, 'videos_watched.json')
        if os.path.exists(videos_watched_path):
            total_ads_viewed += count_impressions(videos_watched_path)
        
        # Define the output CSV path
        output_csv_path = 'query_responses/results.csv'
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        
        # Write the CSV file
        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Company Name', 'Number of Ads Viewed'])
            # Since we don't have company names, we use a placeholder
            csv_writer.writerow(['Unknown Company', total_ads_viewed])
    
    except Exception as e:
        print(str(e))

# Call the main function
generate_ads_viewed_csv(root_dir)