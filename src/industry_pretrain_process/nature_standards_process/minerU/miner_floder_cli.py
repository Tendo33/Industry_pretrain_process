import os
import subprocess
from nb_log import get_logger

logger = get_logger(
    "mineru_folder_cli",
    formatter_template=5,
)
os.environ["CUDA_VISIBLE_DEVICES"] = "1"


def process_pdfs_in_directory(
    directory,
    model_path="",
    method="auto",
    inside_model=True,
    model_mode="full",
):
    """
    遍历指定目录下的所有PDF文件，并使用magic-pdf工具进行解析。

    :param directory: 包含PDF文件的目录路径
    :param model_path: 模型文件路径,model_json_path
    :param method: 解析方法，可以是'ocr', 'txt' 或 'auto'
    :param inside_model: 是否使用内置模型
    :param model_mode: 内置模型选择，可以是'lite'或'full'
    """
    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f"目录 {directory} 不存在")
        return

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            base_filename = os.path.splitext(filename)[0]
            folder_path = os.path.join(
                "/workspace/sunjinfeng/github_projet/nature_data/MinerU/magic-pdf",
                base_filename,
            )

            # 检查是否存在同名文件夹
            if os.path.exists(folder_path):
                logger.info(f"文件 {pdf_path} 已被处理，跳过")
                continue

            logger.error(f"正在处理文件: {pdf_path}")

            # 构建命令
            command = [
                "magic-pdf",
                "pdf-command",
                "--pdf",
                pdf_path,
                "--method",
                method,
                "--inside_model",
                str(inside_model),
                "--model_mode",
                model_mode,
            ]

            # 如果model_path不为空，则添加--model参数
            if model_path:
                command.extend(["--model", model_path])

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


if __name__ == "__main__":
    directory = (
        r"/workspace/sunjinfeng/github_projet/nature_data/data_origin/origin_standard"
    )

    model_path = r""

    process_pdfs_in_directory(
        directory=directory,
        model_path=None,
        method="ocr",
        inside_model=True,
        model_mode="full",
    )
