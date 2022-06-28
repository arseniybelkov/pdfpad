from setuptools import setup, find_packages

with open('requirements.txt', encoding='utf-8') as file:
    requirements = file.read().splitlines()

setup(
    name='pdfpad',
    version='0.0.1',
    license='MIT',
    url='https://github.com/arseniybelkov/pdfpad',
    install_requires=requirements,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'pdfpad = pdfpad.main:entrypoint',
        ],
    },
)
