import argparse
import math
from io import BufferedReader
from itertools import product as iterproduct
from pathlib import Path
from typing import List, Union

from pdf2image import convert_from_bytes, convert_from_path
from PIL import Image
from tqdm import tqdm


PathLike = Union[str, Path]


def parse_pdf(fp: Union[PathLike, bytes, BufferedReader]) -> List[Image.Image]:
    """
    Read .pdf file and convert it into a list of PIL Images

    Parameters
    ----------
    fp : Union[PathLike, bytes, BufferedReader]
        path to the .pdf document, or bytes
    """
    if isinstance(fp, bytes):
        return convert_from_bytes(fp)
    elif isinstance(fp, BufferedReader):
        content = fp.read()
        if not isinstance(content, bytes):
            content = content.encode()
        return convert_from_bytes(content)
    elif isinstance(fp, (str, Path)):
        return convert_from_path(Path(fp).resolve())
    else:
        raise ValueError(
            f"file must be either a path, or a byte stream, got {type(fp)}"
        )


def pad(images: List[Image.Image], h: int, w: int, n_pixels: int) -> List[Image.Image]:
    """
    Pad each image in the list, according to its position in h x w grid.
    Returns list of padded images.

    Parameters
    ----------
    images : List[PIL.Image.Image]
        images to be padded.
    h : int
        number of images in column.
    w : int
        number of images in row.
    n_pixels : int
        number of pixels to be used as the padding
    """
    n = math.ceil(len(images) / (h * w))
    n = n + 1 if n == 0 else n

    def add_margin(
        image: Image.Image, top: int, bottom: int, right: int, left: int
    ) -> Image.Image:
        width, height = image.size
        new_width = width + right + left
        new_height = height + top + bottom
        result = Image.new(image.mode, (new_width, new_height), (255, 255, 255))
        result.paste(image, (left, top))
        return result

    pad_top = lambda image: add_margin(image, n_pixels, 0, 0, 0)
    pad_bottom = lambda image: add_margin(image, 0, n_pixels, 0, 0)
    pad_right = lambda image: add_margin(image, 0, 0, n_pixels, 0)
    pad_left = lambda image: add_margin(image, 0, 0, 0, n_pixels)
    no_pad = lambda image: image

    check_i = {
        **{0: pad_top, h - 1: pad_bottom},
        **{k: no_pad for k in range(1, h - 1)},
    }
    check_j = {
        **{0: pad_left, w - 1: pad_right},
        **{k: no_pad for k in range(1, w - 1)},
    }

    for k, i, j in tqdm(iterproduct(range(n), range(h), range(w))):
        if len(images) == k * h * w + w * i + j:
            break
        images[k * h * w + w * i + j] = check_i[i](images[k * h * w + w * i + j])
        images[k * h * w + w * i + j] = check_j[j](images[k * h * w + w * i + j])

        if w == 1:
            images[k * h * w + w * i + j] = pad_left(images[k * h * w + w * i + j])
        if h == 1:
            images[k * h * w + w * i + j] = pad_top(images[k * h * w + w * i + j])

    return images


def pdfpad(
    fp: Union[PathLike, bytes, BufferedReader], h: int, w: int, n_pixels: int
) -> List[Image.Image]:
    return pad(parse_pdf(fp), h, w, n_pixels)


def save_pdf(images: List[Image.Image], filepath: PathLike) -> str:
    new_path = Path(filepath).parent / f"{Path(filepath).stem}_padded.pdf"
    if len(images) > 1:
        images[0].save(new_path, save_all=True, append_images=images[1:])
    else:
        images[0].save(new_path)
    return str(new_path)
