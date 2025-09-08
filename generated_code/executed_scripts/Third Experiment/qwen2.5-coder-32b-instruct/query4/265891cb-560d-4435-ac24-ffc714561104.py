import os
import csv

# The variable referring to the file input must be declared in a single line.
root_dir = "root_dir"

def check_directory_exists(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"FileNotFoundError: The root directory {directory} does not exist.")

def main():
    try:
        check_directory_exists(root_dir)
        
        # Since the necessary information about companies is not available,
        # we create a CSV file with only the column headers.
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Company Name'])
            
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")

if __name__ == "__main__":
    main()