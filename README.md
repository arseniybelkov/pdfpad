# pdfpad
 
## Installation
In order to install the package execute the following commands:  
```python
pip install pdfpad
```
```bash  
git clone https://github.com/arseniybelkov/pdfpad.git
cd pdfpad  
pip install -e .  
```
OR  
If you have [GitHub CLI](https://cli.github.com/) installed  
```bash  
gh repo clone arseniybelkov/pdfpad
cd pdfpad  
pip install -e .  
```

If you have any error involving `poppler`, please execute  
```bash
sudo apt install poppler-utils
```


## Usage
```bash
pdfpad -p [PATH TO PDF] -hg [number OF PICS IN A COLUMN] -w [number OF PICS IN A ROW] -N [AMOUNT OF PADDING PIXELS]
```
