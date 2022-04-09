""" Contains the SQL Queries used by sqlalchemy for ORM. """
# Note: CRUD Stands for Create, Read, Update, and Delete.

from sqlalchemy.orm import Session

import models, schemas
import datetime
from auth import auth_handler
from http_status_codes import *

# db.query().first() -> returns an object
# db.query().all() -> returns a list of objects
## Database READ functions


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_students(db: Session):
    return db.query(models.User).filter(models.User.is_instructor == False).all()

def get_instructor_students(db: Session, instructor_name: str):
    return db.query(models.User) \
            .filter(models.User.instructor_name == instructor_name, models.User.is_instructor == False) \
            .all()

def get_user_id(db: Session, username: str):
    return db.query(models.User.id).filter(models.User.username == username).first()

def get_problem(db: Session, problem_id: int):
    return db.query(models.Problem).filter(models.Problem.id == problem_id).first()

def get_problems(db: Session):
    return db.query(models.Problem).all()


def get_problems_submitted(db: Session, username: str):
    return db.query(models.Grade, models.Problem, models.User) \
        .filter(models.Grade.student_id == models.User.id) \
        .filter(models.Grade.problem_id == models.Problem.id) \
        .filter(models.User.username == username, ) \
        .all()
        # .values(models.Grade.problem_id, models.Grade.submission_date, models.Problem.due_date)

# retrieves list of available problems with status of being solved/unsolved by the student
def get_problems_with_status(db: Session, username: str):


    problems = get_problems(db)
    submitted_problems = get_problems_submitted(db, username)
    submitted_problems_ids = [problem.Grade.problem_id for problem in submitted_problems]

    for i in range(len(problems)):
        # initially assume all problems are not solved + not overdue
        problems[i].is_solved = False
        problems[i].is_overdue = False
        problems[i].submission_date = None
        if problems[i].id in submitted_problems_ids:
            problems[i].is_solved = True
            problems[i].submission_date = get_grade_by_problem_id(db, username, problems[i].id).submission_date

        # if due date has passed, and the problem was not solved --> overdue
        if problems[i].due_date < datetime.datetime.now() and not problems[i].is_solved:
            problems[i].is_overdue = True

    return problems

def get_grade(db: Session, grade_id: int):
    return db.query(models.Grade).filter(models.Grade.id == grade_id).first()

def get_grade_by_problem_id(db: Session, username: str, problem_id: int):
    user = get_user_id(db, username)
    student_id = user.id
    return db.query(models.Grade).filter(models.Grade.student_id == student_id, models.Grade.problem_id == problem_id).first()

def get_student_grades(db: Session, username: str):
    user = get_user_id(db, username)
    student_id = user.id # no need for indexing since user is an object not hash-map
    return db.query(models.Grade).filter(models.Grade.student_id == student_id).all()

def get_average_grade(db: Session, username: str):
    grades = get_student_grades(db, username)

    if len(grades) == 0:
        return 0

    total_grade = sum(grade.grade_received for grade in grades)

    return total_grade / len(grades)

def get_number_of_problems_solved(db: Session, username: str):
    grades = get_student_grades(db, username)
    return len(grades)

# reference for joining between several tables:
# https://stackoverflow.com/questions/6044309/sqlalchemy-how-to-join-several-tables-by-one-query
# reference for retrieving multiple columns
# https://stackoverflow.com/questions/11530196/flask-sqlalchemy-query-specify-column-names
def get_number_of_overdue_submissions(db: Session, username: str):

    problems = get_problems_with_status(db, username)
    overdue_problems = [problem for problem in problems if problem.is_overdue]
    return len(overdue_problems)

# username = instructor_name
def get_students_statistics(db: Session, username: str):

    students = get_instructor_students(db, instructor_name=username)
    statistics = {student.username: [] for student in students}

    records = db.query(models.Grade, models.Problem, models.User) \
        .filter(models.Grade.student_id == models.User.id) \
        .filter(models.Grade.problem_id == models.Problem.id) \
        .filter(models.User.instructor_name == username, ) \
        .values(models.User.username, models.Problem.title, models.Grade.grade_received, models.Grade.submission_date)

    for record in records:
        if statistics.get(record[0]) is not None:
            statistics[record[0]].append({
                'problem_title': record[1],
                'grade_received': record[2],
                'submission_date': record[3]
            })
    for student in statistics:
        statistics[student].append({"average_grade": get_average_grade(db, student)})

    return statistics


## Database READ functions END




## Database CREATE functions
# function takes as input a Pydantic user object
# it then creates a sqlalchemy user object to be added to the database
def create_user(db: Session, user: schemas.UserCreate):

    hashed_password = auth_handler.get_password_hash(user.password)
    # SQLAlchemy model object/instance
    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password,
                          first_name=user.first_name, last_name=user.last_name)
    db.add(db_user) # add the user to the database
    db.commit() # commit changes so they are saved
    db.refresh(db_user) # refresh instance so that it contains any new data from the database, like the generated ID
    return HTTP_STATUS_CODE_CREATED

def add_problem(db: Session, problem: schemas.ProblemCreate):

    # SQLAlchemy model object/instance
    db_problem = models.Problem(title=problem.title, description=problem.description,
                    function_prototype=problem.function_prototype, file_name=problem.file_name,
                    due_date=problem.due_date)
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return HTTP_STATUS_CODE_CREATED

def add_grade(db: Session, grade: schemas.GradeCreate):
    # SQLAlchemy model object/instance
    db_grade = models.Grade(student_id=grade.student_id, problem_id=grade.problem_id,
                            test_cases_passed=grade.test_cases_passed, test_cases_failed=grade.test_cases_failed,
                            grade_received=grade.grade_received)
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return HTTP_STATUS_CODE_CREATED

## Database CREATE functions END
