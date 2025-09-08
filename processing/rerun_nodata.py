import os
import re
import shutil
import pandas as pd
from pathlib import Path
from src.helper import run_python_script, demodify_root_dir
from src.evaluations import evaluate_accuracy_and_log

# Load processed result log
input_csv = 'results/Final Experiment Prompt/processed_result_evaluation_log.csv'
df = pd.read_csv(input_csv)

# Filter entries with No Data == True
no_data_df = df[df['No Data'] == True].copy()

# Output file for updated evaluations
output_csv = 'results/Final Experiment Prompt/nodata_results.csv'

# Dataset to rerun all evaluations on
override_dataset = 'instagram-miger_shkrepa-2025-04-12-n2sjdWwP'

# Path constants
base_script_dir = Path('../generated_code/executed_scripts')
temp_script_path = Path('../generated_code/extracted_code.py')

# Query mapping
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

# Setup output log if not exists
if not os.path.exists(output_csv):
    pd.DataFrame(columns=df.columns).to_csv(output_csv, index=False)

# Iterate and rerun evaluations
for _, row in no_data_df.iterrows():
    experiment_id = row['Experiment ID']
    model = row['Model']
    question = row['Question']
    error_count = row['Number of Retries']
    total_duration = row['Total Duration']

    # If Precision is null, skip execution and copy row directly
    if pd.isna(row['Precision']):
        pd.DataFrame([row]).to_csv(output_csv, mode='a', header=False, index=False)
        print(f"⏭️ Skipped (null precision): {experiment_id}")
        continue

    try:
        query_index = queries.index(question) + 1
    except ValueError:
        print(f"❌ Unknown question text for Experiment ID: {experiment_id}")
        continue

    # Model directory correction
    lookup_model = model.replace("meta/llama-3.1-70b-instruct", "meta-llama-3.1-70b-instruct")

    query_dirs = [d for d in base_script_dir.glob(f"*/{lookup_model}/query{query_index}/{experiment_id}.py")]
    if not query_dirs:
        print(f"⚠️ Script not found for Experiment ID: {experiment_id}")
        continue

    script_path = query_dirs[0]

    try:
        shutil.copy(script_path, temp_script_path)
    except FileNotFoundError:
        print(f"❌ Failed to copy script for Experiment ID: {experiment_id}")
        continue

    with open(temp_script_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'(\broot_dir\s*=\s*)[\'\"].+[\'\"]', f"\\1'datasets/{override_dataset}'", content)
    with open(temp_script_path, "w", encoding="utf-8") as f:
        f.write(content)

    result = run_python_script(experiment_id, model, 1, str(temp_script_path))

    if not isinstance(result, dict) or result.get("error"):
        print(f"❌ Failed execution for {experiment_id}: {result.get('error') if isinstance(result, dict) else 'Invalid return'}")
        fail_row = row.copy()
        fail_row['Dataset Name'] = override_dataset
        fail_row['Precision'] = None
        fail_row['Recall'] = None
        fail_row['F1'] = None
        fail_row['Correct Rows'] = 0
        fail_row['Extra Rows'] = 0
        fail_row['Missing Rows'] = 0
        fail_row['Number of Retries'] = 1
        fail_row['Successful Code Exec. Duration'] = 0
        fail_row['Total Duration'] = 0
        pd.DataFrame([fail_row]).to_csv(output_csv, mode='a', header=False, index=False)
        open(temp_script_path, 'w').close()
        continue

    with open(temp_script_path, "r", encoding="utf-8") as f:
        script_content = f.read()
    with open(temp_script_path, "w", encoding="utf-8") as f:
        f.write(demodify_root_dir(script_content))

    ground_truth_path = Path("../ground_truths") / f"query{query_index}" / f"{override_dataset}_ground_truth.csv"
    generated_path = Path("../query_responses/results.csv")

    result_row = evaluate_accuracy_and_log(
        experiment_id,
        override_dataset,
        model,
        question,
        ground_truth_path,
        generated_path,
        error_count=error_count,
        code_exec_time=result['code_exec_time'],
        total_duration=total_duration,
        log_path=output_csv
    )

    open(temp_script_path, 'w').close()
    print(f"✅ Re-evaluated and logged Experiment ID: {experiment_id}")
