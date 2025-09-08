import csv
import os

def get_topics_of_interest(root_dir):
    try:
        topics_of_interest = []
        for filename in os.listdir(root_dir):
            if filename.endswith(".json"):
                with open(os.path.join(root_dir, filename), 'r') as file:
                    data = eval(file.read())
                    if 'information_about_you' in data and 'locations_of_interest.json' in data['information_about_you']:
                        locations_of_interest = data['information_about_you']['locations_of_interest.json']
                        if 'label_values' in locations_of_interest and locations_of_interest['label_values']:
                            for label_value in locations_of_interest['label_values']:
                                if 'label' in label_value and 'vec' in label_value:
                                    topics_of_interest.append(label_value['label'])
        return topics_of_interest
    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise ValueError("ValueError: An error occurred while processing the data.")

def write_to_csv(topics_of_interest):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Topics of Interest"])
        for topic in topics_of_interest:
            writer.writerow([topic])

root_dir = "root_dir"
topics_of_interest = get_topics_of_interest(root_dir)
write_to_csv(topics_of_interest)