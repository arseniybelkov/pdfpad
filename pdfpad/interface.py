import argparse
import math
from itertools import product as iterproduct
from pathlib import Path
from typing import List, Union

from pdf2image import convert_from_path
from PIL import Image
from tqdm import tqdm


def parse_pdf(path: Union[str, Path]) -> List[Image.Image]:
    """
    Read .pdf file and convert it into a list of PIL Images

    Parameters
    ----------
    path : str, Path
        path to the .pdf document.
    """
    images = convert_from_path(path)
    return images


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
        result = Image.new(image.mode, (new_width, new_height), 0)
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
