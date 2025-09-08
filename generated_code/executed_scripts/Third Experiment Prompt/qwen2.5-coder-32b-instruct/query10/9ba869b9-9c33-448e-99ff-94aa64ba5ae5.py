import os
import csv

# Define the root directory
root_dir = "root_dir"

# Initialize a dictionary to store account views
account_views = {}

def process_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = eval(file.read())
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: Error reading the file {file_path}: {str(e)}")

def process_posts_viewed(data):
    if 'impressions_history_posts_seen' in data:
        for entry in data['impressions_history_posts_seen']:
            author = entry['string_map_data']['Author']['value']
            if author not in account_views:
                account_views[author] = {'Post Views': 0, 'Video Views': 0}
            account_views[author]['Post Views'] += 1

def process_videos_watched(data):
    if 'impressions_history_videos_watched' in data:
        for entry in data['impressions_history_videos_watched']:
            if 'string_map_data' in entry and 'Author' in entry['string_map_data']:
                author = entry['string_map_data']['Author']['value']
                if author not in account_views:
                    account_views[author] = {'Post Views': 0, 'Video Views': 0}
                account_views[author]['Video Views'] += 1

def main():
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Define the path to the posts_viewed.json and videos_watched.json files
        posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        videos_watched_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')
        
        # Process posts_viewed.json if it exists
        if os.path.exists(posts_viewed_path):
            posts_viewed_data = process_json_file(posts_viewed_path)
            process_posts_viewed(posts_viewed_data)
        
        # Process videos_watched.json if it exists
        if os.path.exists(videos_watched_path):
            videos_watched_data = process_json_file(videos_watched_path)
            process_videos_watched(videos_watched_data)
        
        # Define the output CSV file path
        output_csv_path = 'query_responses/results.csv'
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        
        # Write the results to the CSV file
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for account, views in account_views.items():
                writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        # Create an empty CSV file with headers if an error occurs
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()