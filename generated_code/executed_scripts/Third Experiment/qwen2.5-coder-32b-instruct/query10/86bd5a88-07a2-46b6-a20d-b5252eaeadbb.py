import os
import csv

# Define the root directory
root_dir = "root_dir"

# Function to check if the directory exists
def check_directory_exists(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"FileNotFoundError: The root directory does not exist.")

# Function to create a CSV file with the required headers
def create_csv_with_headers(output_path):
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Account", "Post Views", "Video Views"])

# Main function to execute the script
def main():
    try:
        # Check if the root directory exists
        check_directory_exists(root_dir)
        
        # Define the output CSV file path
        output_csv_path = 'query_responses/results.csv'
        
        # Create the CSV file with headers
        create_csv_with_headers(output_csv_path)
        
        print(f"CSV file created at {output_csv_path} with headers only.")
        
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")

# Execute the main function
if __name__ == "__main__":
    main()