import logging
import os
import json
from openai import OpenAI
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

SYSTEM_PROMPT = '''
## Background
你是一个内容分析助手，你的任务是接收用户输入的段落，然后根据段落内容生成一个严谨的问答对。

## Goals
- 读取并分析用户输入的段落。
- 根据段落内容提出若干个相关的问题。
- 从段落中找到并给出相应的回答。
- 按照指定的格式输出结果。

## Skills
- 文本分析
- 信息提取
- 问答对生成

## Constraints
- 确保生成的问答对为中文。
- 确保问题与段落内容紧密相关。
- 生成的问题和回答必须宏观、有价值，脱离段落，不要生成特别细节的问题。
- 生成的问题和回答中要严谨，名称主语完整无误，不能使用类似“本文件，表2，表A”这类似笼统以及局限的代词。
- 回答必须直接来自段落中的信息。
- 如果输入的段落是重复的话，或者整段文字没有意义，或者没有可以提取的问题和回答，则直接返回空字符串。
- 问题和回答为纯文本，不要带任何markdown格式。
- 输出格式必须严格为jsonl格式: {"instruction":"{问题}","output":"{回答}"}\n{"instruction":"{问题2}","output":"{回答2}"}。

## Rules
- 必须使用用户输入的段落来生成若干问答对。
- 问题和回答必须严谨，清晰、准确。
- 输出格式必须严格遵守。

## Workflow
1. 接收用户输入的段落。
2. 分析段落内容，提出若干个相关的问题。
3. 从段落中找到并给出相应的回答。
4. 按照指定的格式输出结果。
'''


def model_infer(system_prompt: str, user_prompt: str, model_name: str, temperature: float = 0.8, frequency_penalty: float = 0.0, presence_penalty: float = 0.0) -> str:
    client = OpenAI(
        api_key="sk-uG93vRV5V2Dog95J15FfCdE5DaAe438fBb17C642F2E1Ae57",
        base_url="http://ai-api.e-tudou.com:9000/v1"
    )
    # 使用OpenAI ChatCompletion API生成聊天响应
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature
    )
    if response.choices[0].message.content:
        output = response.choices[0].message.content.strip()
    return output


def chunk_text(text: str, chunk_size: int = 4000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def make_prompt(text: str) -> str:
    prompt = f'''
    根据下面的段落文字提取出若干个中文的问题对：
    
    {text}
    '''
    return prompt


if __name__ == "__main__":
    MODEL_NAME = "gpt-4o"

    FILE_PATH = r"/share_data/data/nature_data/out_123_text_ori.jsonl"
    OUT_PATH = r"/share_data/data/nature_data/natuer_qa.jsonl"

    with open(FILE_PATH, 'r', encoding='utf-8') as input_file:
        documents = [json.loads(line) for line in input_file]

    with open(OUT_PATH, 'a', encoding='utf-8') as f_out:
        for document in tqdm(documents, total=len(documents), desc="Processing"):
            text = document.get("content", "")
            title = document.get("title", "")
            chunks = chunk_text(text=text, chunk_size=6000)
            for chunk in chunks:
                user_prompt = make_prompt(chunk)
                output = model_infer(
                    SYSTEM_PROMPT, user_prompt, MODEL_NAME, temperature=0.5)
                print(output)

                output_jsonl = output.split('\n')
                for line in output_jsonl:
                    try:
                        json_obj = json.loads(line)
                        f_out.write(json.dumps(
                            json_obj, ensure_ascii=False) + '\n')
                    except json.JSONDecodeError:
                        logging.warning(f"Failed to decode JSON: {line}")
