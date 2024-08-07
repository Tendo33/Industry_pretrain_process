import os
import dotenv
import subprocess
from gptpdf import parse_pdf

dotenv.load_dotenv()


def test_use_api_key(pdf_path, output_dir, model_name):
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_API_BASE")

    content, image_paths = parse_pdf(
        pdf_path,
        output_dir=output_dir,
        api_key=api_key,
        base_url=base_url,
        model=model_name,
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
    pdf_path = r"/home/sunjinf/github_projet/Industry_pretrain_process/data/test_data/采空区瓦斯流动规律的CFD模拟.pdf"
    output_dir = r"/home/sunjinf/github_projet/Industry_pretrain_process/data/test_data_output/gptpdf_internvl2_20B"
    md_path = os.path.join(output_dir, "output.md")
    json_path = os.path.join(output_dir, "output.json")
    model_name = "gpt-4o"
    model_name = "InternVL2-40B-AWQ"
    test_use_api_key(pdf_path, output_dir, model_name=model_name)
    convert_md_to_json(md_path, json_path)
