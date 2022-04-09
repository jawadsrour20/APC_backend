# sourcery skip: avoid-builtin-shadow
"""     Contains the models for the database used by sqlalchemy for ORM.    """
# Setup reference: https://fastapi.tiangolo.com/tutorial/sql-databases/
from sqlalchemy import \
            Boolean, Column, ForeignKey, \
            Integer, String, Float, Text, \
            DateTime, UniqueConstraint

from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    # name of the table in the database
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # note: In sql databases index are used speed up query performance.
    email = Column(String(255), unique=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False, index=True) # index=True does nullable=False internally
    first_name = Column(String(50), nullable=False, index=True)
    last_name = Column(String(50), nullable=False, index=True)
    is_instructor = Column(Boolean, default=False)
    instructor_name = Column(String(255), index=True, default=None)

class Problem(Base):

    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(Text(5000), index=True)
    function_prototype = Column(String(255), index=True)
    file_name = Column(String(255), index=True)
    due_date = Column(DateTime, index=True)

class Grade(Base):

    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False) # by default SQL allows for nullable
    problem_id = Column(Integer, ForeignKey("problems.id"), index=True, nullable=False)
    test_cases_passed = Column(Integer, index=True)
    test_cases_failed = Column(Integer, index=True)
    grade_received = Column(Integer, index=True)
    submission_date = Column(DateTime, index=True)

    __table_args__ = (
        # this can be PrimaryKeyConstraint if you want it to be a primary key
        # each student can solve a problem only once.
        # So, there can be only one (student, problem) pair in the table.
        UniqueConstraint('student_id', 'problem_id', name='_student_problem_uc'),
      )