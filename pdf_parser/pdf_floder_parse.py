import os
import dotenv
import subprocess
from gptpdf import parse_pdf
from tqdm import tqdm
from typing import Tuple, List

# Load environment variables from .env file
dotenv.load_dotenv()


def load_environment_variables() -> Tuple[str, str]:
    """Load API key and base URL from environment variables.

    Returns:
        Tuple[str, str]: API key and base URL.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('OPENAI_API_BASE')
    return api_key, base_url


def create_output_directory(output_dir: str) -> None:
    """Create output directory if it does not exist.

    Args:
        output_dir (str): Path to the output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def process_pdf_file(pdf_path: str, output_dir: str, api_key: str, base_url: str) -> Tuple[str, List[str]]:
    """Process a PDF file and extract content and images.

    Args:
        pdf_path (str): Path to the PDF file.
        output_dir (str): Directory to save the output.
        api_key (str): API key for authentication.
        base_url (str): Base URL for the API.

    Returns:
        Tuple[str, List[str]]: Extracted content and list of image paths.
    """
    content, image_paths = parse_pdf(
        pdf_path,
        output_dir=output_dir,
        api_key=api_key,
        base_url=base_url,
        model='gpt-4o',
        gpt_worker=6
    )
    return content, image_paths


def convert_md_to_json(md_path: str, json_path: str) -> None:
    """Convert a Markdown file to JSON format.

    Args:
        md_path (str): Path to the Markdown file.
        json_path (str): Path to save the JSON output.
    """
    command = f'md_to_json -o "{json_path}" "{md_path}"'
    result = subprocess.run(command, shell=True, check=True,
                            text=True, capture_output=True)
    print(result.stdout)
    print(result.stderr)


def process_pdfs_in_directory(directory: str, api_key: str, base_url: str) -> None:
    """Process all PDF files in a directory.

    Args:
        directory (str): Path to the directory containing PDF files.
        api_key (str): API key for authentication.
        base_url (str): Base URL for the API.
    """
    if not os.path.isdir(directory):
        print(f"Directory '{directory}' does not exist.")
        return

    for filename in tqdm(os.listdir(directory)):
        if filename.endswith('.pdf'):
            filename_without_suffix = os.path.splitext(filename)[0]
            pdf_path = os.path.join(directory, filename)
            # Create a directory based on the PDF file name
            output_dir = os.path.splitext(pdf_path)[0]

            # Check if the output directory already exists
            if os.path.isdir(output_dir):
                print(f"'{output_dir}' already exists. Skipping '{pdf_path}'.")
                continue
            try:
                create_output_directory(output_dir)

                content, image_paths = process_pdf_file(
                    pdf_path, output_dir, api_key, base_url)

                md_path = os.path.join(output_dir, 'output.md')
                json_path = os.path.join(
                    output_dir, f'{filename_without_suffix}.json')

                convert_md_to_json(md_path, json_path)

                print(f"Processed '{pdf_path}':")
                print(content)
                print(image_paths)
                print(f"Output saved to '{output_dir}'\n")
            except Exception as e:
                print(f"Error processing '{pdf_path}': {e}")

def main(pdf_directory: str) -> None:
    """Main function to load environment variables and process PDFs."""
    try:
        api_key, base_url = load_environment_variables()

        print("API Key:", api_key)
        print("Base URL:", base_url)

        process_pdfs_in_directory(pdf_directory, api_key, base_url)
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    pdf_directory = r'/home/sunjinf/github_projet/nature_data/origin_pdf_third'
    main(pdf_directory)
