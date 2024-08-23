import json


def process_conversation(conversation: list[dict]) -> dict:
    instruction = None
    output = None

    # 遍历conversation中的每个字典，找出对应的human和gpt的内容
    for entry in conversation:
        if entry["from"] == "human":
            instruction = entry["value"]
        elif entry["from"] == "gpt":
            output = entry["value"]

    # 返回转换后的格式
    return {"instruction": instruction, "input": "", "output": output}


def convert_jsonl_to_instruction_output(jsonl_file, output_file):
    with open(jsonl_file, "r", encoding="utf-8") as infile, open(
        output_file, "w", encoding="utf-8"
    ) as outfile:
        for line in infile:
            data = json.loads(line.strip())
            conversation = data.get("conversations", [])

            # 处理每条conversation并转换格式
            result = process_conversation(conversation)

            # 将结果写入新的jsonl文件
            outfile.write(json.dumps(result, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    # jsonl_file = "/data/nfs/data/Magpie-Llama-3.1-Pro-300K-Filtered-jsonl/Magpie-Llama-3.1-Pro-300K-all-filter.jsonl"  # 输入文件名
    # output_file = "/home/sunjinf/github_projet/nature_data/sft_data/magpie_en_dataset.jsonl"  # 输出文件名
    jsonl_file = "/data/nfs/data/Magpie-Qwen2-Pro-200K-Chinese-jsonl/Magpie-Qwen2-Pro-200K-Chinese-all-filter.jsonl"  # 输入文件名
    output_file = "/home/sunjinf/github_projet/nature_data/sft_data/magpie_zh_dataset.jsonl"  # 输出文件名
    convert_jsonl_to_instruction_output(jsonl_file, output_file)
