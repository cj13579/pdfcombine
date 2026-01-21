# PDF Combine Script

![Coverage](./badges/coverage.svg)

This repository contains a simple Python script to combine PDFs and images from a folder into a single PDF document.

## Requirements
- Python 3.10+
- PyPDF2
- Pillow
- Loguru
- Coverage.py
- genbadge (for local badge generation)

## Setup
1. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the script from the command line, specifying the folder to combine and the output file name:

```bash
python combine_files.py --folder /path/to/folder --output output.pdf
```

- `--folder`: Path to the folder containing PDFs and images to combine (sorted by name)
- `--output`: Name of the combined output PDF file (defaults to `combined.pdf`)

If you omit the flags, the script will prompt you for both values.

If your path contains spaces, wrap it in quotes:

```bash
python combine_files.py --folder "/my/path/contains spaces/subdir" --output receipts.pdf
```

## Testing
This project uses Coverage.py to measure test coverage. The configuration enforces a minimum of 90%.
Generate the local badge after running coverage:

```bash
python -m coverage run -m unittest -v
python -m coverage xml
genbadge coverage -i coverage.xml -o badges/coverage.svg
```

The badge is stored in `badges/coverage.svg` and referenced directly in the README.

## Logging
The script uses Loguru for logging. By default it logs at INFO level, including:
- Per-file processing time
- Total run time
- Skipped files (non-files or unsupported types)

## License
MIT
