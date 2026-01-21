# PDF Combine Script

This repository contains a simple Python script to combine multiple PDF files into a single PDF document.

## Requirements
- Python 3.10+
- PyPDF2

## Setup
1. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install PyPDF2
   ```

## Usage
Run the script from the command line, specifying the PDF files to combine and the output file name:

```bash
python combine_files.py input1.pdf input2.pdf ... output.pdf
```

- `input1.pdf`, `input2.pdf`, ...: PDF files to combine (in order)
- `output.pdf`: Name of the combined output PDF file

## Example
```bash
python combine_files.py 1058_receipts.pdf another_file.pdf combined.pdf
```

## License
MIT
