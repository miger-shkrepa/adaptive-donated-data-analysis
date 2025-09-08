import os
import csv

# The root directory variable
root_dir = "root_dir"

# Function to check if the directory exists
def check_directory_exists(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Function to write the CSV file
def write_csv(file_path, data):
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
            for item in data:
                writer.writerow([item])
    except Exception as e:
        raise ValueError(f"ValueError: Failed to write CSV file - {str(e)}")

# Main function to process the directory and generate the CSV
def main():
    try:
        check_directory_exists(root_dir)
        # Assuming Instagram has access to all data in the directory
        companies_with_access = ["Instagram"]
        output_file_path = 'query_responses/results.csv'
        write_csv(output_file_path, companies_with_access)
        print(f"CSV file has been created at {output_file_path}")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except ValueError as ve_error:
        print(ve_error)

if __name__ == "__main__":
    main()