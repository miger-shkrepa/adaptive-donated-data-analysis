import os
import json
import csv

root_dir = "root_dir"

def find_viewed_not_liked_accounts(root):
    viewed_accounts = set()
    liked_accounts = set()
    
    try:
        if not os.path.exists(root):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        for dirpath, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if filename == "activity_log.json":
                    with open(os.path.join(dirpath, filename), 'r') as file:
                        data = json.load(file)
                        for entry in data.get("activity_log_entries", []):
                            if "Viewed Post" in entry.get("title", ""):
                                viewed_accounts.add(entry["string_map_data"]["Account"]["value"])
                            elif "Liked Post" in entry.get("title", ""):
                                liked_accounts.add(entry["string_map_data"]["Account"]["value"])
        
        viewed_not_liked_accounts = viewed_accounts - liked_accounts
        return viewed_not_liked_accounts
    
    except json.JSONDecodeError:
        raise ValueError("Error: JSON file is not properly formatted.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def write_to_csv(accounts, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

try:
    viewed_not_liked_accounts = find_viewed_not_liked_accounts(root_dir)
    write_to_csv(viewed_not_liked_accounts, 'query_responses/results.csv')
except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)
except Exception as e:
    print(e)