import os
import dotenv
import subprocess
from gptpdf import parse_pdf

dotenv.load_dotenv()


def test_use_api_key(pdf_path, output_dir):
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_API_BASE")

    content, image_paths = parse_pdf(
        pdf_path,
        output_dir=output_dir,
        api_key=api_key,
        base_url=base_url,
        model="xxx",
        gpt_worker=12,
    )

    print(content)
    print(image_paths)


def convert_md_to_json(md_path, json_path):
    command = f'md_to_json -o "{json_path}" "{md_path}"'
    result = subprocess.run(
        command, shell=True, check=True, text=True, capture_output=True
    )
    print(result.stdout)
    print(result.stderr)


if __name__ == "__main__":
    pdf_path = r"/home/sunjinf/github_projet/nature_data/origin_pdf/(GBT 30600-2022)高标准农田建设 通则.pdf"
    output_dir = r"/home/sunjinf/github_projet/nature_data/(GBT 30600-2022)高标准农田建设 通则"
    md_path = os.path.join(output_dir, "output.md")
    json_path = r"/home/sunjinf/github_projet/nature_data/output.json"

    test_use_api_key(pdf_path, output_dir)
    convert_md_to_json(md_path, json_path)
