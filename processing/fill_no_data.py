import pandas as pd
import os

# Map of queries to query folder names
queries = [
    "What topics does Instagram determine to be of interest for a user?",
    "How often does a user see advertisements and about which topics (from which companies)?",
    "How often do people see posts(daily and weekly)?",
    "Which companies have access to your Instagram activity or information?",
    "Which devices has the user logged in from and when?",
    "What Instagram account changes (e.g., name, phone, email) has the user made over time?",
    "Whose stories does the user tend to engage with most often?",
    "Which accounts has the user interacted with most often through post likes, story likes and comments(Top 20)?",
    "Which profiles does the user follow that do not follow him back?",
    "How often does the user view content (including both posts and videos) and from which accounts?",
    "Which accounts has the user viewed posts from but not liked them?",
    "How many messages does the user send per week?"
]

# Map question to queryX
question_to_query = {q: f"query{i+1}" for i, q in enumerate(queries)}

# Load the log file
df = pd.read_csv("../results/Final Experiment Prompt/result_evaluation_log.csv")

# Ensure 'No Data' column exists (if not, create empty one)
if 'No Data' not in df.columns:
    df['No Data'] = None

# Directory containing ground truth folders
ground_truth_base = "../ground_truths"

# Go through each row and update 'No Data' regardless of current value
for idx, row in df.iterrows():
    dataset_name = row['Dataset Name']
    question = row['Question']
    query_folder = question_to_query.get(question)

    if not query_folder:
        print(f"⚠️ Could not find query folder for question: {question}")
        continue

    query_path = os.path.join(ground_truth_base, query_folder)

    # Check for both possible file types
    expected_file = f"{dataset_name}_ground_truth.csv"
    nodata_file = f"NODATA_{dataset_name}_ground_truth.csv"

    expected_path = os.path.join(query_path, expected_file)
    nodata_path = os.path.join(query_path, nodata_file)

    if os.path.exists(expected_path):
        df.at[idx, 'No Data'] = False
    elif os.path.exists(nodata_path):
        df.at[idx, 'No Data'] = True
    else:
        print(f"⚠️ No matching ground truth file found for dataset: {dataset_name} in {query_path}")
        df.at[idx, 'No Data'] = "Unknown"

int_columns = ["Correct Rows","Extra Rows","Missing Rows","Number of Retries"]

for col in int_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

# Save the updated file
df.to_csv("../results/Final Experiment Prompt/processed_result_evaluation_log.csv", index=False)