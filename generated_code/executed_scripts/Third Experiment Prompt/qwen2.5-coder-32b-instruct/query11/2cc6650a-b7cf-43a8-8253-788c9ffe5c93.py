import os
import csv

# Define the root directory
root_dir = "root_dir"

# Function to read JSON files and extract authors
def read_json_file(file_path):
    authors = set()
    try:
        with open(file_path, 'r') as file:
            data = eval(file.read())
            if 'impressions_history_posts_seen' in data:
                for entry in data['impressions_history_posts_seen']:
                    if 'string_map_data' in entry and 'Author' in entry['string_map_data']:
                        authors.add(entry['string_map_data']['Author']['value'])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: Error reading the file {file_path}: {str(e)}")
    return authors

# Function to find accounts viewed but not liked
def find_accounts_viewed_but_not_liked(root_dir):
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    
    try:
        viewed_authors = read_json_file(posts_viewed_path)
    except FileNotFoundError:
        viewed_authors = set()
    
    try:
        liked_authors = read_json_file(liked_posts_path)
    except FileNotFoundError:
        liked_authors = set()
    
    # Find the difference
    accounts_viewed_but_not_liked = viewed_authors - liked_authors
    
    return accounts_viewed_but_not_liked

# Main function to execute the query and save the result to CSV
def main():
    try:
        accounts = find_accounts_viewed_but_not_liked(root_dir)
        
        # Save the result to CSV
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        # If any error occurs, create an empty CSV with only the header
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])

# Execute the main function
if __name__ == "__main__":
    main()