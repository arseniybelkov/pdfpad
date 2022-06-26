import math
import argparse
from PIL import Image
from tqdm import tqdm
from pathlib import Path
from pdf2image import convert_from_path
from itertools import product as iterproduct


def parse_pdf(path: str) -> list:
    images = convert_from_path(path)
    return images


def pad(images: list, h: int, w: int, n_pixels: int) -> list:
    n = math.ceil(len(images) / (h * w))
    n = n + 1 if n == 0 else n
    
    def add_margin(image: Image, top: int, bottom: int, right: int, left: int) -> Image:
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
    
    check_i = {**{0: pad_top, h - 1: pad_bottom}, **{k: no_pad for k in range(1, h-1)}}
    check_j = {**{0: pad_left, w - 1: pad_right}, **{k: no_pad for k in range(1, w-1)}}
    
    for k, i, j in tqdm(iterproduct(range(n), range(h), range(w))):
        if len(images) == k*h*w + w*i + j:
            break
        images[k*h*w + w*i + j] = check_i[i](images[k*h*w + w*i + j])
        images[k*h*w + w*i + j] = check_j[j](images[k*h*w + w*i + j])
        
    return images
    

def entrypoint():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', type=str, help='Path to a pdf file')
    parser.add_argument('--height', '-hg', type=int, default=3, help='Number of pages in a column')
    parser.add_argument('--width', '-w', type=int, default=3, help='Number of pages in a row')
    parser.add_argument('--n_pixels', '-N', type=int, default=256, help='Number of pixels for padding')
    args = parser.parse_args()
    
    images = parse_pdf(args.path)
    padded_images = pad(images.copy(), args.height, args.width, args.n_pixels)
    
    images[0].save(Path(args.path).parent / f'{Path(args.path).stem}_padded.pdf', save_all=True, append_images=padded_images)