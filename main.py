import os
from fastapi import FastAPI, UploadFile, Request, Response
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
async def uploadfile(file: UploadFile, request: Request):
    directory = "/d/bnp_format"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = "/d/bnp_format/input"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    output_file_path = await process_file(file_path)
    if not os.path.exists(output_file_path):
        return Response(status_code=500, content="Error processing file")
    return templates.TemplateResponse(
        "download.html", {"request": request, "file_name": output_file_path}
    )


@app.get("/download/{file_name}")
async def download_file(request: Request, file_name: str):
    file_path = file_name
    print("paaath")
    print(file_path)
    return Response(content=open(file_path, "rb").read(), media_type="text/plain")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
