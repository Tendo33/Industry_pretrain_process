import json
import os
from utils.save_file import save_to_jsonl

keywords = [
    "矿业", "石油", "天然气", "森林", "水资源", "煤炭", "可再生能源",
    "矿产", "开采", "地质", "水电", "风能", "太阳能", "农业",
    "渔业", "林业", "矿物", "资源开采", "环境保护"
]


def extract_info(file_path: str) -> list[dict]:
    with open(file_path, 'r', encoding='utf-8') as f:
        all_data_list = []
        for line in f:
            data = json.loads(line)
            # 提取词条信息和内容
            entry_info = {
                "title": "",
                "content": ""
            }
            # 找到词条和内容
            for paragraph in data["段落"]:
                content = paragraph["内容"]
                if paragraph["行号"] == 0 or content.startswith("【") and content.endswith("】"):
                    entry_info["title"] = content[1:-1]  # 去掉【】
                else:
                    entry_info["content"] += content + "\n"
            entry_info["content"] = entry_info["content"].strip()
            all_data_list.append(entry_info)
        return all_data_list


def main(file_path: str, out_path: str) -> None:
    all_data_list = extract_info(file_path)
    save_to_jsonl(all_data_list, out_path)


if __name__ == '__main__':
    file_path = r"/data/nfs/data/MNBVC/wiki_filter/20230197.jsonl"
    out_file = r"/data/nfs/data/MNBVC/wiki_filter/20230197_new.jsonl"
    # for file_name in os.listdir(root_dir):
    #     file_path = os.path.join(root_dir, file_name)
    #     out_path = file_name.split(".")[0] + "_new.jsonl"
    #     if file_path.endswith(".jsonl"):
    #         # print(file_path)
    main(file_path, out_file)
