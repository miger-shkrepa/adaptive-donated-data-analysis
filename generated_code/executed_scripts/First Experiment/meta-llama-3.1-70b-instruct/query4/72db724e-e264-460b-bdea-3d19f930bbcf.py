import os
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a set to store unique company names
        companies = set()

        # Iterate over the subdirectories in the root directory
        for subdir in os.listdir(root_dir):
            subdir_path = os.path.join(root_dir, subdir)

            # Check if the subdirectory is a directory
            if os.path.isdir(subdir_path):
                # Check if the subdirectory is 'your_instagram_activity' or 'information_about_you' or 'personal_information'
                if subdir in ['your_instagram_activity', 'information_about_you', 'personal_information']:
                    # Iterate over the files in the subdirectory
                    for filename in os.listdir(subdir_path):
                        file_path = os.path.join(subdir_path, filename)

                        # Check if the file is a JSON file
                        if filename.endswith('.json'):
                            # Open the JSON file and read its contents
                            with open(file_path, 'r') as file:
                                # Since we don't have the actual JSON data, we'll assume it's a string
                                # In a real scenario, you'd use the json module to parse the JSON data
                                json_data = file.read()

                                # Check if the JSON data contains any company names
                                # For this example, we'll assume the company name is in the 'title' field
                                if 'title' in json_data:
                                    # Extract the company name from the JSON data
                                    company_name = json_data.split('"title":')[1].split(',')[0].strip().strip('"')

                                    # Add the company name to the set
                                    companies.add(company_name)

        # Return the set of company names
        return companies

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_companies_to_csv(companies):
    try:
        # Open the CSV file for writing
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            # Create a CSV writer
            writer = csv.writer(csvfile)

            # Write the header
            writer.writerow(['Company Name'])

            # Write each company name to the CSV file
            for company in companies:
                writer.writerow([company])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        companies = get_companies_with_access(root_dir)
        write_companies_to_csv(companies)

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()