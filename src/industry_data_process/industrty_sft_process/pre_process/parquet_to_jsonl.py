from utils.file_clean_util import directory_parquet_to_jsonl


if __name__ == "__main__":
    parquet_dir: str = "/data/nfs/data/Infinity-Instruct"
    output_dir: str = "/data/nfs/data/Infinity-Instruct-jsonl"

    directory_parquet_to_jsonl(parquet_dir, output_dir)
