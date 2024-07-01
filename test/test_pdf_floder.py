import os
import dotenv
from gptpdf import parse_pdf

# Load environment variables from .env file
dotenv.load_dotenv()


def load_environment_variables():
    api_key = os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('OPENAI_API_BASE')
    return api_key, base_url


def create_output_directory(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def process_pdf_file(pdf_path, output_dir, api_key, base_url):
    content, image_paths = parse_pdf(
        pdf_path,
        output_dir=output_dir,
        api_key=api_key,
        base_url=base_url,
        model='gpt-4o',
        gpt_worker=6
    )
    return content, image_paths


def process_pdfs_in_directory(directory, api_key, base_url):
    # Check if the directory exists
    if not os.path.isdir(directory):
        print(f"Directory '{directory}' does not exist.")
        return

    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(directory, filename)
            # Create a directory based on the PDF file name
            output_dir = os.path.splitext(pdf_path)[0]

            create_output_directory(output_dir)

            # Process the PDF file
            content, image_paths = process_pdf_file(
                pdf_path, output_dir, api_key, base_url)

            print(f"Processed '{pdf_path}':")
            print(content)
            print(image_paths)
            print(f"Output saved to '{output_dir}'\n")


def main():
    try:
        api_key, base_url = load_environment_variables()

        print("API Key:", api_key)
        print("Base URL:", base_url)

        # Specify the directory containing the PDF files
        pdf_directory = '../examples/'

        # Process all PDFs in the directory
        process_pdfs_in_directory(pdf_directory, api_key, base_url)
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()
