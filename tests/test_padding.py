from typing import Tuple

from pdfpad import pad, parse_pdf
from PIL import Image


def get_shape(image: Image.Image) -> Tuple[int, int]:
    """
    returns: (width, height) of PIL Image
    """
    return image.size


def pad_shape(shape: Tuple[int, int], w: int, h: int) -> Tuple[int, int]:
    return (shape[0] + w, shape[1] + h)


def test_padding2x2(pdf_path):
    images = parse_pdf(pdf_path)
    padded_images = pad(images.copy(), 2, 2, 128)

    shapes = list(map(get_shape, images))
    pd_shapes = list(map(get_shape, padded_images))

    assert pd_shapes[0] == pad_shape(shapes[0], 128, 128)
    assert pd_shapes[1] == pad_shape(shapes[1], 128, 128)
    assert pd_shapes[2] == pad_shape(shapes[2], 128, 128)
    assert pd_shapes[3] == pad_shape(shapes[3], 128, 128)
    assert pd_shapes[4] == pad_shape(shapes[4], 128, 128)


def test_padding1x3(pdf_path):
    images = parse_pdf(pdf_path)
    padded_images = pad(images.copy(), 1, 3, 128)

    shapes = list(map(get_shape, images))
    pd_shapes = list(map(get_shape, padded_images))

    assert pd_shapes[0] == pad_shape(shapes[0], 128, 256)
    assert pd_shapes[1] == pad_shape(shapes[1], 0, 256)
    assert pd_shapes[2] == pad_shape(shapes[2], 128, 256)
    assert pd_shapes[3] == pad_shape(shapes[3], 128, 256)
    assert pd_shapes[4] == pad_shape(shapes[4], 0, 256)
    

def test_padding3x1(pdf_path):
    images = parse_pdf(pdf_path)
    padded_images = pad(images.copy(), 3, 1, 128)

    shapes = list(map(get_shape, images))
    pd_shapes = list(map(get_shape, padded_images))

    assert pd_shapes[0] == pad_shape(shapes[0], 256, 128)
    assert pd_shapes[1] == pad_shape(shapes[1], 256, 0)
    assert pd_shapes[2] == pad_shape(shapes[2], 256, 128)
    assert pd_shapes[3] == pad_shape(shapes[3], 256, 128)
    assert pd_shapes[4] == pad_shape(shapes[4], 256, 0)