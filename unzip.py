import gzip
import shutil
import os

from tqdm import tqdm


def decompress_gz_files(folder_path):
    for root, _, files in os.walk(folder_path):
        for file_name in tqdm(files):
            if file_name.endswith('.gz'):
                file_path = os.path.join(root, file_name)
                output_file_path = os.path.join(
                    root, file_name[:-3])  # 去掉 '.gz'

                with gzip.open(file_path, 'rb') as f_in:
                    with open(output_file_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

                print(f"Decompressed: {file_path}")


# 使用示例
folder_path = r'/data/nfs/data/IndustryCorpus/chinese'
decompress_gz_files(folder_path)
