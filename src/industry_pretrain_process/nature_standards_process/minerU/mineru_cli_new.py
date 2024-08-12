import os
import subprocess
from nb_log import get_logger

logger = get_logger(
    "mineru_folder_cli_new",
    formatter_template=5,
    log_path="../../../../logs/",
    log_filename="mineru_folder_cli_new.log",
)

os.environ["CUDA_VISIBLE_DEVICES"] = "1"


def process_pdfs_in_directory(directory, output_base_dir, method="auto"):
    """
    遍历指定目录下的所有PDF文件，并使用magic-pdf工具进行解析。

    :param directory: 包含PDF文件的目录路径
    :param output_base_dir: 解析结果保存的基础目录
    :param method: 解析方法，可以是'ocr', 'txt' 或 'auto'
    """
    # 检查目录是否存在
    if not os.path.exists(directory):
        logger.error(f"目录 {directory} 不存在")
        return

    # 确保输出基础目录存在
    os.makedirs(output_base_dir, exist_ok=True)

    # 遍历目录中的所有PDF文件
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            base_filename = os.path.splitext(filename)[0]
            output_dir = os.path.join(output_base_dir, base_filename)

            # 检查是否存在同名文件夹，若存在则跳过
            if os.path.exists(output_dir):
                logger.info(f"文件 {pdf_path} 已被处理，跳过")
                continue

            logger.info(f"正在处理文件: {pdf_path}")

            # 构建命令
            command = [
                "magic-pdf",
                "-p",
                pdf_path,
                "-o",
                output_dir,
                "-m",
                method,
            ]

            # 运行命令
            try:
                result = subprocess.run(
                    command,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                logger.info(f"输出: {result.stdout.decode('utf-8')}")
            except subprocess.CalledProcessError as e:
                logger.error(f"错误: {e.stderr.decode('utf-8')}")
            except Exception as e:
                logger.error(f"未知错误: {str(e)}")


if __name__ == "__main__":
    directory = (
        r"/workspace/sunjinfeng/github_projet/nature_data/data_origin/origin_paper"
    )
    output_base_dir = r"/workspace/sunjinfeng/github_projet/nature_data/data_after_process/out_paper_mineru"

    process_pdfs_in_directory(
        directory=directory, output_base_dir=output_base_dir, method="ocr"
    )
