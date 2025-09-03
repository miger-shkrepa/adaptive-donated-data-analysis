import os
import json
import csv
from collections import defaultdict
from datetime import datetime

datasets_root_dir = "../../datasets"
output_base_dir = "../../query12"
os.makedirs(output_base_dir, exist_ok=True)

def parse_week(timestamp_ms):
    try:
        dt = datetime.fromtimestamp(timestamp_ms / 1000.0)
        return f"Week {dt.strftime('%Y-%W')}"
    except Exception:
        return None

for dataset in os.listdir(datasets_root_dir):
    dataset_path = os.path.join(datasets_root_dir, dataset)
    inbox_path = os.path.join(dataset_path, 'your_instagram_activity', "messages", "inbox")
    output_csv_path = os.path.join(output_base_dir, f"{dataset}_ground_truth.csv")
    nodata_csv_path = os.path.join(output_base_dir, f"NODATA_{dataset}_ground_truth.csv")

    messages_per_week = defaultdict(int)
    found_data = False

    if os.path.isdir(inbox_path):
        for convo in os.listdir(inbox_path):
            convo_path = os.path.join(inbox_path, convo)
            if not os.path.isdir(convo_path):
                continue

            x = 1
            while True:
                message_file = os.path.join(convo_path, f"message_{x}.json")
                if not os.path.isfile(message_file):
                    break

                try:
                    with open(message_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        for message in data.get('messages', []):
                            if message.get('sender_name') and message.get('timestamp_ms'):
                                if message.get('is_sent', True):
                                    week_key = parse_week(message['timestamp_ms'])
                                    if week_key:
                                        messages_per_week[week_key] += 1
                                        found_data = True
                except Exception as e:
                    print(f"Failed to parse {message_file}: {e}")
                x += 1

    if found_data:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Week", "Messages Sent"])
            for week in sorted(messages_per_week):
                writer.writerow([week, messages_per_week[week]])
        print(f"✅ {dataset}: saved to {output_csv_path}")
    else:
        with open(nodata_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Week", "Messages Sent"])
        print(f"⚠️ {dataset}: no data found, created {nodata_csv_path}")

print(f"\n🎉 All datasets processed. Results in: {output_base_dir}")
