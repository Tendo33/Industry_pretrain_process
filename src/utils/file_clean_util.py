import re
import os
import glob
import json
from typing import Union, List


# 删除文件名中不包含关键词的文件
# keywords_list = ["国家", "国务院", "国资委", "海关总署", "交通运输部", "教育部", "民政部", "办公厅", "农业农村部", "人力资源社会保障部", "商务部", "水利部", "统计局", "文化和旅游部", "中国银监会", "住房和城乡建设部"]
def delete_files_not_containing_keywords(folder_path: str, keywords: list) -> None:
    files = os.listdir(folder_path)

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if not any(keyword in file_name for keyword in keywords):
            os.remove(file_path)
            print(f"Deleted: {file_path}")


# 删除文件名字中包含关键词的文件
# keywords_list = ["解读", "答记者问", "!", "！", "：", "“"]
def delete_files_containing_keywords(folder_path: str, keywords: list) -> None:
    # 获取文件夹中的文件列表
    files = os.listdir(folder_path)

    # 遍历文件夹中的文件
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)

        # 检查文件名是否包含关键词列表中的任意一个关键词
        if any(keyword in file_name for keyword in keywords):
            # 文件名包含关键词，删除文件
            os.remove(file_path)
            print(f"Deleted: {file_path}")


# 删除不以特殊关键字开头的文件
# keywords_list = ["国家", "国务院", "国资委", "海关总署", "交通运输部", "教育部", "工业和信息化部", "民政部", "农业农村部", "人力资源社会保障部", "商务部", "水利部", "统计局", "文化和旅游部", "中国银监会", "住房和城乡建设部", "最高人民法院", "自然资源部", "总局办公厅"]
def delete_files_not_starting_with_keywords(folder_path: str, keywords: list) -> None:
    files = os.listdir(folder_path)

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if not any(file_name.startswith(keyword) for keyword in keywords):
            os.remove(file_path)
            print(f"Deleted: {file_path}")


# 删除不以特殊关键字结尾的文件（格式）
# keywords_list = [".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".txt"]
def delete_files_not_ending_with_keywords(folder_path: str, keywords: list):
    # 获取文件夹中所有文件和文件夹
    all_items = glob.glob(os.path.join(folder_path, '*'))

    for item_path in all_items:
        if os.path.isfile(item_path):  # 检查是否为文件
            should_delete = True
            for keyword in keywords:
                if item_path.endswith(keyword):
                    should_delete = False
                    break
            if should_delete:
                os.remove(item_path)
                print(f"文件 {item_path} 已删除.")


# 删除文件大小小于指定大小的文件
def delete_small_files(folder_path: str, size: int):
    all_files = os.listdir(folder_path)
    # 遍历文件夹中的文件
    for file_name in all_files:
        file_path = os.path.join(folder_path, file_name)

        # 检查文件是否为空
        if os.path.getsize(file_path) < size:
            os.remove(file_path)
            print(f"空文件 {file_path} 已删除.")


# 删除 jsonl 文件中正文的换行符小于 n 的文件
def delete_few_sentences_files(folder_path: str, num: int):
    # 获取文件夹中的文件列表
    files = os.listdir(folder_path)

    # 遍历文件夹中的文件
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)

        # 检查文件是否以 ".jsonl" 结尾
        if file_name.endswith('.jsonl'):
            # 读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

                # 检查content字段中换行符的数量
                newline_count = data.get('content', '').count('\n')

                # 如果换行符少于10个，删除文件
                if newline_count < num:
                    # 关闭文件
                    json_file.close()
                    # 删除文件
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
        # else:
        #     # 删除不是 JSONL 格式的文件
        #     os.remove(file_path)
        #     print(f"Deleted: {file_path}")


# 获取文件夹中的所有文件名
def get_filenames(folder_path: str):
    all_filenames = []

    for filename in os.listdir(folder_path):
        all_filenames.append(os.path.splitext(filename)[0])  # 不包括后缀

    return all_filenames


# 判断 title 的类别
def categories_count(titles: list[str]) -> dict:
    # 定义类别字典，初始化计数为0
    categories_dict = {
        "命令": 0,
        "议案": 0,
        "公报": 0,
        "纪要": 0,
        "公告": 0,
        "通告": 0,
        "意见": 0,
        "通知": 0,
        "通报": 0,
        "报告": 0,
        "请示": 0,
        "批复": 0,
        "函": 0,
        "决议": 0,
        "决定": 0
    }
    for title in titles:
        for category in categories_dict:
            # 如果类别出现在文件名的末尾5个字符中，则增加该类别的计数
            if category in title[-5:]:
                categories_dict[category] += 1
                break  # 找到匹配的类别后跳出内循环

    return categories_dict


# 提取出文件夹内 txt 文件的内容保存为 list[dict]
def extract_txt_content(folder_path: str) -> list[dict]:
    all_txt_data = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                txt_data = {
                    "file_name": file,
                    "file_path": file_path,
                    "content": content
                }
                # 将每个txt文件的数据添加到列表中
                all_txt_data.append(txt_data)
    return all_txt_data


# 从 jsonl 中提取 key 信息
def extract_key_information(file_path: str, keywords: str) -> List[str]:
    keyword_out = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line)
            keyword_out.append(data.get(keywords, '').strip())

    return keyword_out
