import json
import os
import time
import logging
import subprocess
from openai import OpenAI
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

SYSTEM_PROMPT = '''
# Role
文本提取与错字修复助手

## Profile
- Language: 中文
- Description: 你是一个专门用于从Markdown文件中提取纯文字，并自动修复其中中文错字漏字的助手。

## Knowledges
- Markdown语法
- 中文常见错字漏字

## Skills
- 文本识别提取
- 错字识别与修复

## Constraints
- 忽略图片信息。
- 按照原文意思提取出有用的信息，如果句子不完整或者不通顺，你要使其变得完整。
- 如果表格中有文字内容，你要用完整的语言来描述这个表格内容。如果表格里的数据全是数字，就忽略这个表格。
- 返回的内容中的正文不要带markdown格式，只有标题可以带markdown格式。
- 只输出提取出来的文字，不能输出总结，建议或者任何其他的字段。

## Workflow
1. 用户提供Markdown文件内容。
2. 提取文件中的纯文字和信息。
3. 识别并修复其中的中文错字漏字。
4. 返回修复后的纯文字内容。
'''


def model_infer_curl(system_content: str, user_content: str, model_url: str, temperature: float = 0.9):

    API_URL = "http://ai-api.e-tudou.com:9000/v1/chat/completions"
    API_KEY = "sk-uG93vRV5V2Dog95J15FfCdE5DaAe438fBb17C642F2E1Ae57"
    MODEL_NAME = "qwen-max"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.3
    }

    command = [
        "curl", API_URL,
        "-H", f"Content-Type: {headers['Content-Type']}",
        "-H", f"Authorization: {headers['Authorization']}",
        "-d", json.dumps(payload)
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"API request failed: {result.stderr}")

    response = json.loads(result.stdout)
    print(response)
    return response['choices'][0]['message']['content'].strip()


def model_infer(system_content: str, user_content: str, model_url: str, temperature: float = 0.9, frequency_penalty: float = 0.0, presence_penalty: float = 0.0) -> str:
    client = OpenAI(
        api_key="YOUR_API_KEY",
        base_url=model_url
    )
    model_name = "qwen-max"
    start_time = time.time()

    response = client.chat_completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
        max_tokens=32000,
        temperature=temperature,
        top_p=0.95,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )

    end_time = time.time()
    elapsed_time = end_time - start_time
    output = response.choices[0].message.content.strip()
    generated_speed = len(output) / elapsed_time

    print(f"生成速度：{generated_speed:.2f} 字/秒")
    return output


def construct_query(content: str) -> str:
    prompt = f"下面是一个文字混乱格式混乱的markdown, 从中提取出连续可训练的文字：'''{content}'''"
    return prompt


def split_into_chunks(text: str, chunk_size: int = 4000) -> list:
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def process_markdown_files(input_folder: str, output_file: str, model_url: str):
    results = []
    for subdir, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".md"):
                folder_name = os.path.basename(subdir)
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # 为了准确性和模型上下文长度限制，对内容进行分块处理
                chunks = split_into_chunks(content)
                processed_content = ""
                for chunk in tqdm(chunks, desc=f"Processing {file}"):
                    query = construct_query(chunk)
                    chunk_result = model_infer_curl(
                        SYSTEM_PROMPT, query, model_url)
                    processed_content += chunk_result

                result = {"title": folder_name, "content": processed_content}
                results.append(result)

    with open(output_file, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    input_folder_path = r"/home/sunjinf/github_projet/nature_data/out_first"
    output_file_path = r"/home/sunjinf/github_projet/nature_data/out_first_processed.jsonl"
    model_api_url = "http://ai-api.e-tudou.com:9000/v1"
    process_markdown_files(input_folder_path, output_file_path, model_api_url)
