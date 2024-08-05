import json
import os
from utils.save_file import save_to_jsonl


def extract_wiki_info(file_path: str) -> list[dict]:
    all_data_list = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:  # 检查是否为空行
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in line: {line}")
                print(e)
                continue
            entry_info = {"title": "", "content": ""}
            for paragraph in data.get("段落", []):  # 确保“段落”存在
                content = paragraph["内容"]
                if paragraph["行号"] == 0 or (
                    content.startswith("【") and content.endswith("】")
                ):
                    entry_info["title"] = content[1:-1]
                else:
                    entry_info["content"] += content + "\n"
            entry_info["content"] = entry_info["content"].strip()
            all_data_list.append(entry_info)
    return all_data_list


def clean_wiki_data(wiki_data: dict) -> dict:
    content = wiki_data["content"]
    content_list = content.split("\n")
    cleaned_content = []
    skip_next = False

    for i in range(len(content_list)):
        if skip_next:
            skip_next = False
            continue

        if content_list[i].startswith("=="):
            if i + 1 < len(content_list) and content_list[i + 1].startswith(
                "=="
            ):
                skip_next = True
                continue
            elif i == len(content_list) - 1 or "外部连结" in content_list[i]:
                break

            cleaned_content.append(f"{content_list[i].strip('=').strip()}:")
        elif (
            "外部连结" in content_list[i]
            or "参考文献" in content_list[i]
            or "#>Documentation at" in content_list[i]
        ):
            break
        else:
            cleaned_content.append(content_list[i].strip("*").strip())

    wiki_data["content"] = "\n".join(cleaned_content)
    return wiki_data


def main(file_path: str, out_path: str) -> None:
    all_data_list = extract_wiki_info(file_path)
    cleaned_data_list = [clean_wiki_data(data) for data in all_data_list]
    save_to_jsonl(cleaned_data_list, out_path)


if __name__ == "__main__":
    file_path = r"/workspace/share_data/data/MNBVC/wiki_filter/20230198.jsonl"
    out_file = (
        r"/workspace/share_data/data/MNBVC/wiki_filter/20230198_new.jsonl"
    )
    main(file_path, out_file)
    # 可以取消以下代码的注释以处理多个文件
    # root_dir = r"/data/nfs/data/MNBVC/wiki_filter/"
    # for file_name in os.listdir(root_dir):
    #     file_path = os.path.join(root_dir, file_name)
    #     out_path = file_name.split(".")[0] + "_new.jsonl"
    #     if file_path.endswith(".jsonl"):
    #         main(file_path, out_path)
