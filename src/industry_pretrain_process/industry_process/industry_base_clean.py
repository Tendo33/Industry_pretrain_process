from utils.file_clean_util import extract_key_information
from utils.content_clean_util import pretrain_base_clean
from utils.save_file import save_to_jsonl


def create_temp_dict(
    content_list: list[str],
    lang_score_list: list[float],
    special_char_ratio_list: list[float],
    char_rep_ratio_list: list[float],
    perplexity_list: list[float],
) -> list[dict]:
    temp_list = []

    for (
        content,
        lang_score,
        special_char_ratio,
        char_rep_ratio,
        perplexity,
    ) in zip(
        content_list,
        lang_score_list,
        special_char_ratio_list,
        char_rep_ratio_list,
        perplexity_list,
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
    ]
    dict_temp = extract_key_information(source_file_path, keys)

    texts = dict_temp["text"]
    lang_scores = dict_temp["lang_score"]
    special_char_ratios = dict_temp["special_char_ratio"]
    char_rep_ratios = dict_temp["char_rep_ratio"]
    perplexities = dict_temp["perplexity"]

    cleaned_content_list = pretrain_base_clean(texts)

    # 将清理后的数据和提取的信息保存为JSONL文件
    data_list = create_temp_dict(
        cleaned_content_list,
        lang_scores,
        special_char_ratios,
        char_rep_ratios,
        perplexities,
    )
    print(len(data_list))
    save_to_jsonl(data_list, target_file_path)


if __name__ == "__main__":
    source_file_path = r"/data/nfs/data/Industry_raw_data/law.jsonl"
    target_file_path = r"/data/nfs/data/Industry_raw_data/law_filter.jsonl"
    process_base(source_file_path, target_file_path)
