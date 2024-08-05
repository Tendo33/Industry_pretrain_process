import re
import os
import json
from tqdm import tqdm
from transformers import AutoTokenizer
from lmdeploy import pipeline, GenerationConfig, TurbomindEngineConfig

# os.environ["NCCL_NVLS_ENABLE"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "2"

BATCH_SIZE = 68

# 定义系统提示语
SYSTEM_PROMPT = """
# Role
自然资源领域鉴定助手

## Profile
- Language: 中文
- Description: 这个角色专门用于鉴定用户输入的内容是否属于自然资源领域。

## Knowledges
- 自然资源的基本概念，包括水资源、土地资源、矿产资源、森林资源、野生动植物资源、环境、资源利用等。
- 任何与自然资源相关的术语和关键词。

## Skills
- 文本分析能力
- 关键词匹配技巧

## Rules
- 必须基于用户输入的内容进行鉴定。
- 如果用户输入的内容与自然资源相关，返回数字“1”。
- 如果用户输入的内容与自然资源不相关，返回数字“0”。
- 除了数字“1”或者“0”，不得输出其他文字。

## Workflow
1. 接收用户输入的文本。
2. 分析文本内容，查找与自然资源相关的关键词和概念。
3. 仔细思考然后判断用户输入的内容是否与自然资源相关。
4. 如果用户输入的内容符合自然资源领域，返回数字“1”否则返回数字“0”。
"""

SYSTEM_PROMPT_PRO = """
# Role
自然资源领域严格鉴定助手

## Profile
- Language: 中文
- Description: 这个角色专门用于严格鉴定用户输入的内容是否属于自然资源领域。

## Knowledges
- 自然资源的基本概念，包括水资源、土地资源、矿产资源、森林资源、野生动植物资源、环境、资源利用，土地林、水资源、草原、湿地、荒漠等。
- 任何与自然资源相关的术语和关键词。

## Skills
- 文本分析能力
- 关键词匹配技巧

## Rules
- 必须基于用户输入的内容进行鉴定。
- 如果用户输入的内容与自然资源领域重合达到百分之90，返回数字“1”。
- 任何的人物信息和事件均不属于自然资源领域，直接返回数字“0”。
- 如果用户输入的内容有一点与自然资源不相关，返回数字“0”。
- 除了数字“1”或者“0”，不得输出其他文字。

## Workflow
1. 接收用户输入的文本。
2. 分析文本内容，查找与自然资源相关的关键词和概念。
3. 仔细思考然后严格判断用户输入的内容是否与自然资源相关。
4. 如果你认为跟自然资源领域的重合度大于百分之90，则返回数字“1”否则返回数字“0”。
"""


def apply_template(text: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_PRO},
        {"role": "user", "content": text},
    ]
    # tokenized_chat = tokenizer.apply_chat_template(
    #     messages, tokenize=False, add_generation_prompt=True)
    return messages


def make_user_prompt(text: str) -> str:
    prompt = f"""请鉴定以下内容：
    '''
    {text}
    '''
    """
    return prompt


def process_documents_in_batch(
    documents, start_index, end_index, pipe, gen_config
):
    batch_documents = documents[start_index:end_index]
    # batch_documents = [document["text"]
    #                   for document in batch_documents]  # 智源数据集的字段是text
    batch_documents_content = [
        document["content"] for document in batch_documents
    ]  # wiki 数据集的字段是content
    batch_queries = []

    for document in batch_documents_content:
        query_text = make_user_prompt(text=document)
        formatted_query = apply_template(query_text)
        batch_queries.append(formatted_query)

    # 批量生成结果
    generated_outputs = pipe(batch_queries, gen_config=gen_config)

    result = []
    for i, document in enumerate(batch_documents_content):
        generated_text = generated_outputs[i].text.strip("\n").strip()
        print(generated_text)
        result.append(generated_text)
        print("*" * 50)

    return result, batch_documents


if __name__ == "__main__":
    # 模型和tokenizer路径
    MODEL_PATH = r"/workspace/share_data/base_llms/Qwen2-72B-Instruct-AWQ"
    # MODEL_PATH = r"/workspace/share_data/base_llms/Qwen2-7B-Instruct"
    # tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

    # Sampling参数
    backend_config = TurbomindEngineConfig(
        tp=1,
        quant_policy=8,
        model_format="awq",
        max_batch_size=256,
        cache_max_entry_count=0.9,
        enable_prefix_caching=True,
    )
    gen_config = GenerationConfig(
        top_p=0.8, top_k=40, temperature=0.5, max_new_tokens=32000
    )
    pipe = pipeline(MODEL_PATH, backend_config=backend_config)

    # 文件路径
    INPUT_FILE_PATH = (
        r"/workspace/share_data/data/pretrain_data/wiki_filter_all_new.jsonl"
    )
    OUTPUT_FILE_PATH = (
        r"/workspace/share_data/data/pretrain_data/wiki_nature_all.jsonl"
    )
    # 读取文件内容
    with open(INPUT_FILE_PATH, "r", encoding="utf-8") as input_file:
        input_documents = [json.loads(line) for line in input_file]

    # 读取输出路径中已有的内容
    if os.path.exists(OUTPUT_FILE_PATH):
        with open(OUTPUT_FILE_PATH, "r", encoding="utf-8") as output_file:
            processed_lines = output_file.readlines()
    else:
        processed_lines = []

    total_docs = len(input_documents)
    for start_index in tqdm(
        range(0, total_docs, BATCH_SIZE),
        total=total_docs // BATCH_SIZE,
        desc="Processing",
    ):
        end_index = min(start_index + BATCH_SIZE, total_docs)
        if start_index < len(processed_lines):
            continue

        # 处理所有批次
        batch_result, batch_documents = process_documents_in_batch(
            input_documents, start_index, end_index, pipe, gen_config
        )

        filtered_documents = []
        # 筛选出包含数字1的文档
        for res, document in zip(batch_result, batch_documents):
            if "1" in res and "0" not in res:
                filtered_documents.append(document)

        if len(filtered_documents) == 0:
            continue
        else:
            print(f"{len(filtered_documents)} documents are filtered.")
            # 将筛选出的文档写入文件
            with open(OUTPUT_FILE_PATH, "a", encoding="utf-8") as output_file:
                for document in filtered_documents:
                    output_file.write(
                        json.dumps(document, ensure_ascii=False) + "\n"
                    )
