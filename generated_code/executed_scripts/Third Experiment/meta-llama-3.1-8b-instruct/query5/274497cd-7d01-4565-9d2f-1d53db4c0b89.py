import csv
import os
import json

root_dir = "root_dir"

def get_login_data(root_dir):
    login_data = []
    login_activity_file = os.path.join(root_dir, "security_and_login_information", "login_and_account_creation", "login_activity.json")
    
    try:
        with open(login_activity_file, 'r') as f:
            login_activity_data = json.load(f)
            
            for item in login_activity_data["account_history_login_history"]:
                device_id = item["string_map_data"]["IP-Adresse"]["value"]
                login_time = item["string_map_data"]["Zeit"]["value"]
                login_data.append([device_id, login_time])
                
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The login activity file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The login activity file is not in JSON format.")
        
    return login_data

def save_to_csv(login_data):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Device ID', 'Login Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in login_data:
            writer.writerow({'Device ID': item[0], 'Login Time': item[1]})

def main():
    login_data = get_login_data(root_dir)
    save_to_csv(login_data)

if __name__ == "__main__":
    main()