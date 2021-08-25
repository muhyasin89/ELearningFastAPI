import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ROOT_DIR = os.path.dirname(os.path.realpath(__file__)+'../../../db/')

DATABASE_DIR = os.path.join(os.path.dirname(__file__), "../../db")

SQLALCHEMY_DATABASE_URL = "sqlite:///{}/sql_app.db".format(DATABASE_DIR)
print(SQLALCHEMY_DATABASE_URL)
# SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
# SQLALCHEMY_DATABASE_URL = "sqlite:///sql_app.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
