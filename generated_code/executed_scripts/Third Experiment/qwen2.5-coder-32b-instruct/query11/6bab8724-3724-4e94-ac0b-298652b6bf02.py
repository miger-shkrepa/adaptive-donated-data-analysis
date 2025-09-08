import os
import csv

# The root directory variable
root_dir = "root_dir"

# Function to find the path of the posts_viewed.json file
def find_posts_viewed_file(root_dir):
    ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
    posts_viewed_file = os.path.join(ads_and_topics_dir, "posts_viewed.json")
    if not os.path.exists(posts_viewed_file):
        raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
    return posts_viewed_file

# Function to read the posts_viewed.json file and extract viewed accounts
def extract_viewed_accounts(posts_viewed_file):
    try:
        with open(posts_viewed_file, 'r') as file:
            import json
            data = json.load(file)
            viewed_accounts = set()
            for entry in data.get("impressions_history_posts_seen", []):
                author = entry.get("string_map_data", {}).get("Author", {}).get("value")
                if author:
                    viewed_accounts.add(author)
            return viewed_accounts
    except Exception as e:
        raise ValueError(f"ValueError: Error reading posts_viewed.json file - {str(e)}")

# Main function to execute the script
def main():
    try:
        # Find the posts_viewed.json file
        posts_viewed_file = find_posts_viewed_file(root_dir)
        
        # Extract viewed accounts
        viewed_accounts = extract_viewed_accounts(posts_viewed_file)
        
        # Prepare the output CSV file path
        output_csv_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        
        # Write the results to a CSV file
        with open(output_csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in viewed_accounts:
                writer.writerow([account])
        
        print(f"Results have been saved to {output_csv_path}")
    
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        # Create an empty CSV file with only the column headers
        output_csv_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        with open(output_csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
        print(f"Empty results CSV with headers has been saved to {output_csv_path}")
    
    except ValueError as ve_error:
        print(ve_error)
        # Create an empty CSV file with only the column headers
        output_csv_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        with open(output_csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
        print(f"Empty results CSV with headers has been saved to {output_csv_path}")

# Execute the main function
if __name__ == "__main__":
    main()