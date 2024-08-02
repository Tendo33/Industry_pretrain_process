import json
import os
from magic_pdf.pipe.TXTPipe import TXTPipe
from magic_pdf.pipe.OCRPipe import OCRPipe
from magic_pdf.pipe.UNIPipe import UNIPipe
from magic_pdf.rw.DiskReaderWriter import DiskReaderWriter
import magic_pdf.model as model_config

from nb_log import get_logger

logger = get_logger('mineru_folder', formatter_template=5,)
os.environ["CUDA_VISIBLE_DEVICES"] = "3"

# 使用内部模型
model_config.__use_inside_model__ = True


def json_md_dump(pipe, md_writer, pdf_name, content_list, md_content):
    """将解析结果写入JSON和Markdown文件"""
    output_files = {
        f"{pdf_name}_model.json": pipe.model_list,
        f"{pdf_name}_middle.json": pipe.pdf_mid_data,
        f"{pdf_name}_content_list.json": content_list,
        f"{pdf_name}.md": md_content
    }
    
    for file_name, content in output_files.items():
        md_writer.write(content=json.dumps(content, ensure_ascii=False, indent=4)
                        if file_name.endswith('.json') else content, path=file_name)


def pdf_parse_main(pdf_path: str, parse_method: str = 'auto', model_json_path: str = None, is_json_md_dump: bool = True, output_dir: str = None):
    """
    执行从 pdf 转换到 json、md 的过程，输出 md 和 json 文件到指定目录

    :param pdf_path: .pdf 文件的路径
    :param parse_method: 解析方法，可选 'auto'、'ocr'、'txt'，默认 'auto'
    :param model_json_path: 已存在的模型数据文件路径
    :param is_json_md_dump: 是否将解析后的数据写入到 .json 和 .md 文件中，默认 True
    :param output_dir: 输出结果的目录地址，默认与 pdf 文件相同目录
    """
    try:
        # 获取pdf文件名（不含扩展名）
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        # 设置输出路径
        output_path = os.path.join(
            output_dir or os.path.dirname(pdf_path), pdf_name)
        output_image_path = os.path.join(output_path, 'images')
        image_path_parent = os.path.basename(output_image_path)

        # 创建输出目录和图像目录
        os.makedirs(output_path, exist_ok=True)
        os.makedirs(output_image_path, exist_ok=True)

        # 读取pdf文件的二进制数据
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        # 如果提供了模型数据文件路径，则加载模型数据
        model_json = json.load(
            open(model_json_path, "r", encoding="utf-8")) if model_json_path else []

        # 创建读写器对象
        image_writer, md_writer = DiskReaderWriter(
            output_image_path), DiskReaderWriter(output_path)

        # 根据解析方法选择相应的处理管道
        pipe = {
            "auto": lambda: UNIPipe(pdf_bytes, {"_pdf_type": "", "model_list": model_json}, image_writer),
            "txt": lambda: TXTPipe(pdf_bytes, model_json, image_writer),
            "ocr": lambda: OCRPipe(pdf_bytes, model_json, image_writer)
        }.get(parse_method, lambda: None)()

        if not pipe:
            logger.error("未知解析方法，仅支持 auto, ocr, txt")
            return

        # 执行分类
        pipe.pipe_classify()

        # 如果没有提供模型数据且使用内部模型，则进行解析
        if not model_json and model_config.__use_inside_model__:
            pipe.pipe_analyze()
        elif not model_json:
            logger.error("需要模型列表输入")
            return

        # 执行解析
        pipe.pipe_parse()

        # 生成统一格式和Markdown格式的内容
        content_list = pipe.pipe_mk_uni_format(
            image_path_parent, drop_mode="none")
        md_content = pipe.pipe_mk_markdown(image_path_parent, drop_mode="none")

        # 如果需要，写入结果到JSON和Markdown文件
        if is_json_md_dump:
            json_md_dump(pipe, md_writer, pdf_name, content_list, md_content)

    except Exception as e:
        logger.exception(e)


def process_all_pdfs_in_directory(directory: str, parse_method: str = 'auto', model_json_path: str = None, is_json_md_dump: bool = True, output_dir: str = None):
    """
    处理目录中的所有 PDF 文件

    :param directory: 要处理的目录路径
    :param parse_method: 解析方法，可选 'auto'、'ocr'、'txt'，默认 'auto'
    :param model_json_path: 已存在的模型数据文件路径
    :param is_json_md_dump: 是否将解析后的数据写入到 .json 和 .md 文件中，默认 True
    :param output_dir: 输出结果的目录地址，默认与每个 pdf 文件相同目录
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                pdf_parse_main(pdf_path, parse_method,
                               model_json_path, is_json_md_dump, output_dir)


if __name__ == '__main__':
    pdf_directory = r"xxx"
    process_all_pdfs_in_directory(pdf_directory)
