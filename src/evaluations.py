import os
import csv
import ast
import pandas as pd
from radon.complexity import cc_visit
from radon.metrics import mi_visit, h_visit, analyze
from collections import Counter

CURRENT_EXPERIMENT = "First Experiment"

def evaluate_accuracy_and_log(
    experiment_id,
    dataset_name,
    model_name,
    question,
    ground_truth_path,
    generated_path,
    error_count,
    code_exec_time,
    total_duration,
    log_path=f"results/{CURRENT_EXPERIMENT}/result_evaluation_log.csv"
):
    # Load CSVs
    df_true = pd.read_csv(ground_truth_path)
    try:
        df_gen = pd.read_csv(generated_path)
    except pd.errors.EmptyDataError:
        df_gen = pd.DataFrame(columns=df_true.columns)

    # Drop rows that exactly match the column names (accidental header duplication)
    df_true = df_true[
        ~df_true.apply(lambda row: all(str(row[col]).strip().lower() == col.strip().lower() for col in df_true.columns),
                       axis=1)
    ]
    df_gen = df_gen[
        ~df_gen.apply(lambda row: all(str(row[col]).strip().lower() == col.strip().lower() for col in df_gen.columns),
                      axis=1)
    ]

    # Automatically use all shared columns for matching
    shared_cols = df_true.columns.intersection(df_gen.columns).tolist()

    # Normalize each shared column
    for col in shared_cols:
        df_true[col] = df_true[col].astype(str).str.strip().str.lower()
        df_gen[col] = df_gen[col].astype(str).str.strip().str.lower()

    no_data = False

    # If no data at all
    if df_true.empty and df_gen.empty:
        precision = recall = f1 = 1
        true_positives = false_positives = false_negatives = 0
        no_data = True
    else:
        # Generate row identity strings from shared columns
        true_keys = df_true[shared_cols].astype(str).agg('|'.join, axis=1)
        gen_keys = df_gen[shared_cols].astype(str).agg('|'.join, axis=1)

        # Count occurrences
        truth_counter = Counter(true_keys)
        gen_counter = Counter(gen_keys)

        # Metric counts
        true_positives = sum(min(truth_counter[k], gen_counter.get(k, 0)) for k in truth_counter)
        false_negatives = sum(max(truth_counter[k] - gen_counter.get(k, 0), 0) for k in truth_counter)
        false_positives = sum(max(gen_counter[k] - truth_counter.get(k, 0), 0) for k in gen_counter)

        # Metrics
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    # Build result row
    result = {
        "Experiment ID": experiment_id,
        "Dataset Name": dataset_name,
        "Model": model_name,
        "Question": question,
        "No Data": no_data,
        "Precision": precision if precision is None else round(precision, 4),
        "Recall": recall if recall is None else round(recall, 4),
        "F1": f1 if f1 is None else round(f1, 4),
        "Correct Rows": true_positives,
        "Extra Rows": false_positives,
        "Missing Rows": false_negatives,
        "Number of Retries": error_count,
        "Successful Code Exec. Duration": code_exec_time,
        "Total Duration": total_duration
    }

    # Save log
    df_result = pd.DataFrame([result])
    if not os.path.exists(log_path):
        df_result.to_csv(log_path, index=False)
    else:
        df_result.to_csv(log_path, mode='a', header=False, index=False)

    return result

def log_unsuccesful_trial(
        experiment_id,
        dataset_name,
        model_name,
        question,
        error_count,
        total_duration,
        log_path = f"results/{CURRENT_EXPERIMENT}/result_evaluation_log.csv"):
    # Assemble result row
    result = {
        "Experiment ID": experiment_id,
        "Dataset Name": dataset_name,
        "Model": model_name,
        "Question": question,
        "No Data": None,
        "Precision": None,
        "Recall": None,
        "F1": None,
        "Correct Rows": None,
        "Extra Rows": None,
        "Missing Rows": None,
        "Number of Retries": error_count,
        "Successful Code Exec. Duration": None,
        "Total Duration": total_duration
    }

    # Log it
    df_result = pd.DataFrame([result])
    if not os.path.exists(log_path):
        df_result.to_csv(log_path, index=False)
    else:
        df_result.to_csv(log_path, mode='a', header=False, index=False)


# Wrap top-level statements into a fake function for complexity analysis.
def wrap_top_level_in_function(code: str, func_name="__temp_wrapper__") -> str:
    try:
        tree = ast.parse(code)
        if any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) for node in tree.body):
            return code  # already contains functions/classes

        # Wrap top-level statements in a function
        func_def = ast.FunctionDef(
            name=func_name,
            args=ast.arguments(posonlyargs=[], args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None,
                               defaults=[]),
            body=tree.body,
            decorator_list=[],
            returns=None
        )
        tree.body = [func_def]
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)
    except Exception:
        return code


def evaluate_generated_code_and_log(
    experiment_id: str,
    model_name: str,
    question: str,
    generated_code_path: str,
    log_path: str = f"results/{CURRENT_EXPERIMENT}/code_evaluation_log.csv") -> dict:
    with open(generated_code_path, "r", encoding="utf-8") as script_file:
        raw_code = script_file.read()

    result = {
        "Experiment ID": experiment_id,
        "Model": model_name,
        "Question": question,
        "syntax_ok": False,
        "max_cyclomatic_complexity": None,
        "total_cyclomatic_complexity": None,
        "maintainability_index": None
    }

    try:
        compile(raw_code, '<string>', 'exec')
        result["syntax_ok"] = True
    except SyntaxError:
        return result

    try:
        fake_wrapped_code = wrap_top_level_in_function(raw_code)
        complexities = [
            {"name": cc.name, "complexity": cc.complexity, "lineno": cc.lineno}
            for cc in cc_visit(fake_wrapped_code)
        ]
        if complexities:
            result["max_cyclomatic_complexity"] = max(c["complexity"] for c in complexities)
            result["total_cyclomatic_complexity"] = sum(c["complexity"] for c in complexities)
    except Exception:
        pass

    try:
        result["maintainability_index"] = mi_visit(raw_code, False)
    except Exception:
        pass

    try:
        raw_metrics = analyze(raw_code)
        for key, value in raw_metrics._asdict().items():
            result[f"raw_{key}"] = value
    except Exception:
        pass

    try:
        halstead_metrics = h_visit(raw_code)
        for key, value in halstead_metrics.total._asdict().items():
            result[f"halstead_{key}"] = value
    except Exception:
        pass

    # Log it
    with open(log_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=result.keys())

        # If the file is empty, write headers
        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(result)
