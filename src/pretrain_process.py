import jionlp
from utils.file_clean_util import extract_key_information
from utils.content_clean_util import pretrain_base_clean
from utils.save_file import save_to_jsonl


def create_temp_dict(content_list: list[str], title_list: list[str], outline_list: list[str], policy_list: list[str]) -> list[dict]:
    temp_list = []

    for content, title, outline, policy in zip(content_list, title_list, outline_list, policy_list):
        pass

    return temp_list


def process_base(source_file_path: str, target_file_path: str) -> None:

    texts = extract_key_information(source_file_path, "text")
    lang_scores = extract_key_information(source_file_path, "lang_score")
    special_char_ratios = extract_key_information(
        source_file_path, "special_char_ratio")
    char_rep_ratios = extract_key_information(
        source_file_path, "char_rep_ratio")
    perplexities = extract_key_information(source_file_path, "perplexity")

    cleaned_content_list = pretrain_base_clean(texts)

    pass


if __name__ == '__main__':
    pass
