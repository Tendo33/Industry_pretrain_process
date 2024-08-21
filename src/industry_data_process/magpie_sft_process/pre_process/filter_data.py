import json
import os
from concurrent.futures import ProcessPoolExecutor
from utils.file_clean_util import extract_key_information
from utils.save_file import save_to_jsonl

def create_temp_dict(
    content_list: list[str],
    lang_score_list: list[float],
    special_char_ratio_list: list[float],
    char_rep_ratio_list: list[float],
    perplexity_list: list[float],
    task_category_list: list[str],
    other_task_category_list: list[str],
    difficulty_list: list[str],
    input_quality_list: list[float],
    llama_guard_2_list: list[float],
    language_list: list[str],
) -> list[dict]:
    temp_list = []

    for (
        content,
        lang_score,
        special_char_ratio,
        char_rep_ratio,
        perplexity,
        task_category,
        other_task_category,
        difficulty,
        input_quality,
        llama_guard_2,
        language,
    ) in zip(
        content_list,
        lang_score_list,
        special_char_ratio_list,
        char_rep_ratio_list,
        perplexity_list,
        task_category_list,
        other_task_category_list,
        difficulty_list,
        input_quality_list,
        llama_guard_2_list,
        language_list,
    ):
        length = len(content)
        if lang_score > 0.85 and perplexity < 1000:
            temp_dict = {
                "content": content,
                "length": length,
                "lang_score": lang_score,
                "special_char_ratio": special_char_ratio,
                "char_rep_ratio": char_rep_ratio,
                "perplexity": perplexity,
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
        "text",
        "lang_score",
        "special_char_ratio",
        "char_rep_ratio",
        "perplexity",
        "task_category",
        "other_task_category",
        "difficulty",
        "input_quality",
        "llama_guard_2",
        "language",
    ]
    dict_temp = extract_key_information(source_file_path, keys)

    conversations = dict_temp["conversations"]
    task_category = dict_temp["task_category"]
    other_task_category = dict_temp["other_task_category"]
    difficulty = dict_temp["difficulty"]
    input_quality = dict_temp["input_quality"]
    llama_guard_2 = dict_temp["llama_guard_2"]
    language = dict_temp["language"]

    # 将清理后的数据和提取的信息保存为JSONL文件
    data_list = create_temp_dict(
        conversations,
        task_category,
        other_task_category,
        difficulty,
        input_quality,
        llama_guard_2,
        language,
    )
    print(len(data_list))
    save_to_jsonl(data_list, target_file_path)

def process_files_in_parallel(source_directory: str, target_directory: str) -> None:
    files = [f for f in os.listdir(source_directory) if f.endswith(".jsonl")]
    file_pairs = [
        (os.path.join(source_directory, f), os.path.join(target_directory, f))
        for f in files
    ]

    with ProcessPoolExecutor(max_workers=256) as executor:
        executor.map(process_base, file_pairs)


if __name__ == "__main__":
    source_dir = "path/to/source_directory"
    target_dir = "path/to/target_directory"
    process_files_in_parallel(source_dir, target_dir)
