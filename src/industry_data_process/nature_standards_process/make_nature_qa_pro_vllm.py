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

# 定义生成问题系统的提示信息
SYSTEM_PROMPT_QUESTION_GENERATION = """
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

# 定义生成回答系统的提示信息
SYSTEM_PROMPT_ANSWER_GENERATION = """
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

# 定义释放GPU显存的函数
def release_gpu_memory(llm):
    """
    释放GPU显存，防止内存泄漏
    """
    import gc
    import torch
    from vllm.distributed.parallel_state import (
        destroy_model_parallel,
        destroy_distributed_environment,
    )

    destroy_model_parallel()
    destroy_distributed_environment()
    del llm.llm_engine.model_executor.driver_worker
    del llm.llm_engine.model_executor
    del llm
    gc.collect()
    torch.cuda.empty_cache()
    print(f"cuda memory: {torch.cuda.memory_allocated() // 1024 // 1024}MB")
# 检查文档是否已经处理过
def is_document_processed(document_title, output_file_path):
    if not os.path.exists(output_file_path):
        return False

    with open(output_file_path, "r", encoding="utf-8") as output_file:
        for line in output_file:
            if json.loads(line).get("title") == document_title:
                return True
    return False


# 解析模型生成的原始响应，提取问题列表
def parse_questions_from_response(model_response: str) -> list[str]:
    questions = model_response.split("\n")
    extracted_questions = [
        re.sub(r"[0-9].\s*", "", question).strip(".").strip()
        for question in questions
        if len(question) > 5
    ]
    return extracted_questions


# 将文本分割成指定大小的块
def chunk_text(text_content: str, max_chunk_size: int = 4000):
    return [
        text_content[i : i + max_chunk_size]
        for i in range(0, len(text_content), max_chunk_size)
    ]


# 生成问题的提示信息
def create_question_prompt(document_title: str, text_chunk: str) -> str:
    prompt = f"""
    这是《{document_title}》文件中的一个段落，根据下面的段落文字提取出若干个中文的详细并严谨的问题，名称主语完整无误，不能使用类似“本文件，表2，表A”这类似笼统以及局限的代词：
    {text_chunk}
    """
    return prompt


# 生成回答的提示信息
def create_answer_prompt(document_title: str, question: str, text_chunk: str) -> str:
    prompt = f"""
    这是《{document_title}》文件中的一个段落:{text_chunk}。
    根据这个段落中的信息严谨地回答下面的问题：
    {question}
    """
    return prompt


# 将系统提示和用户提示应用于模板
def format_template(system_prompt: str, user_prompt: str) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    formatted_chat = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    return formatted_chat


# 处理文档，生成问题和回答
def process_document_data(document_data: dict):
    document_text = document_data.get("content", "")
    document_title = document_data.get("title", "")
    text_chunks = chunk_text(text_content=document_text, max_chunk_size=4000)
    processed_results = []

    for text_chunk in tqdm(
        text_chunks, total=len(text_chunks), desc="Processing chunks"
    ):
        question_prompt = create_question_prompt(
            document_title=document_title, text_chunk=text_chunk
        )
        formatted_question = format_template(
            SYSTEM_PROMPT_QUESTION_GENERATION, question_prompt
        )
        question_outputs = llm.generate(formatted_question, sampling_params_question)
        extracted_questions = question_outputs[0].outputs[0].text.strip("\n").strip()

        if not extracted_questions:
            continue

        parsed_questions = parse_questions_from_response(extracted_questions)
        question_answer_prompts = []

        for question in parsed_questions:
            answer_prompt = create_answer_prompt(
                document_title=document_title, text_chunk=text_chunk, question=question
            )
            formatted_answer = format_template(
                SYSTEM_PROMPT_ANSWER_GENERATION, answer_prompt
            )
            question_answer_prompts.append(formatted_answer)

        # 按照每个chunk最多包含5个prompt的大小进行分块
        chunk_size = 5
        for i in range(0, len(question_answer_prompts), chunk_size):
            prompt_chunk = question_answer_prompts[i : i + chunk_size]
            answer_outputs = llm.generate(prompt_chunk, sampling_params_answer)
            generated_answers = []

            for output in answer_outputs:
                generated_text = output.outputs[0].text.strip("\n").strip()
                generated_answers.append(generated_text)

            for question, answer in zip(
                parsed_questions[i : i + chunk_size], generated_answers
            ):
                result_entry = {
                    "title": document_title,
                    "question": question,
                    "answer": answer,
                }
                print(result_entry)
                print("*" * 50)
                processed_results.append(result_entry)

    return processed_results


# 主函数，处理输入文件并生成输出文件
if __name__ == "__main__":
    # 模型和tokenizer路径
    MODEL_DIRECTORY = r"/workspace/share_data/base_llms/Qwen2-72B-Instruct-AWQ"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIRECTORY)

    # Sampling参数
    sampling_params_question = SamplingParams(
        temperature=0.4, top_p=0.9, max_tokens=12000
    )
    sampling_params_answer = SamplingParams(
        temperature=0.7, top_p=0.9, max_tokens=30000
    )
    llm = LLM(
        model=MODEL_DIRECTORY,
        dtype="auto",
        quantization="awq",
        tensor_parallel_size=1,
        tokenizer_mode="auto",
        gpu_memory_utilization=0.95,
        enforce_eager=True,
    )
    INPUT_FILE_PATH = r"/workspace/sunjinfeng/github_projet/data/nature_data/paper_mineru_ocr_out.jsonl"
    OUTPUT_FILE_PATH = (
        r"/workspace/sunjinfeng/github_projet/data/nature_data/paper_sft_qa.jsonl"
    )

    with open(INPUT_FILE_PATH, "r", encoding="utf-8") as input_file:
        documents = [json.loads(line) for line in input_file]

    with open(OUTPUT_FILE_PATH, "a", encoding="utf-8") as output_file:
        for document_data in tqdm(
            documents, total=len(documents), desc="Processing Documents"
        ):
            document_title = document_data.get("title", "")
            if is_document_processed(document_title, OUTPUT_FILE_PATH):
                logging.info(
                    f"Document with title '{document_title}' already processed. Skipping."
                )
                continue
            try:
                results = process_document_data(document_data)
                if not results or not isinstance(results, list):
                    logging.warning(
                        f"No results found for document with title '{document_title}'."
                    )
                    continue
                for result_entry in results:
                    output_file.write(
                        json.dumps(result_entry, ensure_ascii=False) + "\n"
                    )
            except Exception as e:
                logging.error(
                    f"Failed to process document with title '{document_title}': {e}"
                )
