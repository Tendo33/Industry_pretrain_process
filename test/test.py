import os
import dotenv
import subprocess
from gptpdf import parse_pdf

dotenv.load_dotenv()


def test_use_api_key(pdf_path, output_dir):
    api_key = os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('OPENAI_API_BASE')

    content, image_paths = parse_pdf(
        pdf_path, output_dir=output_dir, api_key=api_key, base_url=base_url, model='gpt-4o', gpt_worker=12)

    print(content)
    print(image_paths)


def convert_md_to_json(md_path, json_path):
    command = f'md_to_json -o "{json_path}" "{md_path}"'
    result = subprocess.run(command, shell=True, check=True,
                            text=True, capture_output=True)
    print(result.stdout)
    print(result.stderr)


if __name__ == '__main__':
    pdf_path = '/home/sunjinf/github_projet/nature_data/文档/CH31-00 测绘地理信息通用/202x全球基本比例尺地图分幅和编号（征求意见稿）.pdf'
    output_dir = '/home/sunjinf/github_projet/gptpdf/test/CH31-00 测绘地理信息通用/202x全球基本比例尺地图分幅和编号（征求意见稿）'
    md_path = os.path.join(output_dir, 'output.md')
    json_path = '/home/sunjinf/github_projet/gptpdf/examples/output.json'

    test_use_api_key(pdf_path, output_dir)
    convert_md_to_json(md_path, json_path)
