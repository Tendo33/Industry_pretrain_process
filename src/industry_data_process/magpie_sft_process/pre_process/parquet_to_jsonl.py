from utils.file_clean_util import directory_parquet_to_jsonl


if __name__ == "__main__":
    parquet_dir: str = "/data/nfs/data/Magpie-Qwen2-Pro-1M-v0.1"
    output_dir: str = "/data/nfs/data/Magpie-Qwen2-Pro-1M-v0.1-jsonl"

    directory_parquet_to_jsonl(parquet_dir, output_dir)
    print("Done!")
