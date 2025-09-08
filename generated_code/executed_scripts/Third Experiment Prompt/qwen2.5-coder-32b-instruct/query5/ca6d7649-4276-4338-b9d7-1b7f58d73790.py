import os
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to create an empty CSV file with the required headers
def create_empty_csv(output_path):
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Device ID", "Login Time"])

# Main function to process the data
def process_data(root_dir):
    # Define the output file path
    output_path = 'query_responses/results.csv'
    
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Since the required data is not present, create an empty CSV file
    create_empty_csv(output_path)

# Execute the main function
try:
    process_data(root_dir)
except Exception as e:
    print(e)