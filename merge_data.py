import os
import json


def merge_jsonl_files(root_dir):
    # 遍历根目录下的所有文件夹
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)

        if os.path.isdir(folder_path):
            jsonl_filename = f"{folder_name}.jsonl"
            jsonl_filepath = os.path.join(root_dir, jsonl_filename)

            with open(jsonl_filepath, 'w', encoding='utf-8') as jsonl_file:
                # 遍历文件夹中的所有 JSONL 文件
                for json_filename in os.listdir(folder_path):
                    json_filepath = os.path.join(folder_path, json_filename)

                    if json_filename.endswith('.json'):
                        with open(json_filepath, 'r', encoding='utf-8') as json_file:
                            for line in json_file:
                                jsonl_file.write(line)

            print(
                f"All JSONL files from {folder_path} have been merged into {jsonl_filepath}")


if __name__ == "__main__":
    root_directory = r"/data/nfs/data/IndustryCorpus/chinese"
    merge_jsonl_files(root_directory)
