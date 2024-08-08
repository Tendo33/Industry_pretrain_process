import logging
import os
import json
import re
from tqdm import tqdm
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

# 配置日志记录，设置日志级别为INFO
logging.basicConfig(level=logging.INFO)

# 设置环境变量，指定CUDA可见设备为"0"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# 初始化本地推理模型
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
llm = LLM(model="Qwen1.5-72B-Chat", device_map="auto")  # 可以根据实际情况调整model名称

# 定义问题生成系统的提示信息
QUESTION_SYSTEM_PROMPT = """
# Role: 自然资源行业问题分析师
...
"""

# 定义问题回答系统的提示信息
ANSWER_SYSTEM_PROMPT = """
# Role: 自然资源行业问题回答专家
...
"""


# 解析模型生成的原始响应，提取问题列表
def parse_response(original: str) -> list[str]:
    questions = original.split("\n")
    result = []
    for question in questions:
        question = re.sub(r"[0-9].\s*", "", question)
        if len(question) > 5:
            result.append(question)
    return result


# 将文本分割成指定大小的块
def chunk_text(text: str, chunk_size: int = 4000):
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


# 生成问题提示信息
def make_question_prompt(title: str, text: str) -> str:
    prompt = f"""
    这是《{title}》文件中的一个段落chunk，根据下面的段落文字提取出若干个中文的详细并严谨的问题，名称主语完整无误，不能使用类似“本文件，表2，表A”这类似笼统以及局限的代词。：
    {text}
    """
    return prompt


# 生成回答提示信息
def make_response_prompt(title: str, question: str, text: str) -> str:
    prompt = f"""
    这是《{title}》文件中的一个段落chunk:{text}。
    根据这个段落中的信息严谨地回答下面的问题：
    {question}
    """
    return prompt


def apply_template(sys_prompt: str, user_prompt: str) -> str:
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_prompt},
    ]
    tokenized_chat = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    return tokenized_chat


# 调用模型进行推理
def model_infer(
    system_prompt: str,
    user_prompt: str,
    model_name: str,
    temperature: float = 0.8,
) -> str:
    try:
        sampling_params = SamplingParams(temperature=temperature)
        output = llm.generate([system_prompt + user_prompt], sampling_params)
        return output[0].outputs[0].text.strip()
    except Exception as e:
        logging.error(f"Error during model inference: {e}")
        return ""


# 处理文档，生成问题和回答
def process_document(document: dict, model_name: str):
    text = document.get("content", "")
    title = document.get("title", "")
    chunks = chunk_text(text=text, chunk_size=6000)
    results = []

    for chunk in tqdm(chunks, total=len(chunks), desc="Processing chunks"):
        user_q_prompt = make_question_prompt(title=title, text=chunk)
        question_output = model_infer(
            QUESTION_SYSTEM_PROMPT, user_q_prompt, model_name, temperature=0.8
        )
        if not question_output:
            continue

        output_list = parse_response(question_output)
        for question in tqdm(
            output_list, total=len(output_list), desc="Processing questions"
        ):
            user_a_prompt = make_response_prompt(
                title=title, text=chunk, question=question
            )
            answer_output = model_infer(
                ANSWER_SYSTEM_PROMPT,
                user_a_prompt,
                model_name,
                temperature=0.8,
            )
            temp_dict = {
                "title": title,
                "question": question,
                "answer": answer_output,
            }
            print(temp_dict)
            print("*" * 50)
            results.append(temp_dict)
    return results


# 主函数，处理输入文件并生成输出文件
if __name__ == "__main__":
    MODEL_NAME = "gpt-4o"  # 可以选择性移除
    MODEL_NAME = "Qwen1.5-72B-Chat"
    FILE_PATH = r"/home/sunjinf/github_projet/nature_data/data_after_process/out_standard_test/1content_list_json.jsonl"
    OUT_PATH = r"/home/sunjinf/github_projet/nature_data/data_after_process/out_standard_test/1content_list_json_qa.jsonl"

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as input_file, open(
            OUT_PATH, "a", encoding="utf-8"
        ) as f_out:
            documents = [json.loads(line) for line in input_file]

            for document in tqdm(documents, total=len(documents), desc="Processing"):
                try:
                    results = process_document(document, MODEL_NAME)
                    for result in results:
                        f_out.write(json.dumps(result, ensure_ascii=False) + "\n")
                except Exception as e:
                    logging.error(f"Error processing document: {e}")

    except Exception as e:
        logging.error(f"Error opening files: {e}")
