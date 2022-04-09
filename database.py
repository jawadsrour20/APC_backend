from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

config = dotenv_values(".env")

USER = config.get("user")
PASSWORD = config.get("password")
HOST = config.get("host")
DATABASE_NAME = config.get("database_name")
PORT = config.get("port")

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"

# Creating sqlalchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
