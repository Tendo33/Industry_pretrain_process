import json
import os
from concurrent.futures import ProcessPoolExecutor
from utils.file_clean_util import extract_key_information
from utils.save_file import save_to_jsonl

def create_temp_dict(
    conversations_list: list[dict],
    task_category_list: list[str],
    other_task_category_list: list[str],
    difficulty_list: list[str],
    input_quality_list: list[float],
    llama_guard_2_list: list[float],
    language_list: list[str],
) -> list[dict]:
    temp_list = []

    for (
        conversations,
        task_category,
        other_task_category,
        difficulty,
        input_quality,
        llama_guard_2,
        language,
    ) in zip(
        conversations_list,
        task_category_list,
        other_task_category_list,
        difficulty_list,
        input_quality_list,
        llama_guard_2_list,
        language_list,
    ):
        is_valid = True
        question = conversations[0]["value"]
        answer = conversations[1]["value"]
        all_text = question + answer
        if len(all_text) > 5000 or len(all_text) < 100:
            is_valid = False

        if input_quality == "poor" or input_quality == "very poor":
            is_valid = False
        if llama_guard_2 != "safe":
            is_valid = False
        if language != "ZH" and language != "EN":
            is_valid = False
        if repeat_count >= 2:
            is_valid = False

        if (
            "Coding" in task_category
            or "Coding" in other_task_category
            or "Math" in task_category
            or "Math" in other_task_category
        ):
            is_valid = False
        if is_valid:
            temp_dict = {
                "conversations": conversations,
                "task_category": task_category,
                "other_task_category": other_task_category,
                "difficulty": difficulty,
                "input_quality": input_quality,
                "llama_guard_2": llama_guard_2,
                "language": language,
            }
            temp_list.append(temp_dict)

    return temp_list

def process_base(source_file_path: str, target_file_path: str) -> None:
    try:
        keys = [
            "conversations",
            "task_category",
            "other_task_category",
            "difficulty",
            "input_quality",
            "llama_guard_2",
            "repeat_count",
            "language",
        ]
        dict_temp = extract_key_information(source_file_path, keys)
        data_list = create_temp_dict(
            dict_temp["conversations"],
            dict_temp["task_category"],
            dict_temp["other_task_category"],
            dict_temp["difficulty"],
            dict_temp["input_quality"],
            dict_temp["llama_guard_2"],
            dict_temp["language"],
        )
        print(f"Processing {source_file_path}, found {len(data_list)} items")
        save_to_jsonl(data_list, target_file_path)
    except Exception as e:
        print(f"Error processing {source_file_path}: {e}")


def process_files_in_parallel(source_directory: str, target_directory: str) -> None:
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    files = [f for f in os.listdir(source_directory) if f.endswith(".jsonl")]
    file_pairs = [
        (os.path.join(source_directory, f), os.path.join(target_directory, f))
        for f in files
    ]
    print(f"File pairs to process: {file_pairs}")

    max_workers = min(32, os.cpu_count() or 1)
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # results = executor.map(process_base, file_pairs)
        futures = [executor.submit(process_base, *pair) for pair in file_pairs]
        for future in futures:
            try:
                future.result()  # 捕获并处理可能的异常
            except Exception as e:
                print(f"Error in parallel processing: {e}")


if __name__ == "__main__":
    source_dir = "/data/nfs/data/Magpie-Qwen2-Pro-200K-Chinese-jsonl/data"
    target_dir = "/data/nfs/data/Magpie-Qwen2-Pro-200K-Chinese-jsonl/data_filter"
    process_files_in_parallel(source_dir, target_dir)
