import os
import glob
import json
import re

# 保存成 json 文件格式 [{},{},{}]


def save_to_json(content_list: list, file_path: str):
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(content_list, json_file, ensure_ascii=False, indent=4)


# 保存成 jsonl 文件格式 (一行一行) {},{},{}
def save_to_jsonl(content_list: list[dict], file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        for item in content_list:
            file.write(json.dumps(item, ensure_ascii=False) + "\n")


def json_to_jsonl(json_file, jsonl_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(
        jsonl_file,
        "w",
    ) as f:
        for item in data:
            json_str = json.dumps(item)
            f.write(json_str + "\n")


def merge_jsonl(file1: str, file2: str, output_file: str):
    with open(file1, "r", encoding="utf-8") as f1, open(
        file2, "r", encoding="utf-8"
    ) as f2, open(output_file, "w", encoding="utf-8") as output:
        pattern = r"[^\u4e00-\u9fa5，《》<>\"\']+"

        titles_set = set()  # 用于存储已经出现过的title

        # 逐行读取第一个文件的内容，并写入到输出文件中
        for line in f1:
            data = json.loads(line)  # 将每行数据解析为 JSON 对象
            title = data["title"]
            title_clean = re.sub(pattern, "", title)
            if title_clean not in titles_set:
                output.write(line)
                titles_set.add(title_clean)

        # 逐行读取第二个文件的内容，将不重复的内容写入到输出文件中
        for line in f2:
            data = json.loads(line)  # 将每行数据解析为 JSON 对象
            title = data["title"]
            title_clean = re.sub(pattern, "", title)
            if title_clean not in titles_set:
                output.write(line)
                titles_set.add(title_clean)
