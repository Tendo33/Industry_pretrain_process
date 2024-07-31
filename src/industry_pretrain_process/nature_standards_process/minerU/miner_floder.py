from magic_pdf.pipe.UNIPipe import UNIPipe
from magic_pdf.rw.DiskReaderWriter import DiskReaderWriter
import magic_pdf.model as model_config

model_config.__use_inside_model__ = True

with open('assets\***手册.pdf', "rb") as pdf_file:
    pdf_bytes = pdf_file.read()

local_image_dir = "mineru_images"

image_writer = DiskReaderWriter(local_image_dir)

model_json = []  # model_json传空list使用内置模型解析
jso_useful_key = {"_pdf_type": "", "model_list": model_json}
pipe = UNIPipe(pdf_bytes, jso_useful_key, image_writer)
pipe.pipe_classify()
pipe.pipe_parse()
md_content = pipe.pipe_mk_markdown(local_image_dir, drop_mode="none")
