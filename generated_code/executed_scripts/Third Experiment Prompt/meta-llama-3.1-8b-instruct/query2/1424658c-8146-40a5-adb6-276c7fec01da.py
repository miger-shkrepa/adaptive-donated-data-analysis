import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

# Define the function to extract the data from the JSON files
def extract_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            data = file.read()
            return data
    except FileNotFoundError:
        return None

# Define the function to parse the JSON data
def parse_json(data):
    try:
        import json
        return json.loads(data)
    except ValueError:
        return None

# Define the function to extract the company name and number of ads viewed
def extract_info(data):
    company_name = None
    num_ads_viewed = 0
    if data is not None:
        if 'ads_and_topics' in data and 'ads_and_topics' in data['ads_information']:
            for file in data['ads_information']['ads_and_topics']:
                if file['type'] == 'json':
                    json_data = parse_json(file['structure']['impressions_history_posts_seen'][0]['string_map_data']['Author']['value'])
                    if json_data is not None:
                        company_name = json_data
                        num_ads_viewed += 1
    return company_name, num_ads_viewed

# Define the function to write the results to a CSV file
def write_results(results):
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company Name', 'Number of Ads Viewed'])
        for result in results:
            writer.writerow(result)

# Walk through the directory and extract the data
for root, dirs, files in os.walk(root_dir):
    for file in files:
        file_path = os.path.join(root, file)
        data = extract_data(file_path)
        if data is not None:
            company_name, num_ads_viewed = extract_info(data)
            if company_name is not None:
                results.append([company_name, num_ads_viewed])

# Write the results to a CSV file
write_results(results)