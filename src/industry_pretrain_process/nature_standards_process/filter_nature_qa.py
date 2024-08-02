import os
import json
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
from vllm import LLM, SamplingParams

# os.environ["NCCL_NVLS_ENABLE"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

BATCH_SIZE = 128

# 定义系统提示语
SYSTEM_PROMPT = '''
# Role
问答对鉴定专家

## Profile
- Language: 中文
- Description: 专门用于鉴定问答对是否符合标准的角色，能够判断问题是否清晰、答案是否准确、信息是否完整，并给出相应的合格或不合格判定。

## Knowledges
- 理解并分析jsonl数据格式。
- 判断问答对的宏观性、价值性、信息完整性和困惑度。
- 理解并评估问题的清晰度和答案的准确性。

## Skills
- 分析和评估问答对的质量。
- 逻辑推理能力。
- 精准的判断能力。

## Rules
- 必须基于给定的问答对内容进行评估。
- 给定的问题必须有高的语义清晰度以及具有宏观性、价值性、信息完整性和低的困惑度。
- 给定的答案必须与问题吻合切回答了对应的问题。
- 评估结果必须清晰明确，符合标准则返回数字1，不合格则返回数字0。
- 如果问题或者回答中有“**”或者“##”等脱敏符号导致原本的语义不完整，直接返回数字0。
- 如果问题或者回答中有个人信息比如电话，邮件，网站，私人地址等，直接返回数字0。
- 如果问题中有类似“表1”，“本文件”，“本附件”等含糊的内容，直接返回数字0。

## Workflow
1. 接收用户提供的jsonl格式数据。
2. 分析数据中的"instruction"字段作为问答对的问题，评估问题的语义清晰度和价值性以及困惑度，主谓宾都是确定且不模糊的。
3. 分析数据中的"output"字段作为问答对的答案，评估答案的准确性、信息完整性和困惑度。
4. 根据评估结果，返回数字1（合格）或数字0（不合格）。

## Examples
1. 输入为{"instruction": "土地利用确权的使用期限起始时间是什么时候？", "output": "2008-10-01"}，这里面的问题具有宏观性，困惑度低，所以是一个好问题，这里面的回答也是标准的，没有乱回，所以这个问答对是标准的，应当返回数字1。
2. 输入为{"instruction": "保管的起始时间是什么时候？", "output": "2020-7-01"}，这个问题完全不具有宏观性，因为完全不知道是什么的“保管时间”，困惑度较高，所以这个问答对是不合格的，应当返回数字0。
3.{"instruction": "迁建点名称是什么？", "output": "测试008"}这个问题完全不具有宏观性，因为完全不知道是什么的“迁建点”，困惑度较高，应当返回数字0。
4.{"instruction": "表O.1中，赤潮异弯藻的赤潮基准密度是多少？", "output": "表O.1中，赤潮异弯藻的赤潮基准密度是大于5×10³个/L。"}这个问题完全不具有宏观性，因为完全不知道表0.1是什么，困惑度较高，应当返回数字0。
'''


def apply_template(text: str) -> str:

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text}
    ]
    tokenized_chat = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True)
    return tokenized_chat


def make_user_prompt(text: str) -> str:
    prompt = f"""请对以下问答对进行判定，并根据评估结果，返回数字1（合格）或数字0（不合格）。：
    '''
    {text}
    '''
    """
    return prompt


def process_documents_in_batch(documents, start_index, end_index, llm, sampling_params):

    batch_documents = documents[start_index:end_index]
    # print(batch_documents)
    batch_documents_content = [document
                               for document in batch_documents]  # wiki 数据集的字段是content
    batch_queries = []

    for document in batch_documents_content:

        query_text = make_user_prompt(text=document)
        formatted_query = apply_template(query_text)
        batch_queries.append(formatted_query)

    # 批量生成结果
    generated_outputs = llm.generate(batch_queries, sampling_params)

    result = []
    for i, document in enumerate(batch_documents):
        generated_text = generated_outputs[i].outputs[0].text.strip(
            "\n").strip()
        print(generated_text)
        result.append(generated_text)
        print("*" * 50)

    return result, batch_documents


if __name__ == "__main__":
    # 模型和tokenizer路径
    # MODEL_PATH = r"/workspace/share_data/base_llms/Qwen2-7B-Instruct"
    MODEL_PATH = r"/workspace/share_data/base_llms/Qwen1.5-14B-Chat"
    MODEL_PATH = r"/workspace/share_data/base_llms/Qwen2-72B-Instruct-AWQ"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

    # Sampling参数
    sampling_params = SamplingParams(
        temperature=0.2, top_p=0.95, max_tokens=32000)
    llm = LLM(model=MODEL_PATH, dtype="auto", tensor_parallel_size=1,
              tokenizer_mode="auto", gpu_memory_utilization=0.95, enforce_eager=True)

    # 文件路径
    INPUT_FILE_PATH = r"/workspace/share_data/data/nature_data/nature_qa_123.jsonl"
    OUTPUT_FILE_PATH = r"/workspace/share_data/data/nature_data/nature_qa_123_filter.jsonl"
    # 读取文件内容
    with open(INPUT_FILE_PATH, 'r', encoding='utf-8') as input_file:
        documents = [json.loads(line) for line in input_file]

    # 读取输出路径中已有的内容
    if os.path.exists(OUTPUT_FILE_PATH):
        with open(OUTPUT_FILE_PATH, 'r', encoding='utf-8') as output_file:
            processed_lines = output_file.readlines()
    else:
        processed_lines = []

    total_docs = len(documents)
    for start_index in tqdm(range(0, total_docs, BATCH_SIZE), total=total_docs // BATCH_SIZE, desc="Processing"):
        end_index = min(start_index + BATCH_SIZE, total_docs)
        if start_index < len(processed_lines):
            continue

        # 处理所有批次
        batch_result, batch_documents = process_documents_in_batch(
            documents, start_index, end_index, llm, sampling_params)

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
            with open(OUTPUT_FILE_PATH, 'a', encoding='utf-8') as output_file:
                for document in filtered_documents:
                    output_file.write(json.dumps(
                        document, ensure_ascii=False) + '\n')
