import jionlp
from utils.file_clean_util import extract_key_information
from utils.content_clean_util import new_base_clean
from utils.save_file import save_to_jsonl


def process_base(source_file_path: str, target_file_path: str) -> None:

    contents = extract_key_information(source_file_path, "text")
    lang_score = extract_key_information(source_file_path, "lang_score")
    special_char_ratio = extract_key_information(
        source_file_path, "special_char_ratio")
    char_rep_ratio = extract_key_information(
        source_file_path, "char_rep_ratio")
    perplexity = extract_key_information(source_file_path, "perplexity")

    cleaned_content_list = new_base_clean(contents)

    pass


if __name__ == '__main__':
    pass
