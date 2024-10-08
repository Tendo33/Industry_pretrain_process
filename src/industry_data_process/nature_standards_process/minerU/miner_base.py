import os
from magic_pdf.pipe.UNIPipe import UNIPipe
from magic_pdf.rw.DiskReaderWriter import DiskReaderWriter
import magic_pdf.model as model_config
from nb_log import get_logger

logger = get_logger(
    "mineru_folder",
    formatter_template=5,
)
os.environ["CUDA_VISIBLE_DEVICES"] = "3"


# 使用内部模型
model_config.__use_inside_model__ = True


def process_pdf_file(file_path: str, image_dir: str, model_json: list = []):
    """
    处理单个PDF文件，将其内容转换为Markdown格式。

    参数：
    - file_path: PDF文件路径
    - image_dir: 保存图像的目录
    - model_json: 模型配置的JSON列表

    返回：
    - md_content: 生成的Markdown内容
    """
    try:
        # 读取PDF文件
        with open(file_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()

        # 初始化图像写入器
        image_writer = DiskReaderWriter(image_dir)
        json_useful_key = {"_pdf_type": "", "model_list": model_json}

        # 初始化UNIPipe对象并进行处理
        pipe = UNIPipe(pdf_bytes, json_useful_key, image_writer)
        pipe.pipe_classify()
        """如果没有传入有效的模型数据，则使用内置model解析"""
        if len(model_json) == 0:
            if model_config.__use_inside_model__:
                pipe.pipe_analyze()
            else:
                logger.error("need model list input")
                exit(1)
        pipe.pipe_parse()
        md_content = pipe.pipe_mk_markdown(image_dir, drop_mode="none")

        return md_content

    except Exception as e:
        logger.exception(f"处理文件 {file_path} 时出现异常：{e}")
        return None


def process_pdf_folder(folder_path: str, image_dir: str, model_json: list = []):
    """
    处理文件夹中的所有PDF文件，将其内容转换为Markdown格式。

    参数：
    - folder_path: PDF文件夹路径
    - image_dir: 保存图像的目录
    - model_json: 模型配置的JSON列表（可选）
    """
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(folder_path, filename)
                md_content = process_pdf_file(file_path, image_dir, model_json)
                if md_content is not None:
                    output_md_path = os.path.splitext(file_path)[0] + ".md"

                    # 将生成的Markdown内容写入文件
                    with open(output_md_path, "w", encoding="utf-8") as md_file:
                        md_file.write(md_content)

                    print(
                        f"处理完成 {filename} 并保存Markdown内容至 {output_md_path}"
                    )
    except Exception as e:
        logger.exception(f"处理文件夹 {folder_path} 时出现异常：{e}")


if __name__ == "__main__":
    pdf_folder_path = r"/workspace/sunjinfeng/github_projet/Industry_pretrain_process/data/test_data"
    local_image_dir = r"/workspace/sunjinfeng/github_projet/Industry_pretrain_process/data/test_data_output"

    # 处理PDF文件夹
    process_pdf_folder(pdf_folder_path, local_image_dir)
