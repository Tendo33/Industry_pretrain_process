import logging
import os
import json
import re
from openai import OpenAI
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

QUESTION_SYSTEM_PROMPT = """
# Role: 自然资源行业问题分析师
## Profile
- Language: 中文
- Description: 专门负责从自然资源行业的国家标准文件、论文或书籍中提取宏观、有价值的问题，涵盖多个相关话题。

## Knowledges
- 自然资源行业的基本概念和原理
- 国家标准文件、论文或书籍的阅读和分析方法
- 宏观问题的识别和表述技巧

## Skills
- 高效阅读和理解复杂文本
- 提炼关键信息和核心观点
- 生成有深度和广度的问题

## Rules
- 问题必须宏观、有价值，并且涵盖多个相关话题
- 问题表述必须详细且使用严谨的描述风格
- 避免提出过于狭窄或琐碎的问题
- 生成的问题和回答中要严谨，名称主语完整无误，不能使用类似“本文件，表2，表A”这类似笼统以及局限的代词。
- 输出的问题按照“1.xx \n 2.xx ”的格式

## Workflow
1. 用户提供具体的国家标准文件、论文或书籍的片段信息。
2. 分析师阅读并分析文本，识别关键主题和观点。
3. 基于关键主题和观点，分析师生成宏观、有价值且涵盖多个相关话题的问题。
4. 分析师将问题以详细且严谨的描述风格呈现给用户。
"""
ANSWER_SYSTEM_PROMPT = """
# Role: 自然资源行业问题回答专家
## Profile
- Language: 中文
- Description: 专门负责根据给定的自然资源行业的国家标准文件、论文或书籍片段作为知识，根据这些知识回答宏观、有价值且涵盖多个相关话题的问题。

## Knowledges
- 自然资源行业的基本概念和原理
- 国家标准文件、论文或书籍的内容和结构
- 问题回答的逻辑和技巧

## Skills
- 高效阅读和理解复杂文本
- 提炼关键信息和核心观点
- 生成有深度和广度的问题回答

## Rules
- 回答必须基于给定的国家标准文件、论文或书籍
- 回答必须宏观、有价值，并且涵盖多个相关话题
- 回答表述必须详细且使用严谨的描述风格

## Workflow
1. 用户提供具体的国家标准文件、论文或书籍的片段信息。
2. 阅读并分析文本，识别关键主题和观点。
3. 基于关键主题和观点，根据用户给定的问题生成严谨、有价值的回答。
4. 将回答以详细且严谨的描述风格呈现给用户。
"""


# Function to parse responses into questions
def parse_response(original: str) -> list[str]:
    questions = original.split("\n")
    result = []
    for question in questions:
        question = re.sub(r"[0-9].\s*", "", question)
        if len(question) > 5:
            result.append(question)
    return result


def chunk_text(text: str, chunk_size: int = 4000):
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def make_question_prompt(title: str, text: str) -> str:
    prompt = f"""
    这是《{title}》文件中的一个段落chunk，根据下面的段落文字提取出若干个中文的详细并严谨的问题，名称主语完整无误，不能使用类似“本文件，表2，表A”这类似笼统以及局限的代词。：
    {text}
    """
    return prompt


def make_response_prompt(title: str, question: str, text: str) -> str:
    prompt = f"""
    这是《{title}》文件中的一个段落chunk:{text}。
    根据这个段落信息回答下面的问题：
    {question}
    """
    return prompt


def model_infer(
    system_prompt: str,
    user_prompt: str,
    model_name: str,
    temperature: float = 0.8,
) -> str:
    client = OpenAI(
        api_key="sk-uG93vRV5V2Dog95J15FfCdE5DaAe438fBb17C642F2E1Ae57",
        base_url="http://ai-api.e-tudou.com:9000/v1",
    )
    # 使用OpenAI ChatCompletion API生成聊天响应
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
    )
    output = ""
    if response.choices[0].message.content:
        output = response.choices[0].message.content.strip()
    return output


if __name__ == "__main__":
    MODEL_NAME = "gpt-4o"

    FILE_PATH = r"/share_data/data/nature_data/out_4_text_ori.jsonl"
    OUT_PATH = r"/share_data/data/nature_data/nature_qa_4.jsonl"

    with open(FILE_PATH, "r", encoding="utf-8") as input_file:
        documents = [json.loads(line) for line in input_file]

    with open(OUT_PATH, "a", encoding="utf-8") as f_out:
        for document in tqdm(documents, total=len(documents), desc="Processing"):
            text = document.get("content", "")
            title = document.get("title", "")
            chunks = chunk_text(text=text, chunk_size=6000)
            for chunk in chunks:
                user_q_prompt = make_question_prompt(title=title, text=chunk)
                question_output = model_infer(
                    QUESTION_SYSTEM_PROMPT, user_q_prompt, MODEL_NAME, temperature=0.8
                )
                print(question_output)

                output_list = parse_response(question_output)
                for question in output_list:
                    user_a_prompt = make_response_prompt(
                        title=title, text=chunk, question=question
                    )
                    answer_output = model_infer(
                        ANSWER_SYSTEM_PROMPT,
                        user_a_prompt,
                        MODEL_NAME,
                        temperature=0.8,
                    )
                    temp_dict = {
                        "title": title,
                        "question": question,
                        "answer": answer_output,
                    }

                    if temp_dict:
                        print(temp_dict)
                        f_out.write(json.dumps(temp_dict, ensure_ascii=False) + "\n")
