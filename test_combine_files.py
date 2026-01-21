import argparse
import os
import tempfile
import unittest
from unittest import mock

from loguru import logger
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image

from combine_files import (
    combine_files_to_pdf,
    log_timing,
    normalize_path,
    parse_args,
    run_cli,
)


class CombineFilesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logger.disable("combine_files")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.enable("combine_files")

    def create_pdf(self, path: str) -> None:
        writer = PdfWriter()
        writer.add_blank_page(width=612, height=792)
        with open(path, "wb") as handle:
            writer.write(handle)

    def create_image(self, path: str) -> None:
        image = Image.new("RGB", (200, 200), color=(120, 180, 240))
        image.save(path)

    def create_palette_image(self, path: str) -> None:
        image = Image.new("P", (200, 200))
        image.putpalette([0, 0, 0, 255, 255, 255])
        image.save(path)

    def test_normalize_path_handles_quotes_and_spaces(self):
        raw_path = "  '/tmp/path\\ with\\ spaces'  "
        normalized = normalize_path(raw_path)
        self.assertEqual(normalized, "/tmp/path with spaces")

    def test_log_timing_emits_info(self):
        with mock.patch.object(logger, "info") as info_mock:
            log_timing("timed", 0.0)
            info_mock.assert_called()

    def test_combines_pdfs_and_images(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_one = os.path.join(temp_dir, "a.pdf")
            pdf_two = os.path.join(temp_dir, "b.pdf")
            image_path = os.path.join(temp_dir, "c.png")

            self.create_pdf(pdf_one)
            self.create_pdf(pdf_two)
            self.create_image(image_path)

            output_pdf = os.path.join(temp_dir, "combined.pdf")
            combine_files_to_pdf(temp_dir, output_pdf)

            self.assertTrue(os.path.exists(output_pdf))
            reader = PdfReader(output_pdf)
            self.assertEqual(len(reader.pages), 3)

    def test_skips_non_files_and_unsupported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_one = os.path.join(temp_dir, "a.pdf")
            text_path = os.path.join(temp_dir, "notes.txt")
            subdir = os.path.join(temp_dir, "subdir")

            os.makedirs(subdir)
            self.create_pdf(pdf_one)
            with open(text_path, "w", encoding="utf-8") as handle:
                handle.write("skip me")

            output_pdf = os.path.join(temp_dir, "combined.pdf")
            combine_files_to_pdf(temp_dir, output_pdf)

            reader = PdfReader(output_pdf)
            self.assertEqual(len(reader.pages), 1)

    def test_converts_non_rgb_images(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = os.path.join(temp_dir, "palette.png")
            self.create_palette_image(image_path)

            output_pdf = os.path.join(temp_dir, "combined.pdf")
            combine_files_to_pdf(temp_dir, output_pdf)

            reader = PdfReader(output_pdf)
            self.assertEqual(len(reader.pages), 1)

    def test_run_cli_applies_default_extension(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_one = os.path.join(temp_dir, "a.pdf")
            self.create_pdf(pdf_one)

            output_pdf = os.path.join(temp_dir, "combined")
            args = argparse.Namespace(folder=temp_dir, output=output_pdf)

            run_cli(args)

            self.assertTrue(os.path.exists(output_pdf + ".pdf"))

    def test_run_cli_uses_input_defaults(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_one = os.path.join(temp_dir, "a.pdf")
            self.create_pdf(pdf_one)

            args = argparse.Namespace(folder=None, output=None)
            current_dir = os.getcwd()
            try:
                os.chdir(temp_dir)
                with mock.patch("builtins.input", side_effect=[temp_dir, ""]):
                    run_cli(args)
            finally:
                os.chdir(current_dir)

            self.assertTrue(os.path.exists(os.path.join(temp_dir, "combined.pdf")))

    def test_run_cli_missing_folder_raises(self):
        args = argparse.Namespace(folder="/no/such/folder", output="out.pdf")
        with self.assertRaises(FileNotFoundError):
            run_cli(args)

    def test_parse_args_reads_flags(self):
        with mock.patch("sys.argv", ["combine_files.py", "--folder", "/tmp", "--output", "out.pdf"]):
            args = parse_args()

        self.assertEqual(args.folder, "/tmp")
        self.assertEqual(args.output, "out.pdf")

    def test_image_open_failure_raises(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = os.path.join(temp_dir, "bad.png")
            with open(image_path, "wb") as handle:
                handle.write(b"not an image")

            with mock.patch("combine_files.Image.open", side_effect=OSError("bad image")):
                with self.assertRaises(OSError):
                    combine_files_to_pdf(temp_dir, os.path.join(temp_dir, "out.pdf"))


if __name__ == "__main__":
    unittest.main()
