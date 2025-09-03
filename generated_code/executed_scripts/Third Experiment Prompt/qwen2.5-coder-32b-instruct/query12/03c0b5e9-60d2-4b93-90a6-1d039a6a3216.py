import os
import json
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output file path
output_file_path = "query_responses/results.csv"

# Function to parse the timestamp from a message JSON file
def parse_timestamp_from_message(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Assuming the timestamp is stored in a key named 'timestamp'
            # Adjust the key name if the actual structure is different
            timestamp = data.get('timestamp')
            if timestamp is None:
                raise ValueError("ValueError: Timestamp not found in the message file.")
            return timestamp
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing the file {file_path}: {e}")

# Function to count messages per week
def count_messages_per_week(root_dir):
    week_count = {}
    
    # Traverse the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.startswith('message_') and filename.endswith('.json'):
                file_path = os.path.join(dirpath, filename)
                try:
                    timestamp = parse_timestamp_from_message(file_path)
                    dt = datetime.fromtimestamp(int(timestamp))
                    week = dt.strftime('%Y-%W')
                    if week in week_count:
                        week_count[week] += 1
                    else:
                        week_count[week] = 1
                except Exception as e:
                    print(f"Warning: {e}")
    
    return week_count

# Function to write the results to a CSV file
def write_results_to_csv(week_count, output_file_path):
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write("Week,Messages Sent\n")
            for week, count in sorted(week_count.items()):
                file.write(f"{week},{count}\n")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while writing to the file {output_file_path}: {e}")

# Main function to execute the script
def main():
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Count messages per week
        week_count = count_messages_per_week(root_dir)
        
        # Write the results to a CSV file
        write_results_to_csv(week_count, output_file_path)
        
        print(f"Results have been written to {output_file_path}")
    except Exception as e:
        print(e)
        # If there is an error, write only the column headers to the CSV file
        try:
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write("Week,Messages Sent\n")
        except Exception as e:
            print(f"Error: An unexpected error occurred while writing the column headers to the file {output_file_path}: {e}")

# Execute the main function
if __name__ == "__main__":
    main()