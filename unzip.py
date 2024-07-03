import gzip
import shutil
import os
from tqdm import tqdm
from pathlib import Path

def decompress_gz_files(folder_path):
    folder_path = Path(folder_path)

    for file_path in tqdm(folder_path.rglob('*.gz'), desc="Decompressing"):
        output_file_path = file_path.with_suffix('')  # 去掉 '.gz'

        try:
            with gzip.open(file_path, 'rb') as f_in:
                with open(output_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        except gzip.BadGzipFile:
            tqdm.write(
                f"{file_path} is not a valid gzip file, trying to copy directly.")
            try:
                # 尝试直接复制文件
                shutil.copyfile(file_path, output_file_path)
            except Exception as e:
                tqdm.write(f"Error copying {file_path}: {e}")
        except Exception as e:
            tqdm.write(f"Error decompressing {file_path}: {e}")

if __name__ == '__main__':
    folder_path = r'/data/nfs/data/MNBVC'
    decompress_gz_files(folder_path)
