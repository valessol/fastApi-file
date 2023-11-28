from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_files(files: Annotated[list[bytes], File()]):
    print(files)
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    print(files)
    # return {"filenames": [file.filename for file in files]}
    return redirect('/')

async def read_file(file: UploadFile):
    return await file.read()

@app.get("/")
async def main():
    content = f'
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<button type="button" onclick="()">Download</button>
</body>
    '
    return HTMLResponse(content=content)
