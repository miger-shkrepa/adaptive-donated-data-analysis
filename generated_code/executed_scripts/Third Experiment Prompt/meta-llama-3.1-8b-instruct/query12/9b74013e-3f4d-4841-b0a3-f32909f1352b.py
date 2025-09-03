import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")

def get_week(file_path):
    file_name = os.path.basename(file_path)
    week_number = int(file_name.split('_')[1].split('.')[0])
    week_date = datetime(2020, 1, 1) + datetime.timedelta(weeks=week_number - 1)
    return week_date.strftime('%Y-%W')

def process_message_file(file_path):
    message_data = load_json_file(file_path)
    week = get_week(file_path)
    messages_sent = len(message_data['messages'])
    return week, messages_sent

def process_conversation_folder(folder_path):
    conversation_data = {}
    for file_name in os.listdir(folder_path):
        if file_name.startswith('message_') and file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            try:
                week, messages_sent = process_message_file(file_path)
                conversation_data[week] = conversation_data.get(week, 0) + messages_sent
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
    return conversation_data

def process_inbox_folder(folder_path):
    conversation_data = {}
    for folder_name in os.listdir(folder_path):
        folder_path = os.path.join(folder_path, folder_name)
        if os.path.isdir(folder_path):
            try:
                conversation_data.update(process_conversation_folder(folder_path))
            except Exception as e:
                print(f"Error processing folder {folder_path}: {e}")
    return conversation_data

def process_root_directory(root_dir):
    inbox_folder_path = os.path.join(root_dir, 'your_activity_across_facebook', 'messages', 'inbox')
    if os.path.exists(inbox_folder_path):
        conversation_data = process_inbox_folder(inbox_folder_path)
        return conversation_data
    else:
        return {}

def write_csv_file(data, output_file_path):
    with open(output_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Week', 'Messages Sent'])
        for week, messages_sent in data.items():
            writer.writerow([week, messages_sent])

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        conversation_data = process_root_directory(root_dir)
        write_csv_file(conversation_data, 'query_responses/results.csv')
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()