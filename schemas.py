"""
    Here we define the schemas for the pydantic models.
    we need pydantic for the authentication process + object Models
    we will be re-defining a similar User class for sqlalchemy for ORM usage

"""
# Setup reference: https://fastapi.tiangolo.com/tutorial/sql-databases/

from pydantic import BaseModel
from typing import Optional
import datetime

# UserBase Pydantic model (or let's say "schema") to have common attributes while creating or reading data.
class UserBase(BaseModel):
    email: str # Required field
    username: str # Required field
    first_name: str # Required field
    last_name: str # Required field

# Used for Creating a user
class UserCreate(UserBase):
    password: str # Required field


# Before creating an item, we don't know what will be the ID assigned to it,
# but when reading it (when returning it from the API) we will already know its ID.

# Used for Reads when fetching a user
class User(UserBase):
    id: int # after the user is created, we know user id

    # in the Pydantic models for reading, add an internal Config class; used to provide configurations to Pydantic
    class Config:
        orm_mode = True # this is used to tell pydantic that we are using sqlalchemy ORM

class ProblemBase(BaseModel):

    title: str
    description: str
    function_prototype: str
    file_name: str
    difficulty: str
    due_date: datetime.datetime # in request, responses, will be represented as str

class ProblemCreate(ProblemBase):
    pass

class Problem(ProblemBase):
    id: int

    class Config:
        orm_mode = True # this is used to tell pydantic that we are using sqlalchemy ORM


class GradeBase(BaseModel):

    student_id: int
    problem_id: int
    test_cases_passed: int
    test_cases_failed: int
    grade_received: float
    submission_date: datetime.datetime

class GradeCreate(GradeBase):
    pass

class Grade(GradeBase):

    id: int

    class Config:
        orm_mode = True # this is used to tell pydantic that we are using sqlalchemy ORM
