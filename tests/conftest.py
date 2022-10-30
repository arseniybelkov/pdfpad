from pathlib import Path

import pytest


@pytest.fixture
def tests_root():
    return Path(__file__).resolve().parent


@pytest.fixture
def assets_path(tests_root):
    return tests_root / "assets"


@pytest.fixture
def pdf_path(assets_path):
    return assets_path / "lorem_ipsum.pdf"
