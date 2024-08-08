import json
import os
import shutil


def extract_files(source_folder: str, destination_folder: str) -> None:
    # 确保目标文件夹存在
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 遍历源文件夹中的所有子文件夹
    for folder_name in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder_name)

        if os.path.isdir(folder_path):
            # 构造文件路径
            json_file = os.path.join(folder_path, f"{folder_name}_content_list.json")
            md_file = os.path.join(folder_path, f"{folder_name}.md")

            # 检查文件是否存在并复制
            if os.path.exists(json_file):
                shutil.copy(
                    json_file,
                    os.path.join(
                        destination_folder, f"{folder_name}_content_list.json"
                    ),
                )
                print(f"已复制: {json_file}")

            if os.path.exists(md_file):
                shutil.copy(
                    md_file, os.path.join(destination_folder, f"{folder_name}.md")
                )
                print(f"已复制: {md_file}")


def process_json_files(source_folder, output_file):
    # 打开jsonl文件进行写入
    with open(output_file, "w", encoding="utf-8") as outfile:
        # 遍历源文件夹中的所有文件
        for file_name in os.listdir(source_folder):
            file_path = os.path.join(source_folder, file_name)

            if file_name.endswith("_content_list.json"):
                file_name = file_name.replace("_content_list.json", "")
                # 处理json文件
                with open(file_path, "r", encoding="utf-8") as jf:
                    content_list = json.load(jf)
                    combined_text = "".join(
                        [
                            item["content"]
                            for item in content_list
                            if item["type"] == "text"
                        ]
                    )
                    result = {"title": file_name, "content": combined_text}
                    json.dump(result, outfile, ensure_ascii=False)
                    outfile.write("\n")


def process_md_files(source_folder, output_file):
    # 打开jsonl文件进行写入
    with open(output_file, "w", encoding="utf-8") as outfile:
        # 遍历源文件夹中的所有文件
        for file_name in os.listdir(source_folder):
            file_path = os.path.join(source_folder, file_name)

            if file_name.endswith(".md"):
                file_name = file_name.replace(".md", "")
                # 处理md文件
                with open(file_path, "r", encoding="utf-8") as mf:
                    content = mf.read()
                    result = {"title": file_name, "content": content}
                    json.dump(result, outfile, ensure_ascii=False)
                    outfile.write("\n")


def save_jsonl_and_md_files(source_folder, output_file):
    pass


if __name__ == "__main__":
    # 示例使用
    source_folder = "你的提取文件夹路径"
    output_file = "你的输出jsonl文件路径"
    save_jsonl_and_md_files(source_folder, output_file)
    pass
