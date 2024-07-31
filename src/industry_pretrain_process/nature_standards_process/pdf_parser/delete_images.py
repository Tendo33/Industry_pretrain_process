import os
import shutil

def delete_images_in_subfolders(folder_path):
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif'}

    for root, _, files in os.walk(folder_path):
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                try:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f'Deleted {file_path}')
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")


def move_directories(src_dir, dst_dir):
    if not os.path.exists(src_dir):
        print(f"源文件夹 '{src_dir}' 不存在")
        return

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for item in os.listdir(src_dir):
        item_path = os.path.join(src_dir, item)
        if os.path.isdir(item_path):
            try:
                shutil.move(item_path, dst_dir)
                print(f"文件夹 '{item}' 已移动到 '{dst_dir}'")
            except Exception as e:
                print(f"Error moving {item_path} to {dst_dir}: {e}")

if __name__ == '__main__':

    folder_path = r'/home/sunjinf/github_projet/nature_data/papers_1'
    target_dir = r'/home/sunjinf/github_projet/nature_data/papers_1_out'

    delete_images_in_subfolders(folder_path)
    move_directories(folder_path, target_dir)
