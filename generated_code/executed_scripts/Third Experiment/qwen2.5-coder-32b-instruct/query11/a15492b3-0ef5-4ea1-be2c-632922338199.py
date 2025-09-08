import os
import csv

root_dir = "root_dir"

def find_unliked_accounts(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Define the path to the posts_viewed.json and posts_you're_not_interested_in.json files
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        posts_not_interested_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_you're_not_interested_in.json")
        
        # Initialize sets to store viewed and not interested accounts
        viewed_accounts = set()
        not_interested_accounts = set()
        
        # Read posts_viewed.json and extract viewed accounts
        if os.path.exists(posts_viewed_path):
            with open(posts_viewed_path, 'r') as file:
                import json
                data = json.load(file)
                for entry in data.get('impressions_history_posts_seen', []):
                    author = entry.get('string_map_data', {}).get('Author', {}).get('value')
                    if author:
                        viewed_accounts.add(author)
        else:
            print("Warning: posts_viewed.json not found. Continuing with available data.")
        
        # Read posts_you're_not_interested_in.json and extract not interested accounts
        if os.path.exists(posts_not_interested_path):
            with open(posts_not_interested_path, 'r') as file:
                import json
                data = json.load(file)
                for entry in data.get('impressions_history_posts_not_interested', []):
                    for item in entry.get('string_list_data', []):
                        href = item.get('href')
                        if href:
                            not_interested_accounts.add(href.split('/')[-1])  # Assuming the account name is the last part of the href
        else:
            print("Warning: posts_you're_not_interested_in.json not found. Continuing with available data.")
        
        # Find accounts that were viewed but not liked
        unliked_accounts = viewed_accounts - not_interested_accounts
        
        # Write the result to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in unliked_accounts:
                writer.writerow([account])
    
    except Exception as e:
        print(f"Error: {e}")
        # Create an empty CSV file with only the column headers if an error occurs
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])

# Call the function to execute the script
find_unliked_accounts(root_dir)