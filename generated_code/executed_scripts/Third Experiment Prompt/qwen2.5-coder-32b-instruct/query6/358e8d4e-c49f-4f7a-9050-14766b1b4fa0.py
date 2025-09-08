import os
import csv
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

# Function to check if the root directory exists
def check_root_directory(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Function to generate the CSV file with only column headers
def generate_csv_with_headers():
    headers = ["Changed", "New Value", "Change Date"]
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

# Main function to execute the script
def main():
    try:
        # Check if the root directory exists
        check_root_directory(root_dir)
        
        # Generate CSV with only headers since required files are missing
        generate_csv_with_headers()
        
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Error: {str(e)}")

# Execute the main function
if __name__ == "__main__":
    main()