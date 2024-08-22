import os
from concurrent.futures import ProcessPoolExecutor
from utils.file_clean_util import extract_key_information
from utils.save_file import save_to_jsonl


def create_temp_dict(
    conversations_list: list[list[dict]],
    langdetect_list: list[str],
    source_list: list[str],
) -> list[dict]:
    temp_list = []

    for conversations, langdetect, source in zip(
        conversations_list, langdetect_list, source_list
    ):
        is_valid = True
        question = conversations[0]["value"]
        answer = conversations[1]["value"]
        all_text = question + answer

        # 文本长度检查
        if len(all_text) > 5000 or len(all_text) < 100:
            is_valid = False

        # 语言检查
        if langdetect == "ZH":
            pass
        elif langdetect == "en":  # 英文
            import random

            if random.random() > 1 / 2:  # 一半几率保留
                is_valid = False
        else:  # 其他语言
            is_valid = False

        if is_valid:
            temp_dict = {
                "conversations": conversations,
                "langdetect": langdetect,
                "source": source,
            }
            temp_list.append(temp_dict)

    return temp_list


def process_base(source_file_path: str, target_file_path: str) -> None:
    try:
        keys = ["conversations", "langdetect", "source"]

        dict_temp = extract_key_information(source_file_path, keys)

        if dict_temp is None:
            print(
                f"Warning: extract_key_information returned None for {source_file_path}"
            )
            return

        # 确保 dict_temp 中的所有字段都存在且为列表
        if not isinstance(dict_temp, dict):
            print(
                f"Warning: Unexpected return type {type(dict_temp)} from extract_key_information for {source_file_path}"
            )
            return

        for key in keys:
            if key not in dict_temp:
                print(f"Warning: Missing key '{key}' in data from {source_file_path}")
                return
            if not isinstance(dict_temp[key], list):
                print(
                    f"Warning: Key '{key}' is not a list in data from {source_file_path}"
                )
                return

        data_list = create_temp_dict(
            dict_temp["conversations"],
            dict_temp["langdetect"],
            dict_temp["source"],
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
        futures = [executor.submit(process_base, *pair) for pair in file_pairs]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Error in parallel processing: {e}")


if __name__ == "__main__":
    source_dir = "/data/nfs/data/Magpie-Qwen2-Pro-200K-Chinese-jsonl/data"
    target_dir = "/data/nfs/data/Magpie-Qwen2-Pro-200K-Chinese-jsonl/data_filter"
    process_files_in_parallel(source_dir, target_dir)
