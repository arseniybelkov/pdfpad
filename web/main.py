from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse

from pdfpad import pdfpad, save_pdf


app = FastAPI()


@app.post("/processfile/")
async def process_file(file: UploadFile, h: int=Form(...), w: int=Form(...), n_pixels: int=Form(...)) -> FileResponse:
    saved_path = save_pdf(pdfpad(await file.read(), h, w, n_pixels), file.filename)
    return FileResponse(saved_path)


@app.get("/")
async def main():
    content = """
        <body>
        <form action="/processfile/" enctype="multipart/form-data" method="post" id="form1">
        
        <label for file>Choose PDF:</label>
        file: <input name="file" type="file" form="form1">
        <br><br>
        
        <label for h>Number of pages in a column:</label>
        h: <input name="h" id="h" type="number" form="form1" placeholder="1" value="1">
        <br><br>
        
        <label for w>Number of pages in a row:</label>
        w: <input name="w" id="w" type="number" form="form1" placeholder="1" value="1">
        <br><br>
        
        <label for n_pixels>Padding Width:</label>
        n_pixels: <input name="n_pixels" id="n_pixels" type="number" form="form1" placeholder="128" value="128">
        <br><br>
        
        <input type="submit">
        </form>
        </body>
    """
    return HTMLResponse(content=content)
