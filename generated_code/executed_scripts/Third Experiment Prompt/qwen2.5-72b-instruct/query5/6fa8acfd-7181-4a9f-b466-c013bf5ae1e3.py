import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the path to the hypothetical login activity JSON file
login_activity_path = os.path.join(root_dir, "login_activity", "login_activity.json")

# Function to parse the login activity JSON file and extract device IDs and login times
def parse_login_activity(file_path):
    try:
        if not os.path.exists(file_path):
            print("Warning: The login activity file does not exist. Returning an empty list.")
            return []
        
        with open(file_path, 'r') as file:
            data = json.load(file)
            
            # Assuming the JSON structure is a list of dictionaries with 'device_id' and 'login_time' keys
            login_data = data.get('login_activity', [])
            
            # Extract device IDs and login times
            results = []
            for entry in login_data:
                device_id = entry.get('device_id')
                login_time = entry.get('login_time')
                
                if device_id and login_time:
                    try:
                        # Convert login_time to the required format
                        login_time_formatted = datetime.fromtimestamp(login_time).strftime('%Y-%m-%d %H:%M:%S')
                        results.append((device_id, login_time_formatted))
                    except ValueError:
                        raise ValueError("Error: Invalid timestamp in login_time.")
            
            return results
    except json.JSONDecodeError:
        raise ValueError("Error: Invalid JSON format in the login activity file.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

# Function to write the results to a CSV file
def write_to_csv(results, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
            
            if results:
                writer.writerows(results)
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

# Main function to execute the script
def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        results = parse_login_activity(login_activity_path)
        output_path = 'query_responses/results.csv'
        write_to_csv(results, output_path)
        
        print(f"CSV file has been saved to {output_path}")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()