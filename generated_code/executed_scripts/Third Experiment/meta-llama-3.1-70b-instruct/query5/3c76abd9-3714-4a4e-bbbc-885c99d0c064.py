import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_device_ids_and_login_times(root_dir):
    device_ids = []
    login_times = []
    
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        for filename in os.listdir(root_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(root_dir, filename)
                try:
                    with open(file_path, 'r') as file:
                        # Since the exact structure of the JSON files is not provided, 
                        # we assume that the 'device_id' and 'date_time_original' are 
                        # directly accessible from the JSON data.
                        # In a real-world scenario, you would need to parse the JSON 
                        # data and access the required fields accordingly.
                        json_data = eval(file.read())
                        for item in json_data:
                            if 'media_metadata' in item and 'photo_metadata' in item['media_metadata']:
                                if 'exif_data' in item['media_metadata']['photo_metadata']:
                                    for exif_data in item['media_metadata']['photo_metadata']['exif_data']:
                                        if 'device_id' in exif_data and 'date_time_original' in exif_data:
                                            device_ids.append(exif_data['device_id'])
                                            login_times.append(exif_data['date_time_original'])
                                if 'video_metadata' in item['media_metadata']:
                                    if 'exif_data' in item['media_metadata']['video_metadata']:
                                        for exif_data in item['media_metadata']['video_metadata']['exif_data']:
                                            if 'device_id' in exif_data and 'date_time_original' in exif_data:
                                                device_ids.append(exif_data['device_id'])
                                                login_times.append(exif_data['date_time_original'])
                except Exception as e:
                    raise ValueError("ValueError: Failed to parse JSON file - " + str(e))
    except Exception as e:
        raise Exception("Error: " + str(e))
    
    return device_ids, login_times

def save_to_csv(device_ids, login_times):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Device ID', 'Login Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for device_id, login_time in zip(device_ids, login_times):
                try:
                    # Convert login_time to 'YYYY-MM-DD HH:MM:SS' format
                    dt = datetime.strptime(login_time, '%Y:%m:%d %H:%M:%S')
                    login_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    # If login_time is not in the correct format, skip this entry
                    continue
                writer.writerow({'Device ID': device_id, 'Login Time': login_time})
    except Exception as e:
        raise Exception("Error: Failed to save data to CSV file - " + str(e))

def main():
    try:
        device_ids, login_times = get_device_ids_and_login_times(root_dir)
        save_to_csv(device_ids, login_times)
    except Exception as e:
        print("Error: " + str(e))
        # If an error occurs, save a CSV file with only the column headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Device ID', 'Login Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()