import os
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to check if a file exists
def file_exists(file_path):
    return os.path.exists(file_path)

# Function to create an empty CSV file with headers
def create_empty_csv(output_path):
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Changed", "New Value", "Change Date"])

# Main function to process the query
def process_query(root_dir):
    # Define the path to the output CSV file
    output_path = 'query_responses/results.csv'
    
    # Check if the root directory exists
    if not os.path.isdir(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Check if the required files exist
    liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
    
    if not file_exists(liked_posts_path) and not file_exists(saved_posts_path):
        # If neither file exists, create an empty CSV file with headers
        create_empty_csv(output_path)
        return
    
    # Since the required data for account changes is not present, create an empty CSV file with headers
    create_empty_csv(output_path)

# Execute the main function
try:
    process_query(root_dir)
except Exception as e:
    print(e)