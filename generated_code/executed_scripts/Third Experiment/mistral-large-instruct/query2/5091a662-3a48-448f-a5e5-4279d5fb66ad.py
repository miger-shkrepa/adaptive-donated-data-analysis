import os
import csv

# Define the root directory
root_dir = "root_dir"

# Function to process the directory and extract relevant information
def process_directory(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    # Initialize a dictionary to store the results
    results = {}

    # Walk through the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".json"):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r') as file:
                        # Process the JSON file (assuming it contains relevant data)
                        # Here, we would parse the JSON and extract the necessary information
                        # For simplicity, let's assume we extract company names and ad views
                        # Example:
                        # data = json.load(file)
                        # company_name = data.get('company_name', '')
                        # ad_views = data.get('ad_views', 0)

                        # Update the results dictionary
                        # if company_name:
                        #     results[company_name] = results.get(company_name, 0) + ad_views

                        # Placeholder for actual JSON processing
                        pass
                except Exception as e:
                    raise ValueError(f"Error: Failed to process file {file_path}. {str(e)}")

    # Prepare the CSV output
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for company, views in results.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': views})

# Call the function to process the directory
process_directory(root_dir)