import os
from PyPDF2 import PdfMerger
from PIL import Image

def combine_files_to_pdf(folder_path, output_pdf):
    # Initialize a PdfMerger object
    merger = PdfMerger()

    # Process all files in the folder
    for file_name in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)

        # Skip if not a file
        if not os.path.isfile(file_path):
            continue

        # If it's a PDF, add it to the merger
        if file_name.lower().endswith('.pdf'):
            merger.append(file_path)

        # If it's an image, convert it to PDF and add it
        elif file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')):
            with Image.open(file_path) as img:
                # Convert image to RGB mode if it's not already
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Save the image as a temporary PDF
                temp_pdf_path = file_path + '.temp.pdf'
                img.save(temp_pdf_path, 'PDF')

                # Append the temporary PDF to the merger
                merger.append(temp_pdf_path)

                # Remove the temporary PDF file
                os.remove(temp_pdf_path)

    # Write the combined PDF to the output file
    merger.write(output_pdf)
    merger.close()

    print(f"Combined PDF saved as: {output_pdf}")

# Usage example
if __name__ == "__main__":
    folder_path = input("Enter the path to the folder containing files: ").strip()
    output_pdf = input("Enter the name of the output PDF file: ").strip()

    if not output_pdf.endswith('.pdf'):
        output_pdf += '.pdf'

    combine_files_to_pdf(folder_path, output_pdf)
