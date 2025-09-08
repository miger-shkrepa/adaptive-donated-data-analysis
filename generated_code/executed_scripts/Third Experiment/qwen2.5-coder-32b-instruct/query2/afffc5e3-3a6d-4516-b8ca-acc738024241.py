import os
import csv
import json

root_dir = "root_dir"

def main():
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Define the path to the posts_viewed.json file
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        
        # Check if the posts_viewed.json file exists
        if not os.path.exists(posts_viewed_path):
            raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
        
        # Read the posts_viewed.json file
        with open(posts_viewed_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Initialize a dictionary to count the number of ads viewed per company
        ads_count = {}
        
        # Process the data to count ads viewed per company
        for entry in data.get('impressions_history_posts_seen', []):
            author = entry.get('string_map_data', {}).get('Author', {}).get('value', 'Unknown')
            if author not in ads_count:
                ads_count[author] = 0
            ads_count[author] += 1
        
        # Prepare the data for writing to CSV
        csv_data = [['Company Name', 'Number of Ads Viewed']]
        for company, count in ads_count.items():
            csv_data.append([company, count])
        
        # Write the data to a CSV file
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(csv_data)
    
    except FileNotFoundError as e:
        # Handle file not found errors
        print(e)
        # Create an empty CSV with headers if the file is not found
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name', 'Number of Ads Viewed'])
    except ValueError as e:
        # Handle value errors
        print(f"ValueError: {e}")
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")

if __name__ == "__main__":
    main()