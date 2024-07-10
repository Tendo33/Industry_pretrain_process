import os


def delete_images_in_subfolders(folder_path):

    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']

    # 遍历主文件夹中的所有子文件夹
    for root, dirs, files in os.walk(folder_path):

        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in image_extensions:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f'Deleted {file_path}')


if __name__ == '__main__':
    folder_path = r'/home/sunjinf/github_projet/nature_data/all_pdf_files'
    delete_images_in_subfolders(folder_path)
