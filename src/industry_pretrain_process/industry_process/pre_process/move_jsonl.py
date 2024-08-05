import os
import shutil


def move_jsonl_files(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in os.listdir(source_dir):
        if filename.endswith(".jsonl"):
            source_file = os.path.join(source_dir, filename)
            target_file = os.path.join(target_dir, filename)

            shutil.move(source_file, target_file)
            print(f"Moved: {source_file} to {target_file}")


if __name__ == "__main__":
    source_directory = r"/data/nfs/data/IndustryCorpus/chinese"
    target_directory = r"/data/nfs/data/Industry_raw_data"

    move_jsonl_files(source_directory, target_directory)
