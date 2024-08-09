import logging
import os
import json
import re
from tqdm import tqdm
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

# 配置日志记录，设置日志级别为INFO
logging.basicConfig(level=logging.INFO)

# 设置环境变量，指定CUDA可见设备为"2"
os.environ["CUDA_VISIBLE_DEVICES"] = "2"


# 定义问题生成系统的提示信息
QUESTION_SYSTEM_PROMPT = """
# Role: 自然资源行业问题分析师
## Profile
- Language: 简体中文
- Description: 专门负责从自然资源行业的国家标准文件、论文或书籍中提取宏观、有价值的问题，涵盖多个相关话题。

## Knowledges
- 自然资源行业的基本概念和原理。
- 国家标准文件、论文或书籍的阅读和分析方法。
- 宏观问题的识别和表述技巧。

## Skills
- 高效阅读和理解复杂文本。
- 提炼关键信息和核心观点。
- 生成宏观有深度和广度的问题。

## Rules
- 问题必须宏观、有价值，并且涵盖多个相关话题。
- 问题不要带任何格式，必须为纯文本。
- 避免提出过于狭窄或琐碎的问题。
- 避免文中不是正文的信息（出版时间，参考内容，附件，出版社）成为问题。
- 不要根据给定段落中的狭义信息提问，问题必须宏观，普世，困惑度低。
- 生成的问题要严谨，名称主语完整无误，不能使用类似“本标准，本文件，表2，表A，附录”这类似笼统以及局限的代词。
- 输出的问题按照“1.xx\n2.xx”的格式。

## Workflow
1. 用户提供具体的国家标准文件、论文或书籍的片段信息。
2. 分析师阅读并分析文本，识别关键主题和观点。
3. 基于关键主题和观点，分析师生成宏观、有价值且涵盖多个相关话题的问题。
4. 将生成的问题以详细且严谨的描述风格呈现给用户。
"""

# 定义问题回答系统的提示信息
ANSWER_SYSTEM_PROMPT = """
# Role: 自然资源行业问题回答专家
## Profile
- Language: 简体中文
- Description: 专门负责根据给定的自然资源行业的国家标准文件、论文或书籍片段作为知识，根据这些知识回答用户提出的问题。

## Knowledges
- 自然资源行业的基本概念和原理。
- 国家标准文件、论文或书籍的内容和结构。
- 问题回答的逻辑和技巧。

## Skills
- 高效阅读和理解复杂文本。
- 生成有深度和广度的问题回答。

## Rules
- 回答必须基于给定的国家标准文件、论文或书籍。
- 回答必须宏观、有价值，并且涵盖多个相关话题。
- 回答表述必须详细且使用严谨的描述风格。
- 如果给定的信息不能满足回答问题的要求，或者此片段与问题无关，你可以选择不参考并直接进行回答。

## Workflow
1. 用户提供具体的国家标准文件、论文或书籍的片段信息。
2. 阅读并分析文本，识别关键主题和信息。
3. 基于关键主题和信息，根据用户给定的问题生成严谨、有价值的回答。
"""
# 检查文档是否已经处理过
def is_document_processed(title, output_file_path):
    if not os.path.exists(output_file_path):
        return False

    with open(output_file_path, "r", encoding="utf-8") as f_out:
        for line in f_out:
            if json.loads(line).get("title") == title:
                return True
    return False


# 解析模型生成的原始响应，提取问题列表
def parse_response(original: str) -> list[str]:
    questions = original.split("\n")
    result = []
    for question in questions:
        question = re.sub(r"[0-9].\s*", "", question)
        if len(question) > 5:
            result.append(question.strip(".").strip())
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
def process_document(document: dict):
    text = document.get("content", "")
    title = document.get("title", "")
    chunks = chunk_text(text=text, chunk_size=4000)
    results = []

    for chunk in tqdm(chunks, total=len(chunks), desc="Processing chunks"):
        user_q_prompt = make_question_prompt(title=title, text=chunk)
        query_for_process = apply_template(QUESTION_SYSTEM_PROMPT, user_q_prompt)
        generated_outputs = llm.generate(query_for_process, sampling_params_q)
        generated_question = generated_outputs[0].outputs[0].text.strip("\n").strip()
        if not generated_question:
            continue
        output_q_list = parse_response(generated_question)
        question_answ_list = []
        for question in output_q_list:
            user_a_prompt = make_response_prompt(
                title=title, text=chunk, question=question
            )
            query_r_for_process = apply_template(ANSWER_SYSTEM_PROMPT, user_a_prompt)
            question_answ_list.append(query_r_for_process)
        generated_a_outputs = llm.generate(question_answ_list, sampling_params_a)

        output_a_list = []
        for i, document in enumerate(generated_a_outputs):
            generated_text = generated_a_outputs[i].outputs[0].text.strip("\n").strip()
            output_a_list.append(generated_text)
        for q, a in zip(output_q_list, output_a_list):
            temp_dict = {
                "title": title,
                "question": q,
                "answer": a,
            }
            print(temp_dict)
            print("*" * 50)
            results.append(temp_dict)
    return results


# 主函数，处理输入文件并生成输出文件
if __name__ == "__main__":
    # 模型和tokenizer路径
    MODEL_PATH = r"/workspace/share_data/base_llms/Qwen2-72B-Instruct-AWQ"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

    # Sampling参数
    sampling_params_q = SamplingParams(temperature=0.4, top_p=0.95, max_tokens=12000)
    sampling_params_a = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=30000)
    llm = LLM(
        model=MODEL_PATH,
        dtype="auto",
        quantization="awq",
        tensor_parallel_size=1,
        tokenizer_mode="auto",
        gpu_memory_utilization=0.95,
        enforce_eager=True,
    )
    FILE_PATH = (
        r"/workspace/sunjinfeng/github_projet/data/nature_data/1content_list_json.jsonl"
    )
    OUT_PATH = r"/workspace/sunjinfeng/github_projet/data/nature_data/1content_list_json_qa_vllm.jsonl"

    with open(FILE_PATH, "r", encoding="utf-8") as input_file:
        documents = [json.loads(line) for line in input_file]

    with open(OUT_PATH, "a", encoding="utf-8") as f_out:
        for document in tqdm(
            documents, total=len(documents), desc="Processing Documents"
        ):
            title = document.get("title", "")
            if is_document_processed(title, OUT_PATH):
                logging.info(
                    f"Document with title '{title}' already processed. Skipping."
                )
                continue
            try:
                results = process_document(document)
                if not results:
                    logging.warning(
                        f"No results found for document with title '{title}'"
                    )
                    continue
                if isinstance(results, list):
                    for result in results:
                        f_out.write(json.dumps(result, ensure_ascii=False) + "\n")
                else:
                    continue
            except Exception as e:
                logging.error(f"Error processing document: {e}")
