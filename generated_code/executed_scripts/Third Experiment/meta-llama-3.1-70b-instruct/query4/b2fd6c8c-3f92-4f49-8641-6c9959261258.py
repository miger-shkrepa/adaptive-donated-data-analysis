import os
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Iterate over the files in the root directory
        for filename in os.listdir(root_dir):
            filepath = os.path.join(root_dir, filename)
            # Check if the file is a JSON file
            if os.path.isfile(filepath) and filename.endswith(".json"):
                # Open the JSON file and read its contents
                with open(filepath, 'r') as file:
                    # Check if the file has the required structure
                    if filename == "relationships_follow_requests_received.json" or \
                       filename == "relationships_hide_stories_from.json" or \
                       filename == "relationships_dismissed_suggested_users.json" or \
                       filename == "relationships_restricted_users.json":
                        # Extract the company names from the JSON file
                        with open(filepath, 'r') as file:
                            lines = file.readlines()
                            for line in lines:
                                if "value" in line:
                                    company = line.split('"value":')[1].split(',')[0].strip().replace('"', '')
                                    companies.add(company)
    except Exception as e:
        raise ValueError("Error: " + str(e))
    
    return companies

def save_to_csv(companies):
    try:
        # Create the results directory if it does not exist
        results_dir = 'query_responses'
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        # Save the companies to a CSV file
        with open(os.path.join(results_dir, 'results.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
            for company in companies:
                writer.writerow([company])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        companies = get_companies_with_access(root_dir)
        save_to_csv(companies)
    except Exception as e:
        print("Error: " + str(e))
        # Save an empty CSV file if an error occurs
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])

if __name__ == "__main__":
    main()