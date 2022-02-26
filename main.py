from fastapi import FastAPI, UploadFile, File, status
import shutil
from typing import List
import uvicorn as server
import pynguinAPI
from utils import *


app = FastAPI()

@app.get("/")
def index():
    return {"msg": "Welcome to the Automatic Program Corrector!"}

# @app.post("/file", status_code=status.HTTP_201_CREATED, status_code=status.HTTP_201_CREATED)
# async def upload_file(file: UploadFile = File(...)):

#     with open(f"input/{file.filename}", "wb") as f:
#         shutil.copyfileobj(file.file, f)
#     msg = pynguinAPI.run(get_file_name_without_extension(file.filename))

#     return {"msg": "File uploaded successfully"}
#     # return {"msg": msg}

@app.post("/files")
async def upload_files(files: List[UploadFile] = File(...), status_code=status.HTTP_201_CREATED):

    msg_list = []
    for file in files:
        with open(f"input/{file.filename}", "wb") as f:
            shutil.copyfileobj(file.file, f)

        msg_list.append(pynguinAPI.run(get_file_name_without_extension(file.filename)))
    return {"msg": "Files uploaded successfully"}
    # return {"msg": msg_list}



if __name__ == '__main__':
    server.run(app, host='127.0.0.1', port=8000)