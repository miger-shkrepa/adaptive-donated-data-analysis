import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def count_ads_viewed(data):
    company_count = {}
    for entry in data.get("impressions_history_ads_seen", []):
        author = entry.get("string_map_data", {}).get("Author", {}).get("value")
        if author:
            if author in company_count:
                company_count[author] += 1
            else:
                company_count[author] = 1
    return company_count

def save_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, count in data.items():
                writer.writerow([company, count])
    except Exception as e:
        raise IOError(f"Error: Unable to write to CSV file. {str(e)}")

def main():
    try:
        file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
        data = load_json(file_path)
        company_count = count_ads_viewed(data)

        output_path = "query_responses/results.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        save_to_csv(company_count, output_path)

    except FileNotFoundError as fnf_error:
        print(fnf_error)
        # Create an empty CSV file with headers if the required file is missing
        output_path = "query_responses/results.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        save_to_csv({}, output_path)
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()