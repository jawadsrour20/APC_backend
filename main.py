from fastapi import FastAPI, UploadFile, File, status, HTTPException, Depends, Body, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
from typing import List, Optional
import uvicorn as server
import os

import pynguinAPI
from auth import auth_handler
from cors import *
from http_status_codes import *
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import crud, models, schemas
import utils
from datetime import datetime
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
    # allow_origins=origins,
    allow_origins=["*"],
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

    # create a submissions folder for the new student upon registration
    utils.create_folder(user.username)

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
    return {
        "average_grade": average_grade,
        "overdue_submissions": overdue_submissions,
        "problems": problems,
        "username": user_info["username"],
        "name": user_info["name"],
        "instructor_name": user_info["instructor_name"]
        }

@app.get("/problems/{problem_id}", status_code=HTTP_STATUS_CODE_OK)
def available_problem(problem_id: int, user_info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):

    problem = crud.get_problem(db, problem_id)
    return {"problem": problem,
            "username": user_info["username"],
            "name": user_info["name"],
            "instructor_name": user_info["instructor_name"]
            }

@app.post("/problems/{problem_id}", status_code=HTTP_STATUS_CODE_CREATED)
def submit_problem(problem_id: int, file: UploadFile = File(...), user_info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):

    username = user_info["username"]
    student_id = crud.get_user_id(db, user_info["username"]).id
    problem = crud.get_problem(db, problem_id)
    problem_name = utils.get_file_name_without_extension(problem.file_name)
    test_cases_file_name = f"test_{problem_name}.py"
    test_cases_file_path = f"./output/{test_cases_file_name}"
    student_test_cases_file_path = f"submissions/{username}/{test_cases_file_name}"

    with open(f"submissions/{username}/{problem_name}.py", "wb") as f:
        shutil.copyfileobj(file.file, f)

    with open(student_test_cases_file_path, "wb") as f:
        shutil.copyfile(test_cases_file_path,student_test_cases_file_path)

    number_of_test_cases = utils.count_test_cases(test_cases_file_path)
    with open(f"submissions/{username}/{test_cases_file_name}", 'a') as f:
            f.write("\ncount_passed_test_cases = 0\n")
            for test_case_index in range(number_of_test_cases):
                f.write("try:\n\t")
                f.write(f"test_case_{test_case_index}()\n\t")
                f.write("count_passed_test_cases += 1\n")
                f.write("except Exception:\n\tpass\n")
            f.write("print(count_passed_test_cases)")

    number_of_passed_test_cases = int(utils.evaluate_passed_test_cases(student_test_cases_file_path))
    number_of_failed_test_cases = number_of_test_cases - number_of_passed_test_cases
    grade_received = (number_of_passed_test_cases / number_of_test_cases) * 100
    # compare against pynguin test cases for the problem
    # assign grade to submission + test cases passed + test cases failed

    grade = schemas.GradeCreate(student_id=student_id, problem_id=problem_id,
                            test_cases_passed=number_of_passed_test_cases, test_cases_failed=number_of_failed_test_cases,
                            grade_received=grade_received, submission_date=datetime.now())

    return crud.add_grade(db=db, grade=grade)

@app.get("/questions", status_code=HTTP_STATUS_CODE_OK)
def available_questions(user_info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):

    if not user_info["is_instructor"]:
        raise HTTPException(status_code=HTTP_STATUS_CODE_FORBIDDEN,
            detail="You are Un-authorized to access this page. Only instructors can have access.")

    questions = crud.get_problems(db)
    return {"questions": questions,
            "username": user_info["username"],
            "name": user_info["name"],
            }

@app.get("/questions/{question_id}", status_code=HTTP_STATUS_CODE_OK)
def available_question(question_id: int, user_info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    if not user_info["is_instructor"]:
        raise HTTPException(status_code=HTTP_STATUS_CODE_FORBIDDEN,
                detail="You are Un-authorized to access this page. Only instructors can have access.")

    question = crud.get_problem(db, question_id)
    return {"question": question }


@app.delete("/questions/{question_id}", status_code=HTTP_STATUS_CODE_OK)
def delete_question(question_id: int, user_info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    if not user_info["is_instructor"]:
        raise HTTPException(status_code=HTTP_STATUS_CODE_FORBIDDEN,
                detail="You are Un-authorized to access this page. Only instructors can have access.")

    is_deleted = crud.delete_problem(db, question_id)
    return {"is_deleted": is_deleted }


# Note: we can't use JSON object + UploadFile in the same API.
# Altenratively, we can use Form() with UploadFile
@app.post("/questions", status_code=HTTP_STATUS_CODE_CREATED)
def add_question(problem_title: str = Form(...), problem_description: str = Form(...),
                 due_date: datetime = Form(...), file: UploadFile = File(...),
                 user_info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):

    if not user_info["is_instructor"]:
        raise HTTPException(status_code=HTTP_STATUS_CODE_FORBIDDEN,
                detail="You are Un-authorized to access this page. Only instructors can have access.")

    with open(f"input/{file.filename}", "wb") as f:
            shutil.copyfileobj(file.file, f)


    # Problem difficulty is evaluated using the radon halstead metrics
    difficulty = utils.get_problem_difficulty(file.filename)

    function_prototype = utils.get_function_prototype("input", file.filename)

    problem = schemas.ProblemCreate(title=problem_title, description=problem_description,
                function_prototype=function_prototype, due_date=due_date, file_name=file.filename, difficulty=difficulty)

    crud.add_problem(db=db, problem=problem)

    msg = [pynguinAPI.run(file.filename)]
    file_tests_dict = {file.filename: pynguinAPI.count_passed_and_failed_test_cases(file.filename)}

    return {"file_tests_dict" : file_tests_dict}

@app.get("/submissions-dashboard", status_code=HTTP_STATUS_CODE_OK)
def submissions_dashboard(user_info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):

    if not user_info["is_instructor"]:
        raise HTTPException(status_code=HTTP_STATUS_CODE_FORBIDDEN, 
                            detail="You are Un-authorized to access this page. Only instructors can have access.")

    return crud.get_students_statistics(db, username=user_info["username"])


# @app.post("/files")
# async def upload_files(files: List[UploadFile] = File(...), status_code=status.HTTP_201_CREATED):

#     msg_list = []
#     file_tests_dict = {}
#     for file in files:
#         with open(f"input/{file.filename}", "wb") as f:
#             shutil.copyfileobj(file.file, f)

#         msg_list.append(pynguinAPI.run(file.filename))
#         file_tests_dict[file.filename] = pynguinAPI.count_passed_and_failed_test_cases(file.filename)

#     return {"msg": "Files uploaded successfully"}
#     # return {"msg": msg_list}


data_set_file = 'speed_at_intersection.xlsx'
data_set_path = f'{os.getcwd()}/integration/{data_set_file}'

@app.post('/data_set', response_class=FileResponse, status_code=HTTP_STATUS_CODE_CREATED)
async def generate_data_set(number_of_test_cases: int = Form(...)):
    pynguinAPI.generate_data_set("speed_at_intersection.py", number_of_test_cases)
    return FileResponse(path=data_set_path, filename=data_set_file, media_type='application/octet-stream')

if __name__ == '__main__':
    server.run(app, host='127.0.0.1', port=8000)