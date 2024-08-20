import os
import sys
import logging


def get_logger(name: str) -> logging.Logger:
    r"""
    Gets a standard logger with a stream hander to stdout.
    """
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
    )
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 创建控制台处理器
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # 创建文件处理器
    log_file_path = os.path.join(
        os.path.dirname(__file__), "gongwen_data_clean_project.log"
    )
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 添加处理器到日志记录器
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


def title_prompt(title: str) -> str:
    res = f"请根据标题写一篇标题为《{title}》的公文。"
    return res


def old_gw_prompt(
    title: str, outline: str, policy_files: list, refer_files: str
) -> str:
    pf = "\n".join(["《" + line + "》" for line in policy_files])
    rf = "\n".join(refer_files)
    res = f'''[角色]：你是一名专业的政府公文写作专家，擅长根据提供的大纲和标题书写完整的公文。你写的公文语言表述精炼用词得体，逻辑严谨政治正确。
[输入]：
"大纲"：
"""
{outline}
"""
"政策文件"：
"""
{policy_files} 
"""
"参考内容"：
"""
{refer_files}
"""
[任务指令]：请严格按照大纲写一篇标题为《{title}》的公文。大纲内容不得更改，必须完全一致。生成内容必须参考提供的"政策文件"和"参考内容"。
[输出指示器]：不输出参考内容和额外的标签，仅输出生成内容'''
    return res


# 定义函数生成公文的 prompt
def generate_prompt_new(title, outline, policy_files=None, refer_files=None):
    policy_valid = False
    reference_valid = False

    if len(policy_files) > 5:
        policy_valid = True
    if len(refer_files) > 10:
        reference_valid = True

    prompt = f'''你是一名专业的政府公文写作专家，请严格按照以下要求撰写一篇标题为《{title}》的公文。
1. 请严格按照以下大纲撰写：
"""
{outline}
"""
'''

    # 条件处理内容部分
    if policy_valid and reference_valid:
        prompt += f'''
2. 公文的内容必须参考并引用以下"政策文件"和"参考内容"中的信息：
"政策文件"：
"""
{policy_files}
"""
"参考内容"：
"""
{refer_files}
"""
'''
    elif policy_valid:
        prompt += f'''
2. 公文的内容必须参考并使用以下"政策文件"中的信息：

"政策文件"：
"""
{policy_files}
"""
'''
    elif reference_valid:
        prompt += f'''
2.公文的内容必须参考并使用以下"参考内容"中的信息：

"参考内容"：
"""
{refer_files}
"""
'''
    else:
        prompt += """
2.请根据公文的标准内容要求，撰写一篇全面且详实的公文。
"""

    # 添加格式和语气要求
    prompt += """请按照以上要求生成完整的公文。"""

    return prompt


def new_gw_prompt(
    title: str, outline: str, policy_files: str, refer_files: str
) -> str:
    res = f'''你是一名专业的政府公文写作专家，请严格按照"大纲"写一篇标题为《{title}》的公文,生成内容必须参考提供的"政策文件"和"参考内容"。
"大纲"：
"""
{outline}
"""
"政策文件"：
"""
{policy_files} 
"""
"参考内容"：
"""
{refer_files}
"""'''

    return res


def construct_outline_prompt(title: str) -> str:
    res = f"[角色]：你是一名专业的政府公文写作专家，擅长根据提供的标题生成完整的公文大纲。\n[任务指令]：请按照标题《{title}》生成公文的大纲。"
    return res


def construct_outline_prompt_new(text: str) -> str:
    prompt = f"你是一名专业的政府公文大纲生成专家\n请按照标题《{text}》生成公文的大纲。"
    return prompt


# 制作普通数据集
def construct_dataset(prompt, output, system):
    res = {
        "instruction": prompt,
        "input": "",
        "output": output,
        "system": system,
    }
    return res


# 制作普通数据集


def construct_dataset_old(prompt, output):
    res = {"instruction": prompt, "input": "", "output": output}
    return res


# 制作 dpo 数据集


def construct_dpo_dataset(prompt, positive_output, negative_output):
    res = {
        "instruction": prompt,
        "input": "",
        "output": [positive_output, negative_output],
    }
    return res
