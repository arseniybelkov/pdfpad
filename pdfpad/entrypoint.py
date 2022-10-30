import argparse
from pathlib import Path

from .interface import parse_pdf, pad


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

    images = parse_pdf(args.path)
    padded_images = pad(images.copy(), args.height, args.width, args.n_pixels)

    if len(padded_images) > 1:
        padded_images[0].save(
            Path(args.path).parent / f"{Path(args.path).stem}_padded.pdf",
            save_all=True,
            append_images=padded_images[1:],
        )
    else:
        padded_images[0].save(
            Path(args.path).parent / f"{Path(args.path).stem}_padded.pdf"
        )
