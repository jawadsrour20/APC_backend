# keep all code that we don't need for now here

# decide on keeping or removing upload single File API... the upload multiple files can be used to upload one file ...
# @app.post("/file", status_code=status.HTTP_201_CREATED, status_code=status.HTTP_201_CREATED)
# async def upload_file(file: UploadFile = File(...)):

#     with open(f"input/{file.filename}", "wb") as f:
#         shutil.copyfileobj(file.file, f)
#     msg = pynguinAPI.run(get_file_name_without_extension(file.filename))

#     return {"msg": "File uploaded successfully"}
#     # return {"msg": msg}