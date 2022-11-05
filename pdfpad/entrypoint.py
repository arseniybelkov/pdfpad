import argparse
from pathlib import Path

from .interface import pdfpad, save_pdf


def entrypoint():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", type=str, help="Path to a pdf file")
    parser.add_argument(
        "--height", "-hg", type=int, default=3, help="Number of pages in a column"
    )
    parser.add_argument(
        "--width", "-w", type=int, default=3, help="Number of pages in a row"
    )
    parser.add_argument(
        "--n_pixels", "-N", type=int, default=100, help="Number of pixels for padding"
    )
    args = parser.parse_args()

    padded_images = pdfpad(args.path, args.height, args.width, args.n_pixels)
    save_pdf(padded_images, args.path)
