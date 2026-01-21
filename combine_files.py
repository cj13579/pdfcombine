import argparse
import os
import sys
import time
from loguru import logger
from PyPDF2 import PdfMerger
from PIL import Image


def normalize_path(raw_path: str) -> str:
    trimmed = raw_path.strip().strip('"').strip("'")
    unescaped = trimmed.replace("\\ ", " ")
    return os.path.expanduser(unescaped)


def log_timing(label: str, start_time: float) -> None:
    elapsed = time.perf_counter() - start_time
    logger.info("{label} completed in {elapsed:.4f}s", label=label, elapsed=elapsed)


def combine_files_to_pdf(folder_path, output_pdf):
    # Initialize a PdfMerger object
    merger = PdfMerger()
    total_start = time.perf_counter()
    processed_files = 0
    logger.info("Combining files from {folder}", folder=folder_path)

    # Process all files in the folder
    for file_name in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)

        # Skip if not a file
        if not os.path.isfile(file_path):
            logger.debug("Skipping non-file entry: {file_path}", file_path=file_path)
            continue

        file_start = time.perf_counter()

        # If it's a PDF, add it to the merger
        if file_name.lower().endswith('.pdf'):
            logger.info("Appending PDF: {file_path}", file_path=file_path)
            merger.append(file_path)
            processed_files += 1
            log_timing(f"Processed {file_name}", file_start)

        # If it's an image, convert it to PDF and add it
        elif file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')):
            logger.info("Converting image: {file_path}", file_path=file_path)
            try:
                with Image.open(file_path) as img:
                    # Convert image to RGB mode if it's not already
                    if img.mode != 'RGB':
                        img = img.convert('RGB')

                    # Save the image as a temporary PDF
                    temp_pdf_path = file_path + '.temp.pdf'
                    img.save(temp_pdf_path, 'PDF')
                    logger.debug("Temporary PDF created: {temp_pdf}", temp_pdf=temp_pdf_path)

                    # Append the temporary PDF to the merger
                    merger.append(temp_pdf_path)

                # Remove the temporary PDF file
                os.remove(temp_pdf_path)
                logger.debug("Temporary PDF removed: {temp_pdf}", temp_pdf=temp_pdf_path)
                processed_files += 1
                log_timing(f"Processed {file_name}", file_start)
            except Exception:
                logger.exception("Failed to process image: {file_path}", file_path=file_path)
                raise

        else:
            logger.warning("Skipping unsupported file type: {file_path}", file_path=file_path)
            continue

    # Write the combined PDF to the output file
    merger.write(output_pdf)
    merger.close()

    log_timing("PDF merge", total_start)
    logger.info("Processed {count} file(s)", count=processed_files)
    logger.info("Combined PDF saved as: {output}", output=output_pdf)


def run_cli(args: argparse.Namespace) -> None:
    folder_path = args.folder or input("Enter the path to the folder containing files: ")
    output_pdf = args.output or input("Enter the name of the output PDF file: ")

    folder_path = normalize_path(folder_path)
    output_pdf = normalize_path(output_pdf)

    if not output_pdf:
        output_pdf = "combined.pdf"

    if not output_pdf.endswith('.pdf'):
        output_pdf += '.pdf'

    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    combine_files_to_pdf(folder_path, output_pdf)

def parse_args():
    parser = argparse.ArgumentParser(description="Combine PDFs and images from a folder into a single PDF.")
    parser.add_argument("--folder", nargs="?", help="Path to the folder containing files to combine")
    parser.add_argument("--output", nargs="?", help="Output PDF filename (default: combined.pdf)")
    return parser.parse_args()


# Usage example
if __name__ == "__main__":
    args = parse_args()

    logger.remove()
    logger.add(sys.stderr, level="INFO")

    run_cli(args)
