import os
from fastapi import FastAPI, UploadFile, Request, Response
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


async def process_file(file_path: str):
    print("reading from input...")

    with open(file_path, "r") as i:
        line = i.read()

    length = len(line)

    output_file_path = "/d/bnp_format/output"
    with open(output_file_path, "w") as o:
        x = 0
        y = 300

        while True:
            o.writelines(line[x:y])
            if y != length:
                o.writelines("\n")
                x += 300
                y += 300
            else:
                break

    return output_file_path


@app.post("/upload")
async def uploadfile(file: UploadFile):
    directory = "/d/bnp_format"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = "/d/bnp_format/input"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    output_file_path = await process_file(file_path)
    return FileResponse(
        output_file_path,
        headers={
            "Content-Disposition": "attachment; filename={0}".format(output_file_path)
        },
    )


@app.get("/download/{file_name}")
async def download_file(request: Request, file_name: str):
    file_path = file_name
    return Response(content=open(file_path, "rb").read(), media_type="text/plain")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
