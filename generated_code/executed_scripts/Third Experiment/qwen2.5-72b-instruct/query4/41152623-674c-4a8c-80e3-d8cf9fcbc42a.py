import os
import json
import csv

root_dir = "root_dir"

def find_companies_with_access(root):
    companies = set()
    try:
        if not os.path.exists(root):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Check if the necessary directory exists
        activity_path = os.path.join(root, "your_instagram_activity")
        if not os.path.exists(activity_path):
            return companies  # Return an empty set if the directory is not found
        
        # Iterate through the 'your_instagram_activity' directory
        for category in ["comments", "content", "likes", "messages"]:
            category_path = os.path.join(activity_path, category)
            if not os.path.exists(category_path):
                continue  # Skip if the category directory does not exist
            
            for file_name in os.listdir(category_path):
                file_path = os.path.join(category_path, file_name)
                if os.path.isfile(file_path) and file_name.endswith('.json'):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        # Extract company names from the JSON structure
                        if "string_map_data" in data and "Company Name" in data["string_map_data"]:
                            company_name = data["string_map_data"]["Company Name"]["value"]
                            companies.add(company_name)
                        elif "string_list_data" in data and "Company Name" in data["string_list_data"]:
                            for item in data["string_list_data"]:
                                if "Company Name" in item:
                                    company_name = item["Company Name"]["value"]
                                    companies.add(company_name)
                        elif "participants" in data and "Company Name" in data["participants"]:
                            for participant in data["participants"]:
                                if "Company Name" in participant:
                                    company_name = participant["Company Name"]["value"]
                                    companies.add(company_name)
                        elif "messages" in data and "Company Name" in data["messages"]:
                            for message in data["messages"]:
                                if "Company Name" in message:
                                    company_name = message["Company Name"]["value"]
                                    companies.add(company_name)
        
        return companies
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def save_to_csv(companies):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
        for company in companies:
            writer.writerow([company])

try:
    companies_with_access = find_companies_with_access(root_dir)
    save_to_csv(companies_with_access)
except Exception as e:
    print(e)