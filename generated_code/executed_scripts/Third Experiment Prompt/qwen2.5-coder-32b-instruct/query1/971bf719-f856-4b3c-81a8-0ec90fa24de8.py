import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

def find_your_topics_file(root_dir):
    your_topics_path = os.path.join(root_dir, "preferences", "your_topics", "your_topics.json")
    if not os.path.exists(your_topics_path):
        raise FileNotFoundError(f"FileNotFoundError: The file {your_topics_path} does not exist.")
    return your_topics_path

def read_your_topics_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
            return eval(data)
    except Exception as e:
        raise ValueError(f"ValueError: Error reading the file {file_path}. {str(e)}")

def extract_topics_of_interest(data):
    topics_of_interest = []
    try:
        topics = data.get("topics_your_topics", [])
        for topic in topics:
            name = topic.get("string_map_data", {}).get("Name", {}).get("value", "")
            if name:
                topics_of_interest.append(name)
    except Exception as e:
        raise ValueError(f"ValueError: Error extracting topics of interest. {str(e)}")
    return topics_of_interest

def save_to_csv(topics_of_interest):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])
    except Exception as e:
        raise ValueError(f"ValueError: Error writing to CSV file. {str(e)}")

def main():
    try:
        your_topics_file_path = find_your_topics_file(root_dir)
        your_topics_data = read_your_topics_file(your_topics_file_path)
        topics_of_interest = extract_topics_of_interest(your_topics_data)
        save_to_csv(topics_of_interest)
    except FileNotFoundError as fnf_error:
        save_to_csv([])  # Save only the column headers if the file is not found
        print(fnf_error)
    except ValueError as ve_error:
        save_to_csv([])  # Save only the column headers if there is a value error
        print(ve_error)

if __name__ == "__main__":
    main()