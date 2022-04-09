from fastapi import FastAPI, UploadFile, File, status, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
import shutil
from typing import List, Optional
import uvicorn as server
import pynguinAPI

from auth import auth_handler
from cors import *
from http_status_codes import *
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import crud, models, schemas

# Create Database Tables
models.Base.metadata.create_all(bind=engine)


# Dependency: will create a new SQLAlchemy SessionLocal that will be used in a single request,
# and then close it once the request is finished.
async def get_db():
    db = SessionLocal()
    try:
        yield db
    # The code following the yield statement is executed after the response has been delivered:
    # we could've declared the function async instead of using yield
    finally:
        db.close()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"msg": "Welcome to the Automatic Program Corrector!"}


@app.post("/register", status_code=HTTP_STATUS_CODE_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    is_email_taken = bool(crud.get_user_by_email(db, user.email))
    is_username_taken = bool(crud.get_user_by_username(db, user.username))
    if is_email_taken:
        raise HTTPException(status_code=HTTP_STATUS_CODE_BAD_REQUEST, detail="Email already registered")
    if is_username_taken:
        raise HTTPException(status_code=HTTP_STATUS_CODE_BAD_REQUEST, detail="Username already taken")

    return crud.create_user(db=db, user=user)

@app.post("/login")
def login(username: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=HTTP_STATUS_CODE_UNAUTHORIZED, detail="Invalid credentials")
    is_password_correct = auth_handler.verify_password(password, user.hashed_password)
    if not is_password_correct:
        raise HTTPException(status_code=HTTP_STATUS_CODE_UNAUTHORIZED, detail="Invalid credentials")
    JWT = auth_handler.encode_token(user.username, user.first_name,
                                    user.last_name, user.is_instructor, user.instructor_name)

    return {"token": JWT}


# Protected routes
@app.get("/home", status_code=HTTP_STATUS_CODE_OK)
def home(user_info=Depends(auth_handler.auth_wrapper)):
    return {"username": user_info["username"],
            "name": user_info["name"]
            }

@app.get("/problems", status_code=HTTP_STATUS_CODE_OK)
def available_problems(user_info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    overdue_submissions = crud.get_number_of_overdue_submissions(db, user_info["username"])
    average_grade = crud.get_average_grade(db, user_info["username"])
    problems = crud.get_problems_with_status(db, user_info["username"])
    return {"average_grade": average_grade,
            "overdue_submissions": overdue_submissions,
            "problems": problems,
            "username": user_info["username"],
            "name": user_info["name"],
            "instructor_name": user_info["instructor_name"]
            }

@app.post("/files")
async def upload_files(files: List[UploadFile] = File(...), status_code=status.HTTP_201_CREATED):

    msg_list = []
    file_tests_dict = {}
    for file in files:
        with open(f"input/{file.filename}", "wb") as f:
            shutil.copyfileobj(file.file, f)

        msg_list.append(pynguinAPI.run(file.filename))
        file_tests_dict[file.filename] = pynguinAPI.count_passed_and_failed_test_cases(file.filename)
    # print(file_tests_dict)
    return {"msg": "Files uploaded successfully"}
    # return {"msg": msg_list}



if __name__ == '__main__':
    server.run(app, host='127.0.0.1', port=8000)