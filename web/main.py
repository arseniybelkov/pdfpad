import os

from fastapi import BackgroundTasks, FastAPI, Form, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

from pdfpad import pdfpad, save_pdf


app = FastAPI()


def remove_file(path: str) -> None:
    os.unlink(path)


@app.post("/processfile")
async def process_file(background_tasks: BackgroundTasks, file: UploadFile,
                       h: int=Form(...), w: int=Form(...), n_pixels: int=Form(...)) -> FileResponse:
    saved_path = save_pdf(pdfpad(await file.read(), h, w, n_pixels), file.filename)
    background_tasks.add_task(remove_file, saved_path)
    return FileResponse(saved_path)


@app.get("/")
async def main():
    content = """
        <body>
        <form action="/processfile" enctype="multipart/form-data" method="post" id="form1">

        
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


if __name__ == "__main__":
    import uvicorn
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", type=str, default="127.0.0.1")
    args = parser.parse_args()
    
    uvicorn.run("main:app", host=args.port, port=7575, reload=True)
