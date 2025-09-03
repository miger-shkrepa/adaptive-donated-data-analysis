import os
import json
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output file path
output_file_path = "query_responses/results.csv"

# Function to get all message files in the inbox directory
def get_message_files(root_dir):
    message_files = []
    inbox_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")
    
    if not os.path.exists(inbox_dir):
        return message_files
    
    for conversation_dir in os.listdir(inbox_dir):
        conversation_path = os.path.join(inbox_dir, conversation_dir)
        if os.path.isdir(conversation_path):
            for message_file in os.listdir(conversation_path):
                if message_file.startswith("message_") and message_file.endswith(".json"):
                    message_files.append(os.path.join(conversation_path, message_file))
    
    return sorted(message_files)

# Function to parse messages and count per week
def count_messages_per_week(message_files):
    week_message_count = {}
    
    for message_file in message_files:
        try:
            with open(message_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                messages = data.get("messages", [])
                
                for message in messages:
                    timestamp_ms = message.get("timestamp_ms")
                    if timestamp_ms:
                        timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
                        week = timestamp.strftime('%Y-%W')
                        if week in week_message_count:
                            week_message_count[week] += 1
                        else:
                            week_message_count[week] = 1
        except (FileNotFoundError, ValueError) as e:
            print(f"Error processing file {message_file}: {e}")
    
    return week_message_count

# Function to write the results to a CSV file
def write_results_to_csv(week_message_count, output_file_path):
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write("Week,Messages Sent\n")
            for week, count in sorted(week_message_count.items()):
                file.write(f"Week {week},{count}\n")
    except IOError as e:
        raise IOError(f"IOError: Failed to write to {output_file_path}. {e}")

# Main function to execute the script
def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        message_files = get_message_files(root_dir)
        if not message_files:
            write_results_to_csv({}, output_file_path)
            return
        
        week_message_count = count_messages_per_week(message_files)
        write_results_to_csv(week_message_count, output_file_path)
    
    except Exception as e:
        print(f"Error: {e}")

# Execute the main function
if __name__ == "__main__":
    main()