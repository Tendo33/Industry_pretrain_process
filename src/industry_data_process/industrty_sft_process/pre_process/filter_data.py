import pandas as pd
import json
from typing import Any, Dict


def load_data(file_path: str) -> pd.DataFrame:
    """
    从指定路径加载Parquet文件并返回DataFrame对象。

    Args:
        file_path (str): Parquet文件路径。

    Returns:
        pd.DataFrame: 加载的DataFrame对象。
    """
    return pd.read_parquet(file_path)


def process_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    对数据进行处理，提取并清洗 'title' 和 'content' 列。

    Args:
        data (pd.DataFrame): 需要处理的DataFrame对象。

    Returns:
        pd.DataFrame: 处理后的DataFrame对象。
    """
    processed_data = data[["title", "content"]].copy()

    processed_data.dropna(subset=["title", "content"], inplace=True)

    processed_data["title"] = processed_data["title"].str.strip()
    processed_data["content"] = processed_data["content"].str.strip()

    return processed_data


def save_to_jsonl(data: pd.DataFrame, output_path: str) -> None:
    """
    将DataFrame数据保存为JSONL格式的文件。

    Args:
        data (pd.DataFrame): 需要保存的DataFrame对象。
        output_path (str): 输出JSONL文件的路径。
    """
    with open(output_path, "w", encoding="utf-8") as file:
        for _, row in data.iterrows():
            record: Dict[str, Any] = row.to_dict()
            json_record = json.dumps(record, ensure_ascii=False)
            file.write(json_record + "\n")


if __name__ == "__main__":
    # 设置文件路径
    DATA_PATH = r"/data/nfs/data/Magpie-Qwen2-Pro-200K-Chinese/data/train-00000-of-00002.parquet"
    OUTPUT_PATH = "output.jsonl"

    # 读取Parquet文件
    data = load_data(DATA_PATH)

    # 显示数据的前几行
    print(data.head())

    # 处理数据
    processed_data = process_data(data)

    # 保存处理后的数据为JSONL格式
    save_to_jsonl(processed_data, OUTPUT_PATH)

    print(f"处理后的数据已成功保存为JSONL格式，文件路径为: {OUTPUT_PATH}")
