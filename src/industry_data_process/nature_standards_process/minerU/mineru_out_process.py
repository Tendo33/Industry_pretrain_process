import json
import os
import shutil
import jionlp


def extract_files(source_folder: str, destination_folder: str) -> None:
    # 确保目标文件夹存在
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 遍历源文件夹中的所有子文件夹
    for folder_name in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder_name)

        if os.path.isdir(folder_path):
            # 构造文件路径
            json_file = os.path.join(
                folder_path, "ocr", f"{folder_name}_content_list.json"
            )
            md_file = os.path.join(folder_path, "ocr", f"{folder_name}.md")
            # 检查文件是否存在并复制
            # print(f"正在处理: {json_file}")
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
                    combined_text = "\n".join(
                        [
                            item["text"]
                            for item in content_list
                            if item["type"] == "text"
                            and not item["text"].startswith("图")
                            and not item["text"].startswith("表")
                        ]
                    )
                    combined_text = jionlp.clean_text(
                        combined_text, remove_parentheses=False
                    )
                    combined_text = combined_text.replace("\n\n", "\n")
                    if len(combined_text) > 300:
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
                    if len(content) > 300:
                        result = {"title": file_name, "content": content}
                        json.dump(result, outfile, ensure_ascii=False)
                        outfile.write("\n")


if __name__ == "__main__":
    # 示例使用
    source_folder = r"/home/sunjinf/github_projet/nature_data/MinerU/magic-pdf"
    target_folder = (
        r"/home/sunjinf/github_projet/nature_data/data_after_process/out_paper_mineru"
    )
    jsonl_test_file = os.path.join(target_folder, "1out_paper_mineru_json.jsonl")
    md_test_file = os.path.join(target_folder, "1out_paper_mineru_md.jsonl")
    extract_files(source_folder, target_folder)
    print("文件复制完成")
    process_json_files(target_folder, jsonl_test_file)
    print("json文件处理完成")
    process_md_files(target_folder, md_test_file)
    print("md文件处理完成")
