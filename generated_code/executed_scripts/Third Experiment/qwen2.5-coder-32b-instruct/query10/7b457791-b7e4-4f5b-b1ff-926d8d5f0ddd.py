import os
import csv
import json

root_dir = "root_dir"

def main():
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Check if the required subdirectories and files exist
        likes_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        saved_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
        
        if not os.path.exists(likes_path) and not os.path.exists(saved_path):
            raise FileNotFoundError("FileNotFoundError: Neither liked_posts.json nor saved_posts.json exists.")
        
        # Since the query asks for content views which are not available in the provided structure,
        # we will create a CSV file with only the column headers.
        output_path = "query_responses/results.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Account", "Post Views", "Video Views"])
    
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")

if __name__ == "__main__":
    main()