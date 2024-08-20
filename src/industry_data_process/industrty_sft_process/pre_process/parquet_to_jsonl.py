import os
import pandas as pd
import json
import numpy as np
from typing import Dict, Any


def convert_ndarray_to_list(record) -> Dict[str, Any]:
    """
    将record中的ndarray对象转换为列表，以便进行JSON序列化。
    """
    for key, value in record.items():
        if isinstance(value, np.ndarray):
            record[key] = value.tolist()
            # print(f"Converted ndarray at key '{key}' to list.")  # 调试信息
        elif isinstance(value, (list, dict)):
            # 如果值本身是列表或字典，递归处理
            record[key] = convert_ndarray_to_list(value)
    return record


def parquet_to_jsonl(parquet_file: str, jsonl_file: str) -> None:
    try:
        # 读取parquet文件
        df: pd.DataFrame = pd.read_parquet(parquet_file)

        # 将DataFrame转换为jsonl格式并写入文件
        with open(jsonl_file, "w", encoding="utf-8") as f:
            for record in df.to_dict(orient="records"):
                record = convert_ndarray_to_list(record)  # 转换ndarray对象
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    except Exception as e:
        print(f"Failed to convert {parquet_file}: {str(e)}")


def convert_directory(parquet_dir: str, output_dir: str) -> None:
    for root, dirs, files in os.walk(parquet_dir):
        for file in files:
            if file.endswith(".parquet"):
                parquet_file: str = os.path.join(root, file)

                # 创建输出目录结构
                relative_path: str = os.path.relpath(root, parquet_dir)
                jsonl_output_dir: str = os.path.join(output_dir, relative_path)
                os.makedirs(jsonl_output_dir, exist_ok=True)

                # 设置输出jsonl文件路径
                jsonl_file: str = os.path.join(
                    jsonl_output_dir, file.replace(".parquet", ".jsonl")
                )

                # 转换并保存
                parquet_to_jsonl(parquet_file, jsonl_file)
                print(f"Converted: {parquet_file} -> {jsonl_file}")


if __name__ == "__main__":
    parquet_dir: str = "/data/nfs/data/Infinity-Instruct"
    output_dir: str = "/data/nfs/data/Infinity-Instruct-jsonl"

    convert_directory(parquet_dir, output_dir)
