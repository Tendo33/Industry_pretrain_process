from utils.file_clean_util import directory_parquet_to_jsonl


if __name__ == "__main__":
    parquet_dir: str = "/data/nfs/data/Magpie-Llama-3.1-Pro-300K-Filtered"
    output_dir: str = "/data/nfs/data/Magpie-Llama-3.1-Pro-300K-Filtered-jsonl"

    directory_parquet_to_jsonl(parquet_dir, output_dir)
    print("Done!")
