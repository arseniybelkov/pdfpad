from setuptools import setup, find_packages
from pathlib import Path
import runpy


with open("requirements.txt", encoding="utf-8") as file:
    requirements = file.read().splitlines()

with open("README.md", encoding="utf-8") as file:
    long_description = file.read()

root = Path(__file__).resolve().parent
folder = root / "pdfpad"
version = runpy.run_path(folder / "__version__.py")["__version__"]

setup(
    name="pdfpad",
    version=version,
    license="MIT",
    url="https://github.com/arseniybelkov/pdfpad",
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "pdfpad = pdfpad.entrypoint:entrypoint",
        ],
    },
)
