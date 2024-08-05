import jionlp
import json
from tqdm import tqdm


def process_base(source_file_path: str, target_file_path: str) -> None:
    with open(source_file_path, "r", encoding="utf-8") as f:
        with open(target_file_path, "w", encoding="utf-8") as fw:
            for line in tqdm(f):
                data = json.loads(line)
                text = data["text"]
                lang_score = data["lang_score"]
                # special_char_ratio = data["special_char_ratio"]
                # char_rep_ratio = data["char_rep_ratio"]
                perplexity = data["perplexity"]
                lang = data["lang"]
                if lang_score > 0.9 and perplexity < 1200 and lang == "zh":
                    text = jionlp.clean_text(text)
                    data["text"] = text
                    fw.write(json.dumps(data, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    source_file_path = r"/data/nfs/data/Industry_raw_data/agriculture.jsonl"
    target_file_path = (
        r"/data/nfs/data/Industry_raw_data/data_filter/agriculture_filter.jsonl"
    )
    process_base(source_file_path, target_file_path)
