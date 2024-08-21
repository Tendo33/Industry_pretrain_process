import json
import os
from concurrent.futures import ProcessPoolExecutor
from utils.file_clean_util import extract_key_information
from utils.save_file import save_to_jsonl

def create_temp_dict(
    conversations_list: list[str],
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
    keys = [
        "conversations",
        "task_category",
        "other_task_category",
        "difficulty",
        "input_quality",
        "llama_guard_2",
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
    print(len(data_list))
    save_to_jsonl(data_list, target_file_path)


def process_files_in_parallel(source_directory: str, target_directory: str) -> None:
    files = [f for f in os.listdir(source_directory) if f.endswith(".jsonl")]
    file_pairs = [
        (os.path.join(source_directory, f), os.path.join(target_directory, f))
        for f in files
    ]
    print(file_pairs)
    max_workers = min(64, os.cpu_count() or 1)
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(process_base, (pair for pair in file_pairs))


if __name__ == "__main__":
    source_dir = "/data/nfs/data/Magpie-Qwen2-Pro-200K-Chinese-jsonl/data"
    target_dir = "/data/nfs/data/Magpie-Qwen2-Pro-200K-Chinese-jsonl/data_filter"
    process_files_in_parallel(source_dir, target_dir)
