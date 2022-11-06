from typing import Tuple

import pytest
from PIL import Image

from pdfpad import pad, parse_pdf


@pytest.fixture
def pdf_path_str(pdf_path):
    return str(pdf_path)


@pytest.fixture
def pdf_path_io(pdf_path):
    return open(pdf_path, "r")


@pytest.fixture
def pdf_path_io_b(pdf_path):
    return open(pdf_path, "rb")


def get_shape(image: Image.Image) -> Tuple[int, int]:
    """
    returns: (width, height) of PIL Image
    """
    return image.size


def pad_shape(shape: Tuple[int, int], w: int, h: int) -> Tuple[int, int]:
    return (shape[0] + w, shape[1] + h)


def test_parsing_str(pdf_path_str):
    images = parse_pdf(pdf_path_str)
    padded_images = pad(images.copy(), 2, 2, 128)

    shapes = list(map(get_shape, images))
    pd_shapes = list(map(get_shape, padded_images))

    assert pd_shapes[0] == pad_shape(shapes[0], 128, 128)
    assert pd_shapes[1] == pad_shape(shapes[1], 128, 128)
    assert pd_shapes[2] == pad_shape(shapes[2], 128, 128)
    assert pd_shapes[3] == pad_shape(shapes[3], 128, 128)
    assert pd_shapes[4] == pad_shape(shapes[4], 128, 128)


def test_parsing_io(pdf_path_io):
    with pytest.raises(ValueError) as e:
        images = parse_pdf(pdf_path_io)
    

def test_parsing_io_b(pdf_path_io_b):
    images = parse_pdf(pdf_path_io_b)
    padded_images = pad(images.copy(), 3, 1, 128)

    shapes = list(map(get_shape, images))
    pd_shapes = list(map(get_shape, padded_images))

    assert pd_shapes[0] == pad_shape(shapes[0], 256, 128)
    assert pd_shapes[1] == pad_shape(shapes[1], 256, 0)
    assert pd_shapes[2] == pad_shape(shapes[2], 256, 128)
    assert pd_shapes[3] == pad_shape(shapes[3], 256, 128)
    assert pd_shapes[4] == pad_shape(shapes[4], 256, 0)