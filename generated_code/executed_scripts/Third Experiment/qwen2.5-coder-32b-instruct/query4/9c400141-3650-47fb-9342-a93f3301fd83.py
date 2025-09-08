import os
import csv

# Define the root directory
root_dir = "root_dir"

# Function to check if the directory exists
def check_directory_exists(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"FileNotFoundError: The root directory does not exist.")

# Function to find companies with access (this is a placeholder as no such data is available)
def find_companies_with_access(root_dir):
    companies = []
    # Placeholder logic to simulate checking for company access data
    # In this case, we assume no such data is available
    return companies

# Main function to execute the script
def main():
    try:
        # Check if the root directory exists
        check_directory_exists(root_dir)
        
        # Find companies with access
        companies = find_companies_with_access(root_dir)
        
        # Define the output file path
        output_file_path = 'query_responses/results.csv'
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        
        # Write the results to a CSV file
        with open(output_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])  # Write the header
            for company in companies:
                writer.writerow([company])  # Write each company name
        
        print(f"Results have been saved to {output_file_path}")
    
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")

# Execute the main function
if __name__ == "__main__":
    main()