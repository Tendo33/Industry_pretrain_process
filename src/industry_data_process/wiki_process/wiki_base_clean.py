import os
from tqdm import tqdm
import jionlp
from src.utils.file_clean_util import extract_key_information
from src.utils.content_clean_util import remove_invalid_line
from src.utils.save_file import save_to_jsonl

from nb_log import get_logger

logger = get_logger(
    name="nature",
    log_path="log",
    log_filename="nature_data_clean",
    formatter_template=5,
)


def make_pretrain_data(contents: list[str], titles: list[str]) -> list:
    temp_list = []
    for content, title in tqdm(
        zip(contents, titles), total=len(contents), desc="清洗中"
    ):
        content = jionlp.clean_text(
            content,
            remove_email=True,
            remove_phone_number=True,
            remove_url=False,
            remove_parentheses=False,
            delete_prefix=True,
        )
        text = f"{title}\n{content}"
        if len(text) > 20 and len(text) < 5000:
            temp = {
                "text": text,
            }
            temp_list.append(temp)

    return temp_list


def process_base(source_file_path: str, target_file_path: str) -> None:
    # 从原始文件中提取标题、内容、大纲和政策文件
    key = ["title", "content"]
    dict_temp = extract_key_information(source_file_path, key)

    title = dict_temp["title"]
    contents = dict_temp["content"]

    temp_dict_list = make_pretrain_data(contents, title)
    print("清洗后的数据长度：", len(temp_dict_list))

    save_to_jsonl(temp_dict_list, target_file_path)


if __name__ == "__main__":
    file_path = r"/workspace/sunjinfeng/github_projet/LLaMA-Factory/data/nature_dataset_wiki_v1.jsonl"
    out_path = r"/workspace/sunjinfeng/github_projet/LLaMA-Factory/data/nature_dataset_wiki_v2.jsonl"
    process_base(file_path, out_path)
    print("Done!")
