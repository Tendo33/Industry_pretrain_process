import logging
import re
import os
import json
from tqdm import tqdm
# from transformers import AutoTokenizer
from lmdeploy import pipeline, GenerationConfig, TurbomindEngineConfig

logging.basicConfig(level=logging.INFO)

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

SYSTEM_PROMPT = '''
# Role
文本提取与错字修复助手

## Profile
- Language: 中文
- Description: 你是一个专门用于从Markdown文件中提取纯文字，并自动修复其中中文错字漏字的助手。

## Knowledges
- Markdown语法
- 中文常见错字漏字
- 文本识别提取
- 错字识别与修复

## Constraints
- 忽略图片信息，不要输出跟图片相关的信息。
- 如果遇到表格信息，用文字对表格进行总结，不要输出markdown中“| |”表格格式。
- 不要编纂内容，只输出跟原文相关的内容。
- 如果原文中的句子出现无意义的重复内容，比如“影像不同影像不同影像不同影像不同”，输出时删除类似的内容。
- 按照原文意思提取出有用的信息，如果句子不完整或者不通顺，你要使其变得完整。
- 返回的内容中的正文不要带markdown格式，只有标题可以带markdown格式。
- 只输出提取出来的文字，不能输出你的总结，建议或者任何其他的字段。
- 不要返回任何提示信息。

## Workflow
1. 用户提供Markdown文件内容。
2. 提取文件中的不带Markdown格式的文字和信息。
3. 识别并修复其中的中文错字漏字使其变为通顺的句子。
4. 只返回修复后的纯文字内容。
'''


def apply_template(text: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text}
    ]
    # tokenized_chat = tokenizer.apply_chat_template(
    #     messages, tokenize=False, add_generation_prompt=True)
    return messages


def construct_query(content: str) -> str:
    prompt = f"下面是一个文字混乱格式混乱的markdown, 从中提取出连续可训练的文字：'''{content}'''"
    return prompt


def split_into_chunks(text: str, chunk_size: int = 4000) -> list:
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def process_markdown_files(input_folder: str, output_file: str):
    for subdir, _, files in os.walk(input_folder):
        for file in files:
            print(output_file)
            if file.endswith(".md"):
                folder_name = os.path.basename(subdir)
                file_path = os.path.join(subdir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    logging.error(f"Failed to read {file_path}: {e}")
                    continue

                chunks = split_into_chunks(content)

                query_for_process_list = []
                for chunk in tqdm(chunks, desc=f"Processing {file}"):
                    query_text = construct_query(chunk)
                    query_for_process = apply_template(query_text)
                    query_for_process_list.append(query_for_process)

                responses = pipe(query_for_process_list, gen_config=gen_config)
                after_llm_list = []
                for response in responses:
                    generated_text = response.text.strip("\n").strip()
                    print(generated_text)
                    after_llm_list.append(generated_text)
                    print("*" * 50)
                processed_content = "".join(after_llm_list)
                result = {"title": folder_name, "content": processed_content}

                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(result, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    # 模型和tokenizer路径
    MODEL_PATH = r"/workspace/share_data/base_llms/Qwen2-72B-Instruct-AWQ"
    # tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

    # lmdeploy 配置
    backend_config = TurbomindEngineConfig(
        tp=1, quant_policy=8, model_format="awq")
    gen_config = GenerationConfig(
        top_p=0.8, top_k=40, temperature=0.4, max_new_tokens=24000)
    pipe = pipeline(MODEL_PATH,
                    backend_config=backend_config)

    INPUT_FOLDER = r"/workspace/share_data/data/nature_data/out_123"
    OUTPUT_FILE = r"/workspace/share_data/data/nature_data/out_123_text_lmd.jsonl"
    process_markdown_files(INPUT_FOLDER, OUTPUT_FILE)
