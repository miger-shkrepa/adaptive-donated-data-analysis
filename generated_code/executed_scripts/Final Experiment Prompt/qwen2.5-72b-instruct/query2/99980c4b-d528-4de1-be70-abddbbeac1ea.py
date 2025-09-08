import os
import json
import csv

root_dir = "root_dir"

def process_ads_data(root_dir):
    ads_data_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
    company_ads_count = {}

    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        if not os.path.exists(ads_data_path):
            print("Warning: The ads data file does not exist. Generating an empty CSV file.")
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Company Name', 'Number of Ads Viewed'])
            return

        with open(ads_data_path, 'r') as file:
            data = json.load(file)
            if 'impressions_history_ads_seen' not in data:
                raise ValueError("Error: The JSON data does not contain the expected structure.")

            for entry in data.get('impressions_history_ads_seen', []):
                string_map_data = entry.get('string_map_data', {})
                author = string_map_data.get('Author', {}).get('value')
                if author:
                    company_ads_count[author] = company_ads_count.get(author, 0) + 1

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Company Name', 'Number of Ads Viewed'])
            for company, count in company_ads_count.items():
                csvwriter.writerow([company, count])

    except FileNotFoundError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Company Name', 'Number of Ads Viewed'])
    except json.JSONDecodeError as e:
        print(f"Error: JSON decoding error - {e}")
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Company Name', 'Number of Ads Viewed'])
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Company Name', 'Number of Ads Viewed'])

# Call the function with the root directory
process_ads_data(root_dir)